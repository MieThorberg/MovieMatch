import pandas as pd
import ast

ast.literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_movies():
    movie_df = pd.read_csv("data/10000 Movies Data")
    return movie_df


def load_credits():
    movie_credits = pd.read_csv('data/10000 Credits Data.zip')
    return movie_credits


def prepare_credits(movie_credits):
    movie_credits = movie_credits.drop("title", axis=1)
    return movie_credits


def prepare_movies():
    movies = load_filter_data()
    movies = convert_movie_data(movies)
    movies = generate_tags(movies)
    # movies['tags'] = movies['Genres'] + movies['Keywords'] + movies['Cast'] + movies['Crew'] + movies['overview']
    #
    # movies = movies[['Movie_id', 'title', 'tags']]
    # movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))
    # movies['tags'] = movies['tags'].apply(lambda x: x.lower())
    return movies


def merge_movie_and_credits(movies, movie_credits):
    movies = movies.merge(movie_credits, on='Movie_id')
    return movies


def convert_all(obj):
    L = []
    # return all words
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L


def convert_first_three(obj):
    L = []
    counter = 0
    # return only the first three words
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
    return L


def convert_director(obj):
    L = []
    # return only the director
    for i in ast.literal_eval(obj):
        if i['job'] == "Director":
            L.append(i['name'])
            break
    return L


def remove_spaces(df, column_name):
    return df[column_name].apply(lambda x: [i.replace(" ", "") for i in x])


def split_text(df, column_name):
    return df[column_name].apply(lambda x: x.split())


def convert_movie_data(movies):
    # traverse through the abstract syntax tree and converts the distance
    movies['Genres'] = movies['Genres'].apply(convert_all)
    movies['Keywords'] = movies['Keywords'].apply(convert_all)
    movies['Cast'] = movies['Cast'].apply(convert_first_three)
    movies['Crew'] = movies['Crew'].apply(convert_director)
    # change the text format
    movies['overview'] = split_text(movies, 'overview')
    movies['Genres'] = remove_spaces(movies, 'Genres')
    movies['Keywords'] = remove_spaces(movies, 'Keywords')
    movies['Cast'] = remove_spaces(movies, 'Cast')
    movies['Crew'] = remove_spaces(movies, 'Crew')
    return movies


def load_filter_data():
    movies = load_movies()
    movie_credits = prepare_credits(load_credits())
    movies = merge_movie_and_credits(movies, movie_credits)
    movies = movies[['Movie_id', 'title', 'Genres', "Keywords", 'overview', 'Cast', 'Crew']]
    movies.dropna(inplace=True)
    return movies


def generate_tags(movie_df):
    movie_df['tags'] = movie_df['Genres'] + movie_df['Keywords'] + movie_df['Cast'] + movie_df['Crew'] + movie_df['overview']
    movie_df['tags'] = movie_df['tags'].apply(lambda x: " ".join(x))
    movie_df['tags'] = movie_df['tags'].apply(lambda x: x.lower())
    return movie_df


def create_matrix_of_tag_words(movie_df):
    # Using CountVectorizer to convert each word in the tag into vectors
    # each word from all tags are represented by a column of the matrix
    # each tag from every movie is represented by the row of the matrix

    # one-hot encoding
    # Associate to a unique integer index to every word
    # the value in the matrix turns into a binary vector of size
    CV = CountVectorizer(max_features=8000,  # the most frequently words
                         stop_words="english"  # only english words
                         )
    # fit and transform
    vector = CV.fit_transform(movie_df['tags']).toarray()
    return vector


def find_similarities(vector):
    similarity = cosine_similarity(vector)
    return similarity


def recommend_movies(title, recommend_size):
    movies = prepare_movies()
    vector = create_matrix_of_tag_words(movies)
    similarity = find_similarities(vector)
    movie_index = movies[movies['title'] == title].index[0]

    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:recommend_size + 1]
    _list = []
    for i in movies_list:
        _list.append(movies.iloc[i[0]].title)
    return _list
