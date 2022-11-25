import pandas as pd
import matplotlib.pyplot as plt
from ast import literal_eval


def prepare_movie_data():
    data = pd.read_csv("data/movies_metadata.csv")
    # data = data[data['original_language']=='en']
    data = data[['budget', 'genres','id', 'imdb_id','title', 'popularity', 'release_date', 'revenue', 'runtime', 'vote_average', 'vote_count']]
    data = data[(data['genres'] != "[]")]
    data['genres'] = data['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    data = data[(data.T != 0).all()]
    return data


def get_all_movie_titles():
    df = prepare_movie_data()
    titles = df['title'].tolist()
    return titles

def get_id_by_title(title):
    df = prepare_movie_data()
    df = df[df['title'] == title]
    id = df['id']
    return id

def get_imdb_id_by_title(title):
    df = prepare_movie_data()
    df = df[df['title'] == title]
    imdb_id = df['imdb_id']
    return imdb_id