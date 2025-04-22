import requests
from bs4 import BeautifulSoup
import json

def get_publications_of_author(author_name):
    # Step 1: Search for the author on DBLP
    search_url = f"https://dblp.org/search/publ/api/?q=author:{author_name}&format=json"
    response = requests.get(search_url)
    data = response.json()

    # Step 2: Extract publication information
    publications = []
    if "result" in data and "hits" in data["result"] and "hit" in data["result"]["hits"]:
        for hit in data["result"]["hits"]["hit"]:
            info = hit["info"]
            publication = {
                "title": info.get("title", ""),
                "authors": info.get("authors", {}).get("author", []),
                "venue": info.get("venue", ""),
                "year": info.get("year", ""),
                "url": info.get("url", "")
            }
            publications.append(publication)

    return publications


if __name__ == "__main__":
    author_name = "Ya-qin Zhang"
    publications = get_publications_of_author(author_name)
    if publications:
        print(publications[1])
    else:
        print("No publications found for the given author.")