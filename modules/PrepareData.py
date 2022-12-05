import pandas as pd


# gets the imdb id from the big movie dataset
def get_imdb_id_by_title(title):
    df = pd.read_csv("data/movies_metadata.csv")
    try:
        df = df[df['title'] == title]
        imdb_id = df['imdb_id'].values[0]
    except:
        imdb_id = -1  # if the movie does not exist or have no imdb id
    return imdb_id