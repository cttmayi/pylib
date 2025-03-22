# filename: arxiv_articles.py

import arxiv

# Search for the latest 5 article
search = arxiv.Search(
  max_results=5,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

for result in search.results():
  print("Title:", result.title)
  print("Summary:", result.summary)
  print("\n")