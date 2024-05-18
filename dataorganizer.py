import matplotlib.pyplot as plt;
import numpy as np;
from matplotlib import colors;
from matplotlib.ticker import PercentFormatter;
from scipy import stats;
import json;
import math;
import seaborn as sns;
import powerlaw;
from sklearn import linear_model;
from sklearn.feature_extraction import DictVectorizer;
import time
import requests
from bs4 import BeautifulSoup
import random;
from requests.auth import HTTPProxyAuth
#import argparse

#parser = argparse.ArgumentParser(description='Get Google Count.')
#parser.add_argument('word', help='word to count')
#args = parser.parse_args()

#headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"}

user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

proxies = [ # gotten from webshare
    "http://38.154.227.167:5868",
    "http://185.199.229.156:7492",
    "http://185.199.228.220:7300",
    "http://185.199.231.45:8382",
    "http://188.74.210.207:6286",
    "http://188.74.183.10:8279",
    "http://188.74.210.21:6100",
    "http://45.155.68.129:8133",
    "http://154.95.36.199:6893",
    "http://45.94.47.66:8110",
]

file = open("games.json", encoding = "utf8");
data = json.load(file);

popularity = [];
prices = [];
reviewRatio = [];
positiveReviewsArr = [];
pricesPopularity = [[prices], [popularity]];
googlePopularity = [];

monthsData = {"Jan": [0, 0], "Feb": [0, 0], "Mar": [0, 0], "Apr": [0, 0], "May": [0, 0], "Jun": [0, 0], "Jul": [0, 0], "Aug": [0, 0], "Sep": [0, 0], "Oct": [0, 0], "Nov": [0, 0], "Dec": [0, 0]};
monthsAverage = {"Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0};

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
# x - 101 / 16740 - 101 = 0.4
# x = 6756.6

def reject_outliers_median(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]

def reject_outliers_mean(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def reject_outliers_merge(data, m=2):
    return data[abs(data - np.median(data)) < m * np.std(data)]

def IQR_outliers(data):
    sorted(data)
    Q1,Q3 = np.percentile(data , [25,75])
    IQR = Q3 - Q1
    lower_range = Q1 - (1.5 * IQR)
    upper_range = Q3 + (1.5 * IQR)
    return [d for d in data if lower_range <= d <= upper_range]

def IQR_outliers_remove_all(popdata):
    sorted(popdata)
    Q1,Q3 = np.percentile(popdata , [25,75])
    IQR = Q3 - Q1
    lower_range = Q1 - (1.5 * IQR)
    upper_range = Q3 + (1.5 * IQR)
    for i, v in enumerate(popdata):
        if not lower_range <= v <= upper_range:
            del popdata[i]
            del prices[i]
            del reviewRatio[i]
    return popdata

'''
def is_outlier(points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False 
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh
'''

count = 0;

for i in data:
    name = data[i]["name"];
    releaseDate = data[i]["release_date"];
    price = data[i]["price"];
    positiveReviews = data[i]["positive"];
    negativeReviews = data[i]["negative"];
    peakConcurrent = data[i]["peak_ccu"];
    
    if peakConcurrent > 100 and peakConcurrent < 20000 and price < 100:
        if (not negativeReviews == 0 and not positiveReviews == 0):
            popularity.append(peakConcurrent);
            reviewRatio.append(positiveReviews/negativeReviews);
            positiveReviewsArr.append(positiveReviews);
            prices.append(price);
            monthsData[releaseDate.split(" ")[0]][0] += 1;
            monthsData[releaseDate.split(" ")[0]][1] += peakConcurrent;
            count += 1;

            realresult = True;
            while not realresult:

                time.sleep(random.randint(1, 3))
                #t = random.choice(proxies)
                #proxies = {
                #    "http": t,
                #    "https": t
                #}
                #headers = {"User-Agent": random.choice(user_agent_list)}
                headers = headers = {
                    'User-Agent': random.choice(user_agent_list),
                    'Accept': '*/*',
                    'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
                    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
                    #'Referer': 'https://www.bing.com/search?q=age+of+wonders+4+video+game&form=QBLH&sp=-1&ghc=1&lq=0&pq=age+of+wonders+4+video+gam&sc=3-26&qs=n&sk=&cvid=4EEEF19338F54CAE9F6DB81DF080C450&ghsh=0&ghacc=0&ghpl=',
                    'DNT': '1',
                    'Sec-GPC': '1',
                    'Connection': 'keep-alive',
                    # 'Cookie': 'MUID=0FD2A8B95349697F0AF2BC3A529B6829; MUIDB=0FD2A8B95349697F0AF2BC3A529B6829; _EDGE_S=F=1&SID=0EBB037113026F4E101917F212D06E74&mkt=en-ca; _EDGE_V=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=43289598238242DB9042835DE206F0AD&dmnchg=1; SRCHUSR=DOB=20240518&T=1715993917000; SRCHHPGUSR=SRCHLANG=en&BRW=XW&BRH=S&CW=1920&CH=533&SCW=1903&SCH=4050&DPR=1.0&UTC=-240&DM=1&WTS=63851590717&HV=1715993930&PRVCW=1920&PRVCH=936&CIBV=1.1742.1&EXLTT=1; _SS=SID=0EBB037113026F4E101917F212D06E74&R=3&RB=0&GB=0&RG=200&RP=0; _HPVN=CS=eyJQbiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyNC0wNS0xOFQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjoyLCJUb2JuIjowfQ==; ak_bmsc=60A1FBA99EB7B4484C382B75506E28BA~000000000000000000000000000000~YAAQVw/QF0RMlHqPAQAADTo1iRe8XpEwdaYb8ChoLk6s8XO43T2R2HpaupmTpKsmgRsDvcVV71G41qalfCK/9rOCnRIhzfkg9u/QnEWP+1Dzy2iKEiSNIwg0VeZAsr/Vr/DG2vjicU+RGItd6CkfG8zE/tBlp0rd1Yt18dX6uwZMr0qtu9KIFhtq2cTU6mlH/o7fdV2Pm4HL3d7Fk/Q4xg3shmcZjzquQ7+PpduSmlyaQkKBEY2KX0hgkHLrBsbuQCVXgvGvmlAayDaDwnH4Pj3+7+GrwvG+uF1X38t2kWqBiir4PTrDiXzOpM6g8OCkEOpflo45n2cybrjbc5/zKbhMvbjOAcPg/xnfdDM41VZS3GsKHp1zqQ8Vl63SC1Ppo9jKU9N6Fw==; BCP=AD=0&AL=0&SM=0; _UR=cdxcls=0&QS=0&TQS=0; ipv6=hit=1715997532191; _RwBf=r=0&ilt=2&ihpd=1&ispd=1&rc=3&rb=0&gb=0&rg=200&pc=0&mtu=0&rbb=0&g=0&cid=&clo=0&v=2&l=2024-05-17T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=0001-01-01T00:00:00.0000000&rwflt=0001-01-01T00:00:00.0000000&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2024-05-18T00:58:48.7067294+00:00&rwred=0&wls=&wlb=&wle=&ccp=&cpt=&lka=0&lkt=0&aad=0&TH=; _Rwho=u=d&ts=2024-05-18; ai_session=qSQyjTywAsNv3DMYMl1i7C^|1715993921844^|1715993921844; bm_sv=50EEBC49F587AA5AC3B04921FCBAD36D~YAAQVw/QFwdNlHqPAQAAkVs1iRdic9uP8iruBWXuHh7qonV8K5KYHHLpV25VnfCXZINc9i3DKA8xIsg925bn3MMbafFzGJnd8hMouZjdihEmwp+lknFUEuB03FPfoAJMst+ENrL+r3XxXl8C8qhLRPfe8lwPeVLx9lZzMN9n7PGlYpLB5SD81WEpb3a69YSVRpmU05OjDjQsnob3L74xNl+F3GENod3GiJZGG3AL+YXAZCBOAwP1rn1Bjdxmcg==~1; USRLOC=HS=1&ELOC=LAT=44.25663757324219^|LON=-76.56807708740234^|N=Kingston^%^2C^%^20Ontario^|ELT=4^|; dsc=order=ShopOrderDefault',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    # Requests doesn't support trailers
                    # 'TE': 'trailers',
                }
                auth = HTTPProxyAuth('dnbcukvf', 'pog5buvc42ya');
                #r = requests.get('https://www.google.com/search?q="{}" video game'.format(name), headers=headers, proxies={"http": "http://dnbcukvf-rotate:pog5buvc42ya@p.webshare.io:80/","https": "http://dnbcukvf-rotate:pog5buvc42ya@p.webshare.io:80/"}, auth=auth)
                # try using bing instead, google is blocking the requests
                try:
                    r = requests.get('https://www.bing.com/search?q="{}" video game'.format(name), headers=headers, proxies={"http": "http://dnbcukvf-rotate:pog5buvc42ya@p.webshare.io:80/","https": "http://dnbcukvf-rotate:pog5buvc42ya@p.webshare.io:80/"}, auth=auth)
                    print(r.url, r.status_code)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    print(soup.find('span', {'class': 'sb_count'}).text)
                #print(soup.find('div',{'id':'resultStats'}).text)
                    resultg = int(soup.find('span', {'class': 'sb_count'}).text.split(' ')[1].replace('.',''))
                    realresult = True;
                except Exception as e:
                    realresult = False;
                    if e == AttributeError:
                        print("detected the scraper i think bing should be ashamed of themselves")
                    if e == ValueError:
                        print("gave string in sb_count")
                    if e == requests.exceptions.ChunkedEncodingError:
                        print("chunked encoding error")
                    pass
            #googlePopularity.append(resultg)

fs = open('currentlyHaveScraped.txt', 'r')
for i in fs:
    if (i.startswith('About')):
        try:
            googlePopularity.append(int(i.split(' ')[1].replace('.','')))
        except ValueError:
            pass

with open('googlepopularity.json', 'w') as f:
    json.dump(googlePopularity, f)

print(len(googlePopularity))
print(count);

#for i in prices:
#    if pricesPopularity[i]:



'''
popularity = np.asarray(popularity);

for i, v in enumerate(popularity):
    if (is_outlier(popularity)):
        del popularity[i];
        del prices[i];
'''
#cf = np.polyfit(prices, popularity, 1);
#poly1d = np.poly1d(cf);

pop = IQR_outliers_remove_all(popularity);

vdict = []
for i in range(len(pop)):
    vdict.append({'r': reviewRatio[i], 'p': prices[i]})
vec = DictVectorizer()
X = vec.fit_transform(vdict)
y = pop;

clf = linear_model.LinearRegression()
clf.fit(X, y)
print(clf.coef_, clf.intercept_)

# create a plane of regression using the r and p values
r = np.linspace(min(reviewRatio), max(reviewRatio), 100)
p = np.linspace(min(prices), max(prices), 100)
R, P = np.meshgrid(r, p)
Z = clf.coef_[0] * R + clf.coef_[1] * P + clf.intercept_

fig = plt.figure()
fig.set_figwidth(40)
fig.set_figheight(10)
ax = plt.axes(projection='3d')
ax.set_xlabel('r', fontsize=12, color='green')
ax.set_ylabel('p', fontsize=12, color='green')
ax.set_zlabel('P', fontsize=12, color='green')
ax.scatter3D(reviewRatio, prices, pop, color='green')
ax.plot_surface(R, P, Z, alpha=0.5)
plt.title("Plot of data points")
plt.show()







for i, v in monthsData.items():
    monthsAverage[i] = v[1] / v[0];


plt.bar(monthsAverage.keys(), monthsAverage.values());
plt.title("Games Released by Month");


plt.show();




popularity.sort();
prices.sort();

popularity_no_outliers = IQR_outliers(np.array(popularity));
prices_no_outliers = IQR_outliers(np.array(prices));

# PRICE CURVE
fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2);
prices_no_outliers.sort();
mu = np.mean(prices_no_outliers); print(mu)
sigma = np.std(prices_no_outliers); print(sigma)

norm_pdf = np.array(stats.norm.pdf(prices_no_outliers, mu, sigma));
ax1.plot(prices_no_outliers, norm_pdf)
ax1.set(xlabel="Prices (Outliers Removed) Min: " + str(round(min(prices_no_outliers), 4)) + " Max: " + str(round(max(prices_no_outliers), 4)), ylabel = "Probability", title="Normal Distribution of Prices")

sample_value = 40
z = (sample_value - mu) / sigma;

# POPULARITY CURVE
popularity.sort();
mu = np.mean(popularity_no_outliers); print(mu)
sigma = np.std(popularity_no_outliers); print(sigma)

norm_pdf = np.array(stats.norm.pdf(popularity_no_outliers, mu, sigma));
ax2.plot(popularity_no_outliers, norm_pdf)
ax2.set(xlabel="Highest Concurrent Players (Outliers Removed) Min: " + str(min(popularity_no_outliers)) + " Max: " + str(max(popularity_no_outliers)), ylabel = "Probability", title="Normal Distribution of Highest Concurrent Players")

pop_result = z * sigma + mu;
print(z, pop_result);

plt.show();











slope, intercept, r_value, p_value, std_err = stats.linregress(prices, popularity);
line = slope*np.array(prices)+intercept;

#plt.plot(prices, popularity, "yo", prices, poly1d(prices), "--k");
plt.plot(prices, line, "r", label = "y={:.2f}x+{:.2f}".format(slope, intercept));
plt.scatter(prices, popularity, color = "k", s=3.5);
plt.legend(fontsize = 9);
plt.show();

sloper, interceptr, r_valuer, p_valuer, std_errr = stats.linregress(reviewRatio, popularity);
liner = sloper*np.array(reviewRatio)+interceptr;

#plt.plot(prices, popularity, "yo", prices, poly1d(prices), "--k");
plt.plot(reviewRatio, liner, "r", label = "y={:.2f}x+{:.2f}".format(sloper, interceptr));
plt.scatter(reviewRatio, popularity, color = "k", s=3.5);
plt.legend(fontsize = 9);
plt.show();

pcounts, pbins = np.histogram(prices);
plt.stairs(pcounts, pbins);
plt.show();

# Bin limits
num_bin = 10
bin_lims = np.linspace(0,1,num_bin+1)
bin_centers = 0.5*(bin_lims[:-1]+bin_lims[1:])
bin_widths = bin_lims[1:]-bin_lims[:-1]

popularity_no_outliers = IQR_outliers(np.array(popularity));
reviewRatio = IQR_outliers(np.array(reviewRatio));

reviewRatio.sort();
popularity_no_outliers.sort();

fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2);
print(max(popularity_no_outliers), min(popularity_no_outliers), max(reviewRatio), min(reviewRatio))
counts, bins = np.histogram(popularity_no_outliers, bins=np.arange(min(popularity_no_outliers), max(popularity_no_outliers) + 1, (max(popularity_no_outliers)-min(popularity_no_outliers)) / 60));
ax1.stairs(NormalizeData(counts), bins);
#plt.show();z

rcounts, rbins = np.histogram(reviewRatio, bins=np.arange(min(reviewRatio), max(reviewRatio) + 1, (max(reviewRatio)-min(reviewRatio)) / 60));
ax2.stairs(NormalizeData(rcounts), rbins);

#histP = counts/np.max(counts);
#histR = rcounts/np.max(rcounts);

#plt.bar(bin_centers, histP, width = bin_widths, align = 'center')
#plt.bar(bin_centers, histR, width = bin_widths, align = 'center', alpha = 0.5)


plt.show();

#popularity_no_outliers = IQR_outliers(np.array(popularity));
#reviewRatio = IQR_outliers(np.array(reviewRatio));

# REVIEW RATIO CURVE
fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2);
reviewRatio.sort();
mu = np.mean(reviewRatio); print(mu)
sigma = np.std(reviewRatio); print(sigma)
#x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
#x = np.linspace(0, 1, 100)
#ax1.plot(NormalizeData(reviewRatio), np.array(stats.norm.pdf(reviewRatio, mu, sigma)))
#norm_pdf = np.array(stats.norm.pdf(reviewRatio, mu, sigma));
#ax1.plot(reviewRatio, norm_pdf)
edges, hist = powerlaw.pdf(reviewRatio)
bin_centers = (edges[1:]+edges[:-1])/2.0
ax1.plot(bin_centers, hist)

ax1.set(xlabel="Positive Review / Negative Reviews Ratio (Outliers Removed) Min: " + str(round(min(reviewRatio), 4)) + " Max: " + str(round(max(reviewRatio), 4)), ylabel = "Probability", title="Normal Distribution of Review Ratio")
#ax = plt.gca()
#ax.set_xlim([0, max(reviewRatio)])
#ax.set_ylim([0, 1])
# test value to convert to z score and convert to popularity
#sample_value = 0.0025;
sample_value = 2 #np.interp(25, reviewRatio, norm_pdf);
z = (sample_value - mu) / sigma;

# POPULARITY CURVE

popularity.sort();
mu = np.mean(popularity_no_outliers); print(mu)
sigma = np.std(popularity_no_outliers); print(sigma)
#x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
#x = np.linspace(0, 1, 100)
#ax2.plot(NormalizeData(popularity_no_outliers), np.array(stats.norm.pdf(popularity_no_outliers, mu, sigma)))
    #norm_pdf = np.array(stats.norm.pdf(popularity_no_outliers, mu, sigma));
#fit = stats.powerlaw.fit(popularity_no_outliers)
#power_pdf = np.array(fit)
edges, hist = powerlaw.pdf(popularity_no_outliers)
bin_centers = (edges[1:]+edges[:-1])/2.0
ax2.plot(bin_centers, hist)

#ax2.plot(popularity_no_outliers, power_pdf)
ax2.set(xlabel="Highest Concurrent Players (Outliers Removed) Min: " + str(min(popularity_no_outliers)) + " Max: " + str(max(popularity_no_outliers)), ylabel = "Probability", title="Normal Distribution of Highest Concurrent Players")
#ax = plt.gca()
#ax.set_xlim([0, 1])

pop_result = z * sigma + mu;
#sample_result = np.interp(pop_result, norm_pdf, popularity_no_outliers);
print(z, pop_result);

plt.show();
#ax.set_ylim([0, 1])
plt.hist2d(reviewRatio, popularity, bins=(np.arange(min(reviewRatio), max(reviewRatio) + 5, 5), np.arange(min(reviewRatio), max(reviewRatio) + 5, 5)), cmap = plt.cm.jet)
plt.colorbar();
plt.show()

sns.boxplot(popularity); # Boxplot outliers default calculation is 1.5 * IQR
plt.show();

#reviewRatio = positiveReviews / negativeReviews;



#clump into 1000 data points per dot





