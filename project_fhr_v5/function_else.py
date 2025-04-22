import requests
from bs4 import BeautifulSoup
import json
import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox,Label,Entry,Button
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
url = 'https://news.ustc.edu.cn/info/1155/89289.htm'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
Chrome/55.0.2883.87 Safari/537.36'}

# 获取IMF数据的API接口
def get_imf_data(country_code, indicator_code, start_year, end_year):
    base_url = "http://api.worldbank.org/v2/country/{}/indicator/{}?date={}:{}&format=json"
    url = base_url.format(country_code, indicator_code, start_year, end_year)
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data from {url}. Error: {e}")
        return None

# 提取数据并转换为DataFrame
def extract_data(data):
    if not data or len(data) < 2:
        return None
    records = data[1]  # 第二个元素包含数据记录
    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'], format='%Y')
    df.set_index('date', inplace=True)
    return df

# 绘制折线图并嵌入到Tkinter窗口
def plot_data(df, country_name, indicator_name, canvas):
    if df is None or df.empty:
        messagebox.showinfo("Info", f"No data available for {country_name} - {indicator_name}")
        return
    canvas_width = canvas.get_tk_widget().winfo_width()
    canvas_height = canvas.get_tk_widget().winfo_height()
    # 转换为英寸（matplotlib 的 figsize 单位是英寸）
    dpi = 100  # 假设 DPI 为 100
    figsize = (canvas_width / dpi, canvas_height / dpi)
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df.index, df['value'], marker='o', linestyle='-')
    ax.set_title(f"{country_name} - {indicator_name} (1990-2022)")
    ax.set_xlabel("Year")
    ax.set_ylabel(indicator_name)
    ax.grid(True)

    # 将图表嵌入到Tkinter窗口
    canvas.figure = fig
    canvas.draw()

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