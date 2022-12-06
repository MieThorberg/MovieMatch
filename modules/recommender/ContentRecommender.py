import pandas as pd
import ast

ast.literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_movies():
    movies_df = pd.read_csv("data/10000 Movies Data")
    return movies_df


def load_credits():
    credits_df = pd.read_csv('data/10000 Credits Data.zip')
    return credits_df


def prepare_credits(credits_df):
    credits_df = credits_df.drop("title", axis=1)
    return credits_df


def prepare_data():
    df = prepare_df_data()
    df = convert_data(df)
    df = generate_tags(df)
    return df


def prepare_df_data():
    movies_df = load_movies()
    credits_df = prepare_credits(load_credits())
    df = merge_movies_and_credits(movies_df, credits_df)
    df = df[['Movie_id', 'title', 'Genres', "Keywords", 'overview', 'Cast', 'Crew']]
    df.dropna(inplace=True)
    return df


def merge_movies_and_credits(movies_df, credits_df):
    return pd.merge(movies_df, credits_df, on='Movie_id')


def convert_data(df):
    # traverse through the abstract syntax tree and converts to a list of words
    df['Genres'] = df['Genres'].apply(convert_all)
    df['Keywords'] = df['Keywords'].apply(convert_all)
    df['Cast'] = df['Cast'].apply(convert_first_three)
    df['Crew'] = df['Crew'].apply(convert_director)
    # change the text format
    df['overview'] = split_text(df, 'overview')
    df['Genres'] = remove_spaces(df, 'Genres')
    df['Keywords'] = remove_spaces(df, 'Keywords')
    df['Cast'] = remove_spaces(df, 'Cast')
    df['Crew'] = remove_spaces(df, 'Crew')
    return df


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


def generate_tags(df):
    df['tags'] = df['Genres'] + df['Keywords'] + df['Cast'] + df['Crew'] + df['overview']
    df['tags'] = df['tags'].apply(lambda x: " ".join(x))
    df['tags'] = df['tags'].apply(lambda x: x.lower())
    return df


def create_matrix_of_tag_words(df):
    # Using CountVectorizer to convert each word in the tag into vectors
    # each word from all tags are represented by a column of the matrix
    # each tag from every movie is represented by the row of the matrix

    # the value in the matrix turns into a binary vector of size
    CV = CountVectorizer(max_features=8000,  # the most frequently words
                         stop_words="english"  # only english words
                         )
    # fit and transform
    vector = CV.fit_transform(df['tags']).toarray()
    return vector


def find_similarities(vector):
    similarity = cosine_similarity(vector)
    return similarity


def recommend_movies(title, recommend_size):
    df = prepare_data()
    vector = create_matrix_of_tag_words(df)
    similarity = find_similarities(vector)
    movie_index = df[df['title'] == title].index[0]

    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:recommend_size + 1]
    _list = []
    for i in movies_list:
        _list.append(df.iloc[i[0]].title)
    return _list


def get_movie_index_by_title(df, title):
    return df[df['title'] == title].index[0]


def get_all_movie_titles():
    df = prepare_df_data()
    df = df['title'].to_list()
    df = sorted(df)
    return df