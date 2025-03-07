# filename: arxiv_latest.py

import feedparser

def fetch_articles():
    NewsFeed = feedparser.parse("http://export.arxiv.org/rss/astro-ph")
    entries = NewsFeed.entries[:5]

    print("\nThe latest 5 articles from arXiv are:\n")
    for entry in entries:
        print(f"Title: {entry.title}")
        print(f"Summary: {entry.summary}")
        print(f"Link: {entry.link}")
        print("\n-----\n")

fetch_articles()