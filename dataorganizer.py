import matplotlib.pyplot as plt;
import numpy as np;
from matplotlib import colors;
from matplotlib.ticker import PercentFormatter;
from scipy import stats;
import json;
import math;

file = open("games.json", encoding = "utf8");
data = json.load(file);

popularity = [];
prices = [];
reviewRatio = [];
positiveReviewsArr = [];
pricesPopularity = [[prices], [popularity]];

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

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

reviewRatio.sort();
popularity.sort();

fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2);
print(max(popularity), min(popularity), max(reviewRatio), min(reviewRatio))
counts, bins = np.histogram(popularity, bins=np.arange(min(popularity), max(popularity) + 1, (max(popularity)-min(popularity)) / 60));
ax1.stairs(NormalizeData(counts), bins);
#plt.show();

rcounts, rbins = np.histogram(reviewRatio, bins=np.arange(min(reviewRatio), max(reviewRatio) + 1, (max(reviewRatio)-min(reviewRatio)) / 60));
ax2.stairs(NormalizeData(rcounts), rbins);

#histP = counts/np.max(counts);
#histR = rcounts/np.max(rcounts);

#plt.bar(bin_centers, histP, width = bin_widths, align = 'center')
#plt.bar(bin_centers, histR, width = bin_widths, align = 'center', alpha = 0.5)


plt.show();

# REVIEW RATIO CURVE
fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2);
reviewRatio.sort();
mu = np.mean(reviewRatio); print(mu)
sigma = np.std(reviewRatio); print(sigma)
#x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
#x = np.linspace(0, 1, 100)
ax1.plot(NormalizeData(reviewRatio), np.array(stats.norm.pdf(reviewRatio, mu, sigma)))
ax1.set(xlabel="Positive Review / Negative Reviews Ratio (Normalized) Min: " + str(round(min(reviewRatio), 4)) + " Max: " + str(round(max(reviewRatio), 4)), ylabel = "Probability", title="Normal Distribution of Review Ratio")
#ax = plt.gca()
#ax.set_xlim([0, max(reviewRatio)])
#ax.set_ylim([0, 1])

# POPULARITY CURVE

popularity.sort();
mu = np.mean(popularity); print(mu)
sigma = np.std(popularity); print(sigma)
#x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
#x = np.linspace(0, 1, 100)
ax2.plot(NormalizeData(popularity), np.array(stats.norm.pdf(popularity, mu, sigma)))
ax2.set(xlabel="Highest Concurrent Players (Normalized) Min: " + str(min(popularity)) + " Max: " + str(max(popularity)), ylabel = "Probability", title="Normal Distribution of Highest Concurrent Players")
#ax = plt.gca()
#ax.set_xlim([0, 1])
plt.show();
#ax.set_ylim([0, 1])
plt.hist2d(reviewRatio, popularity, bins=(np.arange(min(reviewRatio), max(reviewRatio) + 5, 5), np.arange(min(reviewRatio), max(reviewRatio) + 5, 5)), cmap = plt.cm.jet)
plt.colorbar();
plt.show()


#reviewRatio = positiveReviews / negativeReviews;



#clump into 1000 data points per dot
