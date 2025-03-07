# filename: arxiv_summarizer.py

import requests
from bs4 import BeautifulSoup
import feedparser

# ARXIV API endpoint
ENDPOINT = 'http://export.arxiv.org/api/query?'

# Build query parameters
query_params = 'sortBy=submittedDate&sortOrder=descending'

# Send GET request
response = requests.get(ENDPOINT + query_params)

# Parse the response using feedparser
feed = feedparser.parse(response.content)


# Open file to write summaries
with open("arXiv.md", "w") as f:
    # Iterate over the first 5 entries
    for entry in feed.entries[:5]:
        # Write title and summary to file
        f.write(f"Title: {entry.title}\n")
        f.write(f"Summary: {entry.summary}\n\n")

print("Summaries saved to arXiv.md.")