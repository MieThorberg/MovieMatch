import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.linear_model as sk
from ast import literal_eval


def prepare_data():
    data = pd.read_csv("data/movies_metadata.csv")
    data = data[
        ['budget', 'genres', 'id', 'original_title', 'popularity', 'release_date', 'revenue', 'runtime',
         'vote_average', 'vote_count', 'original_language', 'production_companies']]

    data.dropna(inplace=True)
    data['production_companies'] = data['production_companies'].apply(convert)
    data['genres'] = data['genres'].apply(convert)

    # converts string to python readable date
    data['release_date'] = pd.to_datetime(data['release_date'])
    # extracts the year
    data['years'] = data['release_date'].dt.year
    # removes all 0 values
    data = data[(data.T != 0).all()]

    data['profit'] = data['revenue'] - data['budget']
    return data


def convert(obj):
    # return only the first words
    for i in literal_eval(obj):
        return i['name']


def linear_regression_func(df, feat1, feat2):
    reg = sk.LinearRegression()
    reg.fit(df[[feat1]], df[feat2])
    plt.scatter(df[[feat1]], df[feat2], marker="+", color="red")
    plt.plot(df[[feat1]], reg.predict(df[[feat1]]), color="blue", linewidth=3)  # line
    plt.xlabel(feat1)
    plt.ylabel(feat2)
    plt.show()


def revenue_predict(df, feat1, feat2, budget):
    reg = sk.LinearRegression()
    reg.fit(df[[feat1]], df[feat2])
    # coefficient array
    coe = reg.coef_[0]
    # constant
    intercept = reg.intercept_
    revenue = coe * budget + intercept
    return revenue


def correlator(df, feat1, feat2):
    # correlation between the features from -1 to 1
    data_corr = df.corr()
    return print(f"Correlation between {feat1} and {feat2}  is: ", data_corr.loc[feat1, feat2])


def average_revenue_by_month(df):
    # Bar plot
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    month_release = df['release_date'].dt.month

    month_release = pd.DataFrame(month_release)
    month_release.rename(columns={'release_date': 'release_month'}, inplace=True)  # doesnt copy frame
    month_release['revenue'] = df['revenue']
    mean_revenue = month_release.groupby('release_month').mean()
    mean_revenue['month'] = months

    mean_revenue.plot(x='month', kind='bar', figsize=(8, 6), fontsize=11)

    plt.title('Average revenue by month (1915 - 2017)', fontsize=15)
    plt.xlabel('Month', fontsize=13)
    plt.ylabel('Average Revenue', fontsize=13)


def plot_correlation_map(df):
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(12, 10))  # controls size of the plot
    # colour palette
    cmap = sns.diverging_palette(240, 10)
    # cbar is the colour bar on the right
    fig = sns.heatmap(corr, cmap=cmap, square=True, cbar_kws={'shrink': .9}, ax=ax, annot=True,
                    annot_kws={'fontsize': 12})


def count(df, feat):
    # used for counting genres
    genres = df[feat]
    data = pd.Series(genres)
    count = data.value_counts(ascending=False)
    return count


def plot_genre(df, feat):
    # creates bar plot
    _count = count(df, feat)
    print(_count)
    plt.title(f'{feat} (1915 - 2017)', fontsize=15)
    plt.xlabel(feat, fontsize=13)
    plt.ylabel('Amount of Movies', fontsize=13)
    _count.plot(kind="bar")


def plot_production_company(df):
    # bar plot horizontal
    # Create New Dataset for Countries
    dfmovies_companies = pd.DataFrame(columns=['production_companies', 'movies'])

    dfmovies_companies['production_companies'] = df['production_companies']  # Add Data from list to name column
    print('Shape:', dfmovies_companies.shape)

    # agg 'size' counts the movies. reset.index() because movie and production index are different
    dfmovies_companies = dfmovies_companies.groupby('production_companies').agg({'movies': 'size'})\
        .reset_index().sort_values('movies', ascending=False)

    print(dfmovies_companies.head())

    dfmovies_companies.set_index('production_companies').iloc[:20].plot(kind='barh', figsize=(16, 8), fontsize=13)
    plt.title("Production Companies Vs Number Of Movies", fontsize=15)
    plt.xlabel('Number Of Movies', fontsize=14)


def plot_average_revenue_by_genre(df):
    # bar plot
    genres = df['genres']
    genres = pd.DataFrame(genres)
    genres['revenue'] = df['revenue']
    mean_revenue = genres.groupby('genres').mean()
    mean_revenue = mean_revenue.sort_values(by=['revenue'], ascending=False)
    mean_revenue.iloc[:20].plot(kind='bar', figsize=(16, 8), fontsize=13)

    plt.title('Average revenue by genre', fontsize=15)
    plt.xlabel('Genre', fontsize=13)
    plt.ylabel('Average Revenue', fontsize=13)


def average_revenue_by_genre(df):
    # table
    genres = df['genres']
    genres = pd.DataFrame(genres)
    genres['revenue'] = df['revenue']
    mean_revenue = genres.groupby('genres').mean()
    mean_revenue = mean_revenue.sort_values(by=['revenue'], ascending=False)
    return mean_revenue


def plot_average_ratings_by_genre(df):
    # bar plot horizontal
    genres = df['genres']
    genres = pd.DataFrame(genres)
    genres['vote_average'] = df['vote_average']
    mean_rating = genres.groupby('genres').mean()
    mean_rating.plot(kind='barh', figsize=(16, 8), fontsize=13)
    plt.title('Average IMDB rating by genre', fontsize=15)
    plt.xlabel('Average IMDB rating', fontsize=13)
    plt.ylabel('Genre', fontsize=13)


def plot_average_revenue_by_prod(df):
    # bar plot horizontal
    prod = df['production_companies']
    prod = pd.DataFrame(prod)
    prod['revenue'] = df['revenue']
    mean_revenue = prod.groupby('production_companies').mean()
    mean_revenue = mean_revenue.sort_values(by=['revenue'], ascending=False)
    mean_revenue.iloc[:20].plot(kind='barh', figsize=(16, 8), fontsize=13)

    plt.title('Average revenue by production_companies', fontsize=15)
    plt.xlabel('Average Revenue', fontsize=13)
    plt.ylabel('production_companies', fontsize=13)


def plot_vote_average_by_years(df, year1, year2):
    # line plot
    plt.figure(figsize=(10, 6))
    df[(df['years'] < year2) & (df['years'] >= year1)].groupby(by='years').mean()['vote_average'].plot()
    plt.ylabel("Vote Average", fontsize=13)
    plt.xlabel("Years", fontsize=13)

    plt.title(f"Vote Average | {year1}-{year2}", fontsize=13)



