import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def __get_movie_data():
    data = pd.read_csv("data/movies_metadata.csv")
    return data

def __prepare_data(data,col1,col2):
    data = data[["title",col1,col2]]
    data.dropna(inplace=True)
    df = data[(data.T != 0).all()]

    return df

def __data_scaler(df):
    scaler = StandardScaler()
    df[["{df.columns[1]}_t","{df.columns[2]}_t"]] = scaler.fit_transform(df[[df.columns[1],df.columns[2]]])
    return df

def __optimise_k_means(data, max_k):
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

def __create_cluster(clusters,df):
    kmeans = KMeans(n_clusters=clusters)
    kmeans.fit(df[[df.columns[3],df.columns[4]]])
    df["clusters"] = kmeans.labels_
    return df

def __create_scatter(df):
    fig = plt.scatter(x=df[df.columns[3]],y=df[df.columns[4]],c=df["clusters"])
    plt.xlabel(df.columns[1])
    plt.ylabel(df.columns[2])
    plt.legend(*fig.legend_elements(), title='clusters')
    plt.show()


def create_cluster_scatter(col1="vote_average",col2="revenue",clusters=3):
    df = __get_movie_data()
    df = __prepare_data(df,col1,col2)
    df = __data_scaler(df)
    df = __create_cluster(clusters,df)
    __create_scatter(df)

    return df

def get_elbow_diagram(col1="vote_average",col2="revenue",max_clusters=10):
    df = __get_movie_data()
    df = __prepare_data(df,col1,col2)
    __optimise_k_means(df,max_clusters)



