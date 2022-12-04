import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.linear_model as sk
from ast import literal_eval


def prepare_data():
    data = pd.read_csv("data/movies_metadata.csv")
    data = data[
        ['budget', 'genres', 'id', 'imdb_id', 'original_title', 'popularity', 'release_date', 'revenue', 'runtime',
         'vote_average', 'vote_count', 'original_language', 'production_companies']]
    data = data[(data['genres'] != "[]")]
    data['genres'] = data['genres'].fillna('[]').apply(convert_all)
    data['production_companies'] = data['production_companies'].fillna('[]').apply(convert_all)
    data['release_date'] = pd.to_datetime(data['release_date'])
    data['years'] = data['release_date'].dt.year
    data.dropna(inplace=True)
    data = data[(data.T != 0).all()]
    data['profit'] = data['revenue'] - data['budget']
    return data

def convert_all(obj):
    L = []
    # return all words
    for i in literal_eval(obj):
        L.append(i['name'])
    return L

def linear_regression_func(df, feat1, feat2):
    reg = sk.LinearRegression()
    reg.fit(df[[feat1]], df[feat2])
    plt.scatter(df[[feat1]], df[feat2], marker="+", color="red")
    plt.plot(df[[feat1]], reg.predict(df[[feat1]]), color="blue", linewidth=3)  # line
    plt.xlabel(feat1)
    plt.ylabel(feat2)
    plt.show()

def revenue_predict(df,feat1,feat2,budget):
    reg = sk.LinearRegression()
    reg.fit(df[[feat1]], df[feat2])
    coe = reg.coef_[0]
    interce = reg.intercept_
    revenue = coe * budget + interce
    return revenue

def correlator(df, feat1, feat2):
    data_corr = df.corr()
    return print(f"Correlation between {feat1} and {feat2}  is: ", data_corr.loc[feat1, feat2])

def average_revenue_by_month(df):
    # change string format to datetime format
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    df['release_date'].head()

    month_release = df['release_date'].dt.month

    month_release = pd.DataFrame(month_release)
    month_release.rename(columns={'release_date': 'release_month'}, inplace=True)
    month_release['revenue'] = df['revenue']
    mean_revenue = month_release.groupby('release_month').mean()
    mean_revenue['month'] = months

    mean_revenue.plot(x='month', kind='bar', figsize=(8, 6), fontsize=11)

    plt.title('Average revenue by month (1915 - 2017)', fontsize=15)
    plt.xlabel('Month', fontsize=13)
    plt.ylabel('Average Revenue', fontsize=13)
    sns.set_style("darkgrid")

def plot_correlation_map( df ):
    corr = df.corr()
    _ , ax = plt.subplots( figsize = ( 12 , 10 ) )
    cmap = sns.diverging_palette( 240 , 10 )
    _ = sns.heatmap(corr,cmap = cmap,square=True, cbar_kws={ 'shrink' : .9 }, ax=ax, annot = True, annot_kws = { 'fontsize' : 12 })

def count(df, feat):
    genres = df[feat].str[0]
    data = pd.Series(genres)
    count = data.value_counts(ascending=False)
    return count

def plot_genre(df, feat):

    count1 = count(df,feat)
    plt.title(f'{feat} (1915 - 2017)', fontsize=15)
    plt.xlabel(feat, fontsize=13)
    plt.ylabel('Amount of Movies', fontsize=13)
    count1.plot(kind="bar")

def plot_genre_pie(df,feat):
    total_genre_movies = count(df,feat)
    i = 0
    genre_count = []
    for genre in total_genre_movies.index:
        genre_count.append([genre, total_genre_movies[i]])
        i = i + 1

    plt.rc('font', weight='bold')
    fig, ax = plt.subplots(figsize=(10, 10))
    genre_count.sort(key=lambda x: x[1], reverse=True)
    labels, sizes = zip(*genre_count)
    labels_selected = [n if v > sum(sizes) * 0.01 else '' for n, v in genre_count]
    ax.pie(sizes, labels=labels_selected,
           autopct=lambda x: '{:2.0f}%'.format(x) if x > 1 else '',
           shadow=False, startangle=0)
    ax.axis('equal')
    plt.tight_layout()


def plot_production_company(df):
    #getlist_companies = getDataList(df, 'production_companies')
    # Create New Dataset for Countries
    dfmovies_companies = pd.DataFrame(columns=['production_companies', 'movies'])

    dfmovies_companies['production_companies'] = df['production_companies'].str[0]  # Add Data from list to name column
    print('Shape:',dfmovies_companies.shape)
    dfmovies_companies = dfmovies_companies.groupby('production_companies').agg({'movies': 'size'}).reset_index().sort_values('movies',ascending=False)
    print(dfmovies_companies.head())

    dfmovies_companies.set_index('production_companies').iloc[:20].plot(kind='barh', figsize=(16, 8), fontsize=13)
    plt.title("Production Companies Vs Number Of Movies", fontsize=15)
    plt.xlabel('Number Of Movies', fontsize=14)
    sns.set_style("whitegrid")

def plot_average_revenue_by_genre(df):
    genres = df['genres'].str[0]
    genres = pd.DataFrame(genres)
    genres['revenue'] = df['revenue']
    mean_revenue = genres.groupby('genres').mean()
    mean_revenue = mean_revenue.sort_values(by=['revenue'], ascending=False)
    mean_revenue.iloc[:20].plot(kind='bar', figsize=(16, 8), fontsize=13)
    # mean_revenue.plot(kind='barh',figsize = (8,6),fontsize=11)
    #
    plt.title('Average revenue by genre', fontsize=15)
    plt.xlabel('Genre', fontsize=13)
    plt.ylabel('Average Revenue', fontsize=13)
    sns.set_style("darkgrid")

def average_revenue_by_genre(df):
    genres = df['genres'].str[0]
    genres = pd.DataFrame(genres)
    genres['revenue'] = df['revenue']
    mean_revenue = genres.groupby('genres').mean()
    mean_revenue = mean_revenue.sort_values(by=['revenue'], ascending=False)
    return mean_revenue
def plot_average_ratings_by_genre(df):
    genres = df['genres'].str[0]
    genres = pd.DataFrame(genres)
    genres['vote_average'] = df['vote_average']
    mean_rating = genres.groupby('genres').mean()
    mean_rating.plot(kind='barh', figsize=(16, 8), fontsize=13)
    plt.title('Average IMDB rating by genre', fontsize=15)
    plt.xlabel('Average IMDB rating', fontsize=13)
    plt.ylabel('Genre', fontsize=13)
    sns.set_style("darkgrid")

def plot_average_revenue_by_prod(df):
    prod = df['production_companies'].str[0]
    prod = pd.DataFrame(prod)
    prod['revenue'] = df['revenue']
    mean_revenue = prod.groupby('production_companies').mean()
    mean_revenue = mean_revenue.sort_values(by=['revenue'], ascending=False)
    mean_revenue.iloc[:20].plot(kind='barh', figsize=(16, 8),fontsize=13)
    # mean_revenue.plot(kind='barh',figsize = (8,6),fontsize=11)
    #
    plt.title('Average revenue by production_companies', fontsize=15)
    plt.xlabel('Average Revenue', fontsize=13)
    plt.ylabel('production_companies', fontsize=13)
    sns.set_style("darkgrid")

def plot_vote_average_by_years(df,year1, year2):
    plt.figure(figsize=(10, 6))
    df[(df['years'] < year2) & (df['years'] >= year1)].groupby(by='years').mean()['vote_average'].plot();
    plt.ylabel("Vote Average", fontsize=13)
    plt.xlabel("Years", fontsize=13)

    plt.title(f"Vote Average | {year1}-{year2}", fontsize=13);

def plot_distribution(df, feat1,feat2):
    # there's a long tail in the distribution, so let's put it on a log scale instead
    # log_binsize = 0.025
    log_binsize = 0.09

    budget_bins = 10 ** np.arange(2.4, np.log10(df[feat1].max()) + log_binsize, log_binsize)
    revenue_bins = 10 ** np.arange(2.4, np.log10(df[feat2].max()) + log_binsize, log_binsize)

    # plt.figure(figsize=[8, 5])
    plt.figure(figsize=[11.69, 8.27])
    plt.hist(data=df, x=feat1, bins=budget_bins, alpha=0.5)
    plt.hist(data=df, x=feat2, bins=revenue_bins, alpha=0.5)

    plt.xscale('log')
    # plt.xticks([500, 1e3, 2e3, 5e3, 1e4, 2e4], [500, '1k', '2k', '5k', '10k', '20k'])
    # plt.xticks([500, 10^3, 10^4, 10^5, 10^6, 10^8], [500, '1k', '10k', '1M', '10M', '10B'])

    plt.xlabel(f'{feat1} ($)', fontsize=13)
    plt.ylabel('Frequency', fontsize=13)

    plt.title('Budget & Revenue Distributions', fontsize=13)
    plt.legend([feat1, feat2])
    plt.show()