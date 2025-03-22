# filename: arxiv_articles_api.py

import requests
import feedparser

# Define the URL of the arXiv API
url = "http://export.arxiv.org/api/query?"

# Define the parameters for the API request
params = {
    "search_query": "all:electron",
    "start": 0,
    "max_results": 5,
}

# Send a GET request to the API
response = requests.get(url, params=params)

# Parse the response text with feedparser
feed = feedparser.parse(response.text)

# Print the title and summary of the 5 latest articles
for entry in feed.entries:
    print("Title:", entry.title)
    print("Summary:", entry.summary)
    print("\n")