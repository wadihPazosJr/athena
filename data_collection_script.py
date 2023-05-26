import requests
from bs4 import BeautifulSoup
import random
import json
import validators
import os
from datetime import date

BASE_URLS = ["https://apnews.com/hub/"]
URL_TO_TOPICS = {
    "https://apnews.com/hub/": [
        "us-news",
        "world-news",
        "politics",
        "sports",
        "entertainment",
        "business",
        "health",
        "science",
        "oddities",
        "lifestyle",
    ]
}
ARTICLE_KEYWORDS = {"https://apnews.com/hub/": "article"}
TODAYS_DATE = date.today().strftime("%m-%d-%Y")
URL_TO_RULES = {
    "https://apnews.com/hub/": {
        "title": {"tag": "h1", "attrs": {"class": "Component-headline-0-2-121"}},
        "author": {"tag": "span", "attrs": {"class": ""}},
    },
}


def is_article_link(base, href):
    return ARTICLE_KEYWORDS[base] in href


def parse_articles(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        article_urls = []
        article_links = soup.find_all("a")

        for link in article_links:
            href = link.get("href")
            if href and is_article_link(href):
                article_urls.append(href)

        return article_urls

    except requests.exceptions.RequestException as e:
        print("Failed to retrieve articles")


def compile_article_urls(base_url):
    topics = URL_TO_TOPICS[base_url]
    article_urls = {}
    for topic in topics:
        articles = parse_articles(base_url + topic)
        article_urls[topic] = articles
    return article_urls


def scrape_article(rules, url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        data = {}
        # Extracting the title
        # Extracting the author
        # Extracting the publish date
        # Extracting the excerpt
        # Extracting the text

    except requests.exceptions.RequestException as e:
        print("Failed to retrieve articles")


def articles_to_json(base_url, article_urls):
    json_data = []
    diff_topics = URL_TO_TOPICS[base_url]
    for topic in diff_topics:
        articles = article_urls[topic]
        for article in articles:
            article_data = {
                "topic": topic,
                "article_url": article,
            }

            data = scrape_article(URL_TO_RULES[base_url], article)
            article_data["data"] = data

            json_data.append(article_data)

    return json_data


def run():
    for base_url in BASE_URLS:
        article_urls = compile_article_urls(base_url)
        json_data = articles_to_json(base_url, article_urls)
        src = {base_url.split("/")[-2]}
        file_name = f"./data/{src}/{src}_{TODAYS_DATE}_data.json"
        with open(file_name, "w") as file:
            json_string = json.dumps(json_data, indent=4)
            file.write(json_string)


run()
