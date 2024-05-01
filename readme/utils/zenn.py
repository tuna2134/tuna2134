import requests
from bs4 import BeautifulSoup
from typing import TypedDict, List


class Article(TypedDict):
    title: str
    uri: str


def fetch_articles() -> List[Article]:
    response = requests.get("https://zenn.dev/dms_sub/feed")
    soup = BeautifulSoup(response.text, features="xml")
    return [
        {
            "title": item.find("title").get_text(),
            "uri": item.find("link").get_text()
        }
        for item in soup.find_all("item")
    ]