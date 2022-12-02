import requests as rq
from bs4 import BeautifulSoup
import re


# Webscraping from imdb.
# See website: https://www.imdb.com


def get_imdb_url(imdb_id):
    return "https://www.imdb.com/title/" + imdb_id


def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
    }
    data = rq.get(url, headers=headers).text
    soup = BeautifulSoup(data, "html.parser")
    return soup


# returns a list with one short and one detailed movie summary,
def get_summaries(imdb_id):
    url = get_imdb_url(imdb_id) + "/plotsummary"
    try:
        # first p element contains a shorter summary than the rest p's
        summaries = get_soup(url).find("ul", {"class": "ipl-zebra-list"}).findAll("p")[:2]
    except:
        # some movies have only the one short summary registered at imdb
        summaries = get_soup(url).find("ul", {"class": "ipl-zebra-list"}).findAll("p")[:1]
    return summaries


def get_poster(imdb_id):
    url = get_imdb_url(imdb_id)
    poster = get_soup(url).find("img", {"class": "ipc-image"}).get("src")
    return poster


def get_trailer(imdb_id):
    url = get_imdb_url(imdb_id)
    try:
        trailer = get_soup(url).find("a", {"data-testid": "videos-slate-overlay-1"}).attrs["href"]
        trailer = "https://www.imdb.com" + trailer
    except:
        # some movies have no trailer registered at imdb
        trailer = ""

    return trailer


def get_genres(imdb_id):
    url = get_imdb_url(imdb_id)
    a_list = get_soup(url).find("div", {"class", "ipc-chip-list__scroller"}).findAll("a", {
        "class": "sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt"})
    genres = []
    # use regex to get genre from an url
    # url example: "/search/title?genres=adventure&amp;explore=title_type,genres&amp;ref_=tt_ov_inf"
    genre_reg = re.compile(r'(?<=genres=)(\w*)')
    for a in a_list:
        url = a.attrs["href"]
        genre = genre_reg.search(url)
        genres.append(genre.group())
    return genres


def get_rating(imdb_id):
    url = get_imdb_url(imdb_id)
    rating = get_soup(url).find("span", {"class":"sc-7ab21ed2-1 jGRxWM"})
    return rating.text
