# filename: arxiv_fetch.py

import feedparser
from bs4 import BeautifulSoup
import os

def get_arxiv_data():
    d = feedparser.parse('http://export.arxiv.org/rss/cs') 
    return d.entries[:10] 

def write_to_md(entries):
    with open('arXiv.md', 'w') as f:
        for entry in entries:
            soup = BeautifulSoup(entry.summary)
            f.write(f"## {entry.title}\n\n")
            f.write(f"{soup.get_text()}\n\n")
            f.write(f"[Link to the paper]({entry.link})\n\n")

if __name__ == '__main__':
    entries = get_arxiv_data()
    write_to_md(entries)

print("Markdown file 'arXiv.md' has been written in the current directory!")