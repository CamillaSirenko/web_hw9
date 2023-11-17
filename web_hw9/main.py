import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes():
    base_url = "http://quotes.toscrape.com"
    page_url = "/page/1/"
    quotes = []

    while page_url:
        response = requests.get(base_url + page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for quote in soup.select('.quote'):
            text = quote.select_one('.text').get_text()
            author = quote.select_one('.author').get_text()
            tags = [tag.get_text() for tag in quote.select('.tag')]
            quotes.append({
                "text": text,
                "author": author,
                "tags": tags
            })

        next_page = soup.select_one('.next > a')
        page_url = next_page['href'] if next_page else None

    return quotes

def scrape_authors():
    base_url = "http://quotes.toscrape.com"
    authors = []

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for author in soup.select('.author'):
        name = author.get_text()
        authors.append({
            "name": name,
            "url": base_url + "/author/" + name.replace(" ", "-")
        })

    return authors

quotes = scrape_quotes()
authors = scrape_authors()

with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes, f,ensure_ascii=False, indent=2 )

with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors, f, ensure_ascii=False, indent=2)
