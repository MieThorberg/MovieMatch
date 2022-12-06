import pandas as pd
import matplotlib.pyplot as plt
from ast import literal_eval
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot, plot
init_notebook_mode(connected=True)
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


def __load_data():
    data = pd.read_csv("data/movies_metadata.csv")
    return data


def __convert_all(obj):
    L = []
    # return all words
    for i in literal_eval(obj):
        L.append(i['name'])
    return L


def __prepare_data(data):
    data = data[data['original_language'] == 'en']
    data = data[['budget', 'genres', 'id', 'imdb_id', 'original_title', "title", 'popularity', 'release_date',
                'revenue', 'runtime', 'vote_average', 'vote_count']]
    data = data[(data['genres'] != "[]")]
    data['genres'] = data['genres'].apply(__convert_all)
    data = data[(data.T != 0).all()]
    return data


def __scale_data(data):
    scalar = MinMaxScaler()
    scaled_df = data[['budget', 'popularity', 'revenue', 'runtime', 'vote_average', 'vote_count']]
    # change value to be readable for clustering
    scaled = scalar.fit_transform(data[['budget', 'popularity', 'revenue', 'runtime', 'vote_average', 'vote_count']])

    scaled_df = pd.DataFrame(scaled, index=scaled_df.index, columns=scaled_df.columns)
    return scaled_df


def __apply_kmeans(df, clusters):
    kmeans = KMeans(n_clusters=clusters)
    cluster_labels = kmeans.fit(df).labels_
    string_labels = ["c{}".format(i) for i in cluster_labels]
    df['cluster_label'] = cluster_labels
    df['cluster_string'] = string_labels

    return df


# def __elbow_diagram(df):
#     scores = {'clusters': list(), 'score': list()}
#     for cluster_num in range(1,31):
#         scores['clusters'].append(cluster_num)
#         scores['score'].append(KMeans(n_clusters=cluster_num, random_state=0).fit(df).score(df))
#
#     scores_df = pd.DataFrame(scores)
#
#     fig = go.Figure(go.Scatter(
#         x=scores_df['clusters'],
#         y=scores_df['score']
#     ))
#
#     fig.update_layout(
#         xaxis_title='Cluster',
#         yaxis_title='Score',
#         title='Elbow Method Results',
#         height=800,
#         width=800
#     )
#
#     fig.show()


def __create_clusters(data, small, clusters):
    scaled_df = __apply_kmeans(data, clusters)
    small = small.join(scaled_df[['cluster_label', 'cluster_string']])
    return small


def __create_scatter(data):
    fig = px.scatter_matrix(data, dimensions=['budget', 'popularity', 'revenue', 'runtime', 'vote_average', 'vote_count'],
                        color='cluster_string', hover_data=['title', 'genres'])
    fig.update_layout(
       title='Cluster Scatter Matrix',
        height=1000,
       width=800
    )

    iplot(fig)


# def make_elbow_digram():
#     data = __load_data()
#     data = __prepare_data(data)
#     data = __scale_data(data)
#
#     __elbow_diagram(data)


def make_Cluster_metrix(clusters):
    data = __load_data()
    data = __prepare_data(data)
    small = data.copy()
    data = __scale_data(data)

    cluster_data = __create_clusters(data,small,clusters)
    __create_scatter(cluster_data)
