import requests
from bs4 import BeautifulSoup
import json


url = 'https://news.ustc.edu.cn/info/1155/89289.htm'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
Chrome/55.0.2883.87 Safari/537.36'}


def ask_adddress(url='https://news.ustc.edu.cn/info/1155/89289.htm',headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
Chrome/55.0.2883.87 Safari/537.36'}):
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    text_content = soup.get_text()
    print(text_content)
    return text_content
ask_adddress(url,headers)