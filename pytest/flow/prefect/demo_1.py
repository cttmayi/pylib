from prefect import task
import requests

GITHUB_TRENDING_URL = "https://trendings.herokuapp.com/repo"

@task
def download_data():
    params = {'since': 'daily'}
    trending_data = requests.get(GITHUB_TRENDING_URL, params).json()
    return trending_data

def handle_data(data):
    return [i for i in data["items"]]


import csv

def save_data(rows):
    headers = ["repo", "repo_link", "stars", "forks", "added_stars"]
    with open("/tmp/trending.csv", "w", newline="") as f:
        f_csv = csv.DictWriter(f, headers, extrasaction='ignore')
        f_csv.writeheader()
        f_csv.writerows(rows)


from prefect import Flow

with Flow("GitHub_Trending_Flow") as flow:
    data = download_data()
    rows = handle_data(data)
    save_data(rows)

flow.run()