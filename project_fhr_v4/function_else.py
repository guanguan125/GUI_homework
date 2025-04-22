import requests
from bs4 import BeautifulSoup
import json
import cv2
from PIL import Image, ImageTk
url = 'https://news.ustc.edu.cn/info/1155/89289.htm'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
Chrome/55.0.2883.87 Safari/537.36'}


def ask_adddress(url='https://news.ustc.edu.cn/info/1155/89289.htm',headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
Chrome/55.0.2883.87 Safari/537.36'}):
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    text_content = soup.get_text()
    return text_content


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