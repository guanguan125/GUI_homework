import tkinter as tk
from tkinter import ttk, messagebox,Label,Entry,Button
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df['value'], marker='o', linestyle='-')
    ax.set_title(f"{country_name} - {indicator_name} (1990-2022)")
    ax.set_xlabel("Year")
    ax.set_ylabel(indicator_name)
    ax.grid(True)

    # 将图表嵌入到Tkinter窗口
    canvas.figure = fig
    canvas.draw()

# GUI应用程序
class EconomicDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Economic Data Viewer")

        Label(self.root, text="Enter Country Name (e.g., China):").pack(pady=10)
        self.country_entry = Entry(self.root)
        self.country_entry.pack()

        Label(self.root, text="Enter Start Year (e.g., 1990):").pack(pady=10)
        self.start_year_entry = Entry(self.root)
        self.start_year_entry.pack()

        Label(self.root, text="Enter End Year (e.g., 2022):").pack(pady=10)
        self.end_year_entry = Entry(self.root)
        self.end_year_entry.pack()

        Button(self.root, text="Fetch Data", command=self.fetch_data).pack(pady=20)

        # 创建一个Matplotlib画布
        self.figure = plt.Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def fetch_data(self):
        country_name = self.country_entry.get()
        start_year = self.start_year_entry.get()
        end_year = self.end_year_entry.get()

        country_codes = {
            "China": "CN",
            "United States": "US",
            "Japan": "JP",
            "Germany": "DE",
            "India": "IN"
        }

        if country_name not in country_codes:
            messagebox.showerror("Error", "Country not supported.")
            return

        country_code = country_codes[country_name]

        # 获取GDP数据
        gdp_data = get_imf_data(country_code, "NY.GDP.MKTP.CD", start_year, end_year)
        gdp_df = extract_data(gdp_data)

        # 获取通货膨胀率数据
        inflation_data = get_imf_data(country_code, "FP.CPI.TOTL.ZG", start_year, end_year)
        inflation_df = extract_data(inflation_data)

        # 清空画布
        self.figure.clear()

        # 绘制GDP折线图
        plot_data(gdp_df, country_name, "GDP (Current US$)", self.canvas)

        # 绘制通货膨胀率折线图
        plot_data(inflation_df, country_name, "Inflation Rate (%)", self.canvas)

if __name__ == "__main__":
    root = tk.Tk()
    app = EconomicDataApp(root)
    root.mainloop()