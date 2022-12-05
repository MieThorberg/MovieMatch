import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def load_movies():
    movies_df = pd.read_csv('data/movies_metadata.csv', usecols=['id', 'title'])
    return movies_df


def load_ratings():
    ratings_df = pd.read_csv('data/ratings_small.csv', usecols=['userId', 'movieId', 'rating'],
                            dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})
    return ratings_df


def prepare_movies(movies_df):
    # drops Nan values
    movies_df.dropna(inplace=True)
    # defines Dtype of id
    movies_df["id"] = movies_df['id'].astype(pd.Int64Dtype())
    # renames id to movieId for later merge
    movies_df = movies_df.rename(columns={'id': 'movieId'})
    return movies_df


def prepare_data():
    rating_df = load_ratings()
    movies_df = prepare_movies(load_movies())
    df = prepare_df_data(merge_movies_and_ratings(rating_df, movies_df))
    return df


def prepare_df_data(df):
    rating_counts_df = count_ratings(df)
    # merges the totalRatingCount on title
    rating_with_total_rating_counts_df = merge_total_rating_counts(df, rating_counts_df)
    # removes all movies with less than 20 rating counts
    popular_movies_df = get_popular_movies(rating_with_total_rating_counts_df, 20)
    return popular_movies_df


def count_ratings(df):
    # groups all the same title, counts all the ratings and renames ratings to totalRatingCount
    rating_counts_df = (df.
    groupby(by=['title'])['rating'].
    count().
    reset_index().
    rename(columns={'rating': 'totalRatingCount'})
    [['title', 'totalRatingCount']]
    )
    return rating_counts_df


def merge_movies_and_ratings(ratings_df, movies_df):
    return pd.merge(ratings_df, movies_df, on='movieId')


def merge_total_rating_counts(df, rating_counts_df):
    return df.merge(rating_counts_df, left_on='title', right_on='title', how='left')


def get_popular_movies(rating_with_total_rating_counts_df, popularity_threshold):
    return rating_with_total_rating_counts_df[
        rating_with_total_rating_counts_df['totalRatingCount'] >= popularity_threshold]


def transform_df(df):
    return df.pivot_table(index='title', columns='userId', values='rating').fillna(0)


def find_nearest_neighbours(movie_features_df, index, n_neighbours):
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(movie_features_df)
    distances, indices = model_knn.kneighbors(movie_features_df.iloc[index, :].values.reshape(1, -1),
                                              n_neighbors=n_neighbours+1)
    recommends = []

    for i in range(1, len(distances.flatten())):
        recommends.append(movie_features_df.index[indices.flatten()[i]])

    return recommends


def make_cluster(movie_df):
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(movie_df)
    movie_df['labels'] = kmeans.labels_
    return movie_df


def optimise_k_means(data, max_k):
    means = [];
    inertias = []

    for k in range(1, max_k):
        kmeans = KMeans(n_clusters = k)
        kmeans.fit(data[[data.columns[1],data.columns[2]]])

        means.append(k)
        inertias.append(kmeans.inertia_)

    fig = plt.subplots(figsize=(10,5))
    plt.plot(means, inertias, 'o-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.grid(True)
    plt.show()


def recommend_movies(index, recommends_size):
    df = prepare_data()
    new_df = transform_df(df)
    recommends = find_nearest_neighbours(new_df, index, recommends_size)
    return recommends


def get_movie_index_by_title(title):
    data = prepare_data()
    df = transform_df(data)
    for i in range(len(df)):
        if df.index[i] == title:
            return i
    return -1


def get_all_movie_titles():
    data = prepare_data()
    df = transform_df(data)
    size = df.shape[0]
    movies = []
    for i in range(0, size):
        movies.append(df.index[i])
    return movies