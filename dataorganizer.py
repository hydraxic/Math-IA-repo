import matplotlib.pyplot as plt;
import numpy as np;
from matplotlib import colors;
from matplotlib.ticker import PercentFormatter;
from scipy import stats;
import json;
import math;
import seaborn as sns;
import powerlaw;

file = open("games.json", encoding = "utf8");
data = json.load(file);

popularity = [];
prices = [];
reviewRatio = [];
positiveReviewsArr = [];
pricesPopularity = [[prices], [popularity]];

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





