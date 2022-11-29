import requests as rq
from bs4 import BeautifulSoup


def get_imdb_url(imdb_id):
    return "https://www.imdb.com/title/" + imdb_id


def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
    }
    data = rq.get(url, headers=headers).text
    soup = BeautifulSoup(data, "html.parser")
    return soup


# returns a list with one short and one detailed movie summary
def get_summaries(imdb_id):
    url = get_imdb_url(imdb_id) + "/plotsummary"
    # first p element contains a shorter summary than the rest p's
    summaries = get_soup(url).find("ul", {"class": "ipl-zebra-list"}).findAll("p")[:2]
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
        trailer = ""

    return trailer
