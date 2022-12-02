import pandas as pd
import matplotlib.pyplot as plt
from ast import literal_eval
import modules.recommmender.CollaborativeRecommender as cr
import modules.recommmender.ContentRecommender as con


def prepare_movie_data():
    data = pd.read_csv("data/movies_metadata.csv")
    # data = data[data['original_language']=='en']
    # data = data[['budget', 'genres','id', 'imdb_id','title', 'popularity', 'release_date', 'revenue', 'runtime', 'vote_average', 'vote_count']]
    # data = data[(data['genres'] != "[]")]
    # data['genres'] = data['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    # data = data[(data.T != 0).all()]
    return data


def get_all_movie_titles():
    data = cr.prepare_data()
    movie_features_df = cr.create_rating_metrix(data)
    size = movie_features_df.shape[0]
    movies = []
    for i in range(0, size):
        movies.append(movie_features_df.index[i])
    return movies

def get_all_movie_titles1():
    df = con.load_filter_data()
    df = df['title'].to_list()
    df = sorted(df)
    return df


def get_movie_index_by_title(title):
    return get_all_movie_titles().index(title)

def get_id_by_title(title):
    # df = prepare_movie_data()
    df = cr.prepare_data()
    df = df[df['title'] == title]
    id = df['id']
    return id


def get_imdb_id_by_title(title):
    df = pd.read_csv("data/movies_metadata.csv")
    # df = cr.prepare_data()
    try:
        df = df[df['title'] == title]
        imdb_id = df['imdb_id'].values[0] # remember ...
    except:
        imdb_id = -1
    return imdb_id