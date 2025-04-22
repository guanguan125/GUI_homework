import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # 需要安装Pillow库
from tkinter import filedialog
from function_else import ask_adddress,get_publications_of_author

import cv2

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("welcome to fhr project")
        self.root.geometry("640x640")  # 设置窗口大小
        self.load_main_directory()

    def load_main_directory(self):
        # 清空当前窗口的所有内容
        self.clear_widgets()
        
        # 添加一个标签
        label = tk.Label(self.root, text="请选择以下功能", font=("Arial", 14))
        label.pack(pady=20)
        
        # 添加一个按钮，用于进入其他页面
        button1 = tk.Button(self.root, text="搜索科学家的文章", command=self.go_to_other_page1)
        button1.pack(pady=10)

        button2 = tk.Button(self.root, text="进入网络搜索页面", command=self.go_to_other_page2)
        button2.pack(pady=10)

    def go_to_other_page1(self):
        # 清空当前窗口的所有内容
        self.clear_widgets()
        # 加载其他页面的内容
        other_label = tk.Label(self.root, text="这是科学家文章搜索功能页面！", font=("Arial", 14))
        other_label.pack(pady=20)
        # 添加一个按钮，用于返回主目录
        return_button = tk.Button(self.root, text="返回", command=self.load_main_directory)
        return_button.place(x=0, y=0)
        
        # 添加一个按钮，用于选择文件
        entry = tk.Entry(self.root)
        entry.pack()
        address_button = tk.Button(self.root, text="提交", command=lambda: self.search_paper(entry=entry))
        address_button.pack(pady=10)

    def search_paper(self,entry):
        name = entry.get()
        public = get_publications_of_author(name)
        if hasattr(self, 'text'):
            self.text.destroy()
            self.scrollbar.destroy()
        self.text = tk.Text(self.root, wrap="word", font=("Arial", 14))  # 设置字体和自动换行
        self.text.pack(expand=True, fill="both", padx=10, pady=10)  # 填充整个窗口
        self.scrollbar = ttk.Scrollbar(self.root, command=self.text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=self.scrollbar.set)
        if not public:
            self.text.insert("1.0", "No publications found for the given author.")
            return
        for pub in public:
        # 提取作者姓名列表
            authors = [author['text'] for author in pub['authors']]
        # 格式化论文信息
            pub_info = f"Title: {pub['title']}\nAuthors: {', '.join(authors)}\nVenue: {pub['venue']}\nYear: {pub['year']}\n\n"
            self.text.insert(tk.END, pub_info)
        

    def go_to_other_page2(self):
        # 清空当前窗口的所有内容
        self.clear_widgets()
        # 加载其他页面的内容
        other_label = tk.Label(self.root, text="这是搜索页面！", font=("Arial", 14))
        other_label.pack(pady=20)
        # 添加一个按钮，用于返回主目录
        return_button = tk.Button(self.root, text="返回主目录", command=self.load_main_directory)
        return_button.place(x=0, y=0)
        # 添加一个按钮，用于选择文件
        entry = tk.Entry(self.root)
        entry.pack()
        address_button = tk.Button(self.root, text="提交", command=lambda: self.submit(entry=entry))
        address_button.pack(pady=10)
        
        
    def submit(self,entry):
        
        user_input = entry.get()  # 获取输入框的内容
        print("输入的字符串是：", user_input)
        long_text = ask_adddress(url=user_input)
        
        
        text = tk.Text(self.root, wrap="word", font=("Arial", 14))  # 设置字体和自动换行
        text.pack(expand=True, fill="both", padx=10, pady=10)  # 填充整个窗口
        scrollbar = ttk.Scrollbar(self.root, command=text.yview)
        scrollbar.pack(side="right", fill="y")
        text.config(yscrollcommand=scrollbar.set)

        # 设置要显示的长文本
        text.insert("1.0", long_text)  # 插入文本到 Text 控件
        
    def clear_widgets(self):
        # 清空当前窗口的所有内容
        for widget in self.root.winfo_children():
            widget.destroy()