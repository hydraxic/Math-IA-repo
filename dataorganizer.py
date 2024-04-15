import matplotlib.pyplot as plt;
import numpy as np;
from scipy import stats;
import json;

file = open("games.json", encoding = "utf8");
data = json.load(file);

popularity = [];
prices = [];
pricesPopularity = [[prices], [popularity]];
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
    
    if peakConcurrent > 500 and peakConcurrent < 20000 and price < 100:
        popularity.append(peakConcurrent);
        prices.append(price);

for i in prices:
    if pricesPopularity[i]:



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









#reviewRatio = positiveReviews / negativeReviews;



#clump into 1000 data points per dot
