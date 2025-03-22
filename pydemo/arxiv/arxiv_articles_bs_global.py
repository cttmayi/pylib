# filename: arxiv_articles_bs_global.py

import requests
from bs4 import BeautifulSoup

# Define the URL of the arXiv global RSS feed
url = "http://export.arxiv.org/rss/arxiv"

# Send a GET request to the URL
response = requests.get(url)

# Parse the response text with BeautifulSoup with lxml parser
soup = BeautifulSoup(response.text, 'lxml')

# Find all entry elements (each represents a article)
entries = soup.find_all('entry')

# Print the title and summary of the 5 latest articles
for entry in entries[:5]:
    print("Title:", entry.title.text)
    print("Summary:", entry.summary.text)
    print("\n")