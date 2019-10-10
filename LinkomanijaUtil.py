import requests
import re
from bs4 import BeautifulSoup
import BeautifulSoupExtensions as bs
from termcolor import colored as c

initial_url = "https://www.linkomanija.net/login.php"
login_url = "https://www.linkomanija.net/takelogin.php"

session = requests.session()

logged_in = False


def login():
    username = input("Username:")
    password = input("Password:")

    login_data = {
        "username": username,
        "password": password,
        "commit": "Prisijungti"
    }

    login_result = session.post(login_url, data=login_data)

    global logged_in
    logged_in = username in login_result.text
    print("\nLogged in:", logged_in)


def get_page_titles(page):
    soup = BeautifulSoup(page.text.encode("utf-8"), "html.parser")
    title_nodes = soup.find_all(lambda x: x.name == "a"
                                and bs.href_contains(x, "details?"))

    result = list()

    for n in title_nodes:
        text_node = n.find("b")
        if text_node:
            result.append(text_node.text)

    return result


def get_page(main_url, page):
    page_url = main_url + "&page=" + str(page)
    print(c("Linkomanija getting page ", "blue"), page_url)
    return session.get(page_url)


def get_titles(main_url, page_count, start_from=None):
    global logged_in
    if logged_in is False:
        login()

    titles = list()

    start = 1

    if start_from is not None:
        start = start_from + 1

    for i in range(start, page_count + start):
        page = get_page(main_url, i-1)
        page_titles = get_page_titles(page)
        titles = titles + page_titles

    cleaned_up_titles = clean_up_tv_show_titles(titles)

    return list(dict.fromkeys(cleaned_up_titles))


def clean_up_tv_show_titles(titles):
    result = list()

    for t in titles:
        season_episode_match = re.search("S\\d+E\\d+", t)
        if season_episode_match:
            result.append(t[0:season_episode_match.start()].strip())

    return result
