import pandas as pd
from sklearn.cluster import estimate_bandwidth
from sklearn.cluster import MeanShift
from ast import literal_eval
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.datasets import make_blobs


pd.set_option('display.width', 600)
pd.set_option('display.max_columns', 10)
data = pd.read_csv("data/movies_metadata.csv")
#id, genres
#data = data[['original_language']]
data = data.iloc[:2000]
print(data.head())
data['genre_names'] = data['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
print(data[['genres','genre_names']].head())
genres_df = pd.DataFrame(data['genre_names'].tolist())
print(genres_df.head())

genres_df = data['genre_names'].apply(pd.Series)
print("yo",genres_df.head())

stacked_genres = genres_df.stack()
print("stacked",stacked_genres)

#So, for each of the genres for each movie we now have a row. Here are the rows corresponding our first movie:
print("one row",stacked_genres[0])
# One-hot encoding of 'Embarked' with pd.get_dummies
dummies = pd.get_dummies(stacked_genres)
print(dummies.head())

# one row per movie
genre_dummies = dummies.sum(level=0)
print(genre_dummies.head())
data = pd.concat([data["vote_average"], genre_dummies], axis=1)


# Find missing values in the data and drop those rows:
# print('rows before drop n/a',len(data))
bool_matrix = data.isnull() # dataframe with True and False values for each cell in the titanic_data
only_null_filter = bool_matrix.any(axis=1) # is there a True value in any column in each row. returns a pandas Series with index matching index of titcanic dataframe
missing = data[only_null_filter] # show all rows that has one or more null values

# remove null value rows
data = data.dropna()
print('rows after',len(data))
# data
pd.options.display.max_rows = None # let me see all rows in the dataframe (can be used with columns too)
# bool_matrix
print(data.head())

bw = estimate_bandwidth(genre_dummies)
print(bw)
analyzer = MeanShift(bandwidth=bw)
analyzer.fit(genre_dummies)

labels = analyzer.labels_
print(labels)
print('\n\n',np.unique(labels))

cluster_centers = analyzer.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print(cluster_centers)
print("number of estimated clusters : %d" % n_clusters_)


X, y = make_blobs(n_samples=1946, centers=10, cluster_std=0.5)

colors = cycle("bgrcmykbgrcmykbgrcmykbgrcmyk")
for k, col in zip(range(n_clusters_), colors):
    my_members = labels == k
    cluster_center = cluster_centers[k]
    plt.plot(X[my_members, 0], X[my_members, 1], col + ".")
    plt.plot(
        cluster_center[0],
        cluster_center[1],
        "o",
        markerfacecolor=col,
        markeredgecolor="k",
        markersize=10,
    )
plt.title("Estimated number of clusters: %d" % n_clusters_)
plt.show()