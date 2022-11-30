import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast
ast.literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_movies():
    movies = pd.read_csv("data/10000 Movies Data")
    return movies

def load_credits():
    movie_credits = pd.read_csv('data/10000 Credits Data.zip')
    return movie_credits

def prepare_credits(movie_credits):
    movie_credits = movie_credits.drop("title", axis=1)
    return movie_credits

def merge_credits(movies, movie_credits):
    movies = movies.merge(movie_credits, on='Movie_id')
    return movies

def convert(obj):
    L =[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

def convert3(obj):
    L =[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter !=3:
            L.append(i['name'])
            counter+=1
    return L

def fetch_directoer(obj):
    L =[]
    for i in ast.literal_eval(obj):
        if i['job']=="Director":
            L.append(i['name'])
            break
    return L



def convert_movie_data(movies):
    movies['Genres'] = movies['Genres'].apply(convert)
    movies['Keywords'] = movies['Keywords'].apply(convert)
    movies['Cast'] = movies['Cast'].apply(convert3)
    movies['Crew'] = movies['Crew'].apply(fetch_directoer)
    movies['overview'] = movies['overview'].apply(lambda x: x.split())
    movies['Genres'] = movies['Genres'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['Keywords'] = movies['Keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['Cast'] = movies['Cast'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['Crew'] = movies['Crew'].apply(lambda x: [i.replace(" ", "") for i in x])
    return movies

def load_filter_data():
    movies = load_movies()
    movie_credits = prepare_credits(load_credits())
    movies = merge_credits(movies, movie_credits)
    movies = movies[['Movie_id', 'title', 'Genres', "Keywords", 'overview', 'Cast', 'Crew']]
    movies.dropna(inplace=True)

    return movies

def prepare_movies():
    movies = load_filter_data()

    # movies.duplicated().sum()
    movies = convert_movie_data(movies)

    movies['tags'] = movies['Genres'] + movies['Keywords'] + movies['Cast'] + movies['Crew'] + movies['overview']

    movies = movies[['Movie_id', 'title', 'tags']]
    movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))
    movies['tags'] = movies['tags'].apply(lambda x: x.lower())
    return movies


def create_matrix(movies):
    CV = CountVectorizer(max_features=8000, stop_words="english")
    vector = CV.fit_transform(movies['tags']).toarray()
    return vector


def find_similarities(vector):
    similarity = cosine_similarity(vector)
    return similarity


def recommend_movies(title, recommend_size):
    movies = prepare_movies()
    vector = create_matrix(movies)
    similarity = find_similarities(vector)
    movie_index = movies[movies['title'] == title].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:recommend_size]
    _list = []
    for i in movies_list:
        _list.append(movies.iloc[i[0]].title)
    return _list
