import matplotlib.pyplot as plt;
import json;

file = open("results.json", encoding = "utf8");
data = json.load(file);

popularity = [];
prices = [];

for i in data:
    name = data[i]["name"];
    releaseDate = data[i]["release_date"];
    price = data[i]["price"];
    positiveReviews = data[i]["positive"];
    negativeReviews = data[i]["negative"];
    peakConcurrent = data[i]["peak_ccu"];
    
    print(price, peakConcurrent)
    popularity.append(peakConcurrent);
    prices.append(price);


plt.scatter(price, popularity, c = "blue");
plt.show();









#reviewRatio = positiveReviews / negativeReviews;



#clump into 1000 data points per dot
