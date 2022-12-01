import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors


def load_rating():
    rating_df = pd.read_csv('data/ratings_small.csv', usecols=['userId', 'movieId', 'rating'],
                            dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})
    return rating_df


def load_movies():
    movies_df = pd.read_csv('data/movies_metadata.csv', usecols=['id', 'title'])
    return movies_df


def prepare_movie_data(movies_df):
    # drops Nan values
    movies_df.dropna(inplace=True)
    # defines Dtype of id
    movies_df["id"] = movies_df['id'].astype(pd.Int64Dtype())
    # renames id to movieId for later merge
    movies_df = movies_df.rename(columns={'id': 'movieId'})
    return movies_df


def merge_movie_and_rating(rating_df, movies_df):
    df = pd.merge(rating_df, movies_df, on='movieId')
    return df


def count_ratings(df):
    # groups all of same title, counts all the ratings and remanes ratings to totalRatingCount
    movie_rating_count = (df.
    groupby(by=['title'])['rating'].
    count().
    reset_index().
    rename(columns={'rating': 'totalRatingCount'})
    [['title', 'totalRatingCount']]
    )
    return movie_rating_count


def prepare_df_data(df):
    movie_rating_count = count_ratings(df)
    # merges the totalRatingCount on title
    rating_with_total_rating_count = df.merge(movie_rating_count, left_on='title', right_on='title', how='left')
    rating_popular_movie = get_popular_movies(rating_with_total_rating_count)
    return rating_popular_movie


def get_popular_movies(rating_with_total_rating_count):
    # removes all movies with less then 50 ppl rating them.
    popularity_threshold = 50
    rating_popular_movie = rating_with_total_rating_count[
        rating_with_total_rating_count['totalRatingCount'] >= popularity_threshold]
    return rating_popular_movie


def prepare_data():
    rating_df = load_rating()
    movies_df = prepare_movie_data(load_movies())
    df = prepare_df_data(merge_movie_and_rating(rating_df, movies_df))
    return df


def create_rating_metrix(df):
    # puts all movie and user in a metrix with ratings
    movie_features_df = df.pivot_table(index='title', columns='userId', values='rating').fillna(0)
    return movie_features_df


def find_nearest_neighbours(movie_features_df, index, n_neighbours):
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(movie_features_df)
    distances, indices = model_knn.kneighbors(movie_features_df.iloc[index, :].values.reshape(1, -1),
                                              n_neighbors=n_neighbours+1)
    recommends = []

    for i in range(1, len(distances.flatten())):
        recommends.append(movie_features_df.index[indices.flatten()[i]])

    return recommends


def recommend_movies(index, recommends_size):
    df = prepare_data()
    movie_features_df = create_rating_metrix(df)
    recommends = find_nearest_neighbours(movie_features_df, index, recommends_size)
    return recommends
