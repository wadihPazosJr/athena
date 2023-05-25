import requests
from bs4 import BeautifulSoup
import random

def parse_articles(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        article_urls = []
        article_links = soup.find_all('a')

        for link in article_links:
            href = link.get('href')
            if href and is_article_link(href):
                article_urls.append(href)

        return article_urls

    except requests.exceptions.RequestException as e:
        print('Failed to retrieve articles')

def is_article_link(href):
    # Add additional criteria to identify article links
    # For example, you can check if the link contains certain keywords or has a specific URL pattern
    # Return True if the link is determined to be an article, False otherwise
    return 'article' in href or 'news' in href

def add_url(url):
    try:
        response = requests.post('http://localhost:5000/generate_json', json={'url': url})
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print('Failed to add URL')

if __name__ == "__main__":
    urls = parse_articles('https://apnews.com/hub/world-news')
    if urls:
        for url in urls:
            print(f"URL: {url}")
            add_url(url)
    else:
        print('No URLs retrieved from articles')
