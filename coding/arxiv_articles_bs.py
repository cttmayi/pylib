# filename: arxiv_articles_bs.py

import requests
from bs4 import BeautifulSoup

# Define the URL of the arXiv RSS feed
url = "http://export.arxiv.org/rss/cond-mat"

# Send a GET request to the URL
response = requests.get(url)

# Parse the response text with BeautifulSoup with lxml parser
soup = BeautifulSoup(response.text, 'lxml')

# Find all item elements (each represents a article)
items = soup.find_all('item')

# Print the title and summary of the 5 latest articles
for item in items[:5]:
    print("Title:", item.title.text)
    print("Summary:", item.description.text)
    print("\n")