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
    authors_set = set()
    page_number = 1

    while True:
        response = requests.get(f"{base_url}/page/{page_number}/")
        soup = BeautifulSoup(response.text, 'html.parser')

        for author_link in soup.select('.author + a'):
            author_url = base_url + author_link['href']
            authors_set.add(author_url)

        next_page = soup.select_one('.next > a')
        if next_page:
            page_number += 1
        else:
            break

    
    authors_list = list(authors_set)


    authors_info = []
    for author_url in authors_list:
        author_response = requests.get(author_url)
        author_soup = BeautifulSoup(author_response.text, 'html.parser')

        # Extract author information as needed (you may need to customize this part)
        author_name = author_soup.select_one('.author-title').get_text()
        birth_date = author_soup.select_one('.author-born-date').get_text()
        bio = author_soup.select_one('.author-description').get_text()

        authors_info.append({
            "name": author_name,
            "birth_date": birth_date,
            "bio": bio,
            "url": author_url
        })

    return authors_info

quotes = scrape_quotes()
authors = scrape_authors()

with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes, f, ensure_ascii=False, indent=2)

with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors, f, ensure_ascii=False, indent=2)