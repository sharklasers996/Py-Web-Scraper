import ImdbUtil as imdb
import LinkomanijaUtil as lm
from termcolor import colored as c

# run get_tvshows(page_count, start_from=1) to get titles from tvshows_url
# then run tvshow_imdb_search() to get info for earch title

# TV and TV HD categories
tvshows_url = "https://www.linkomanija.net/browse.php?c30=1&c60=1&incldead=0&search="

tvshow_titles = list()
last_page = 1


def get_tvshows(page_count, start_from):
    global tvshow_titles
    tvshow_titles = lm.get_titles(tvshows_url, page_count, start_from)
    print(F"Got {len(tvshow_titles)} titles")

    global last_page
    last_page = page_count + start_from


def tvshow_imdb_search():
    for t in tvshow_titles:
        title_url = imdb.perform_search(t)

        if bool(title_url):
            print(c("IMDb getting info for", "yellow") + f" \"{t}\"\n")
            imdb.get_tv_show_info(title_url)
