import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from termcolor import colored as c
from unidecode import unidecode
import BeautifulSoupExtensions as bs

headers = {
    "Accept-Language": "en-US,en;q=0.5"
}


def perform_search(title):
    """ Performs search for 'title'
    and tries to match results to 'title'
    returns url of best match
    """
    print(c("IMDb searching for", "yellow") + f" \"{title}\"")

    title_encoded = title.replace(" ", "+")

    search_page = requests.get(f"https://www.imdb.com/find?ref_=nv_sr_fn&q={title_encoded} \
    &s=all", headers=headers)

    soup = BeautifulSoup(search_page.text, "html.parser")
    title_nodes = soup.find_all("td", class_="result_text")

    print(F"Found {len(title_nodes)} results\n")

    best_match = 0
    best_match_title = ""
    best_match_url = ""

    for n in title_nodes:
        node = next(iter(n.select("a[href*='title']")), None)

        if node:
            title_text = unidecode(node.text)
            match_ratio = fuzz.token_set_ratio(title, title_text)

            print(c(F"Matching ", "magenta")
                  + F"\"{title_text}\" = "
                  + c(F"{match_ratio}", "green"))

            if match_ratio > best_match:
                best_match = match_ratio
                best_match_title = title_text
                best_match_url = node["href"]

    print(c("\nBest Match", "green") + f" {best_match_title}\n")

    return "https://imdb.com" + best_match_url


def get_tv_show_info(url):
    tv_show_page = requests.get(url, headers=headers)

    soup = BeautifulSoup(tv_show_page.text, "html.parser")

    rating_node = bs.first_node_or_none(
        soup.find_all("span", attrs={"itemprop": "ratingValue"}))

    title_node = bs.first_node_or_none(soup.find_all("h1"))

    subtext_node = bs.first_node_or_none(soup.find_all("div",
                                                       class_="subtext"))

    if subtext_node:
        genre_nodes = subtext_node.find_all(lambda x: x.name == "a"
                                            and bs.href_contains(x, "genres="))

        release_dates_node = subtext_node("a")[-1]

        print(F"{c(bs.try_get_text(title_node).strip(), 'yellow', attrs=['bold'])}", end=" ")
        print(F"({c(bs.try_get_text(rating_node), 'green')})", end=" ")
        print(c(" | ".join(bs.try_get_text_from_nodes(genre_nodes)), 'blue'))

        release_dates = bs.try_get_text(release_dates_node)
        release_dates = release_dates.replace("TV Series", "") \
                                     .replace("(", "") \
                                     .replace(")", "")
        print("Releases: ", unidecode(release_dates).strip())

        duration_node = subtext_node("time")[0:1]
        print("Duration: ", bs.try_get_text(duration_node))

    actors_node = soup.select("div.credit_summary_item:nth-child(3) > a")
    if not actors_node:
        actors_node = soup.select(".credit_summary_item > a")

    print("Actors: ", ", ".join(bs.try_get_text_from_nodes(actors_node[0:-1])))

    episodes_page_node = soup.find("a", class_="bp_item np_episode_guide np_right_arrow")

    if episodes_page_node:
        episodes_url = "https://imdb.com" + episodes_page_node.get("href")
        episodes_page = requests.get(episodes_url)

        episodes_soup = BeautifulSoup(episodes_page.text, "html.parser")
        seasons_node = episodes_soup.find("select", id="bySeason")

        if seasons_node:
            print("Seasons: ", len(seasons_node.find_all("option")))

    summary_node = soup.find("div", class_="summary_text")

    summary_text = bs.try_get_text(summary_node).strip()
    if "See full summary" in summary_text:
        summary_end_index = summary_text.index("See full summary")
        summary_text = summary_text[0:summary_end_index].strip()

    print("Summary: ", summary_text)

    review_node = soup.find("div", class_="user-comments")
    if review_node:
        review_title = ""
        review_rating = ""
        review_text = ""

        review_rating_node = review_node.find("div", class_="tinystarbar")
        if review_rating_node:
            review_rating = review_rating_node.get("title")

        review_title_node = review_node.select(".user-comments > span:nth-child(2) > strong:nth-child(1)")
        if review_title_node:
            review_title = bs.try_get_text(review_title_node)

        review_text_node = review_node.select(".user-comments > span:nth-child(2) > div:nth-child(3)")
        if review_text_node:
            review_text = bs.try_get_text(review_text_node)

        print("\n")
        print("Review: ", c(review_title, "yellow"), c(review_rating, "green"))
        print(unidecode(review_text))

    print("Url: ", url)
    print("\n")

# import importlib
# importlib.reload(lib)

