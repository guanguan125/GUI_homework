import tkinter as tk
from PIL import Image, ImageTk  # 需要安装Pillow库
from tkinter import filedialog

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter 示例")
        self.root.geometry("640x640")  # 设置窗口大小
        self.load_main_directory()

    def load_main_directory(self):
        # 清空当前窗口的所有内容
        self.clear_widgets()
        
        # 添加一个标签
        label = tk.Label(self.root, text="这是主目录！", font=("Arial", 14))
        label.pack(pady=20)
        
        # 添加一个按钮，用于进入其他页面
        other_button = tk.Button(self.root, text="进入其他页面", command=self.go_to_other_page)
        other_button.pack(pady=10)

    def go_to_other_page(self):
        # 清空当前窗口的所有内容
        self.clear_widgets()
        
        # 加载其他页面的内容
        other_label = tk.Label(self.root, text="这是其他页面！", font=("Arial", 14))
        other_label.pack(pady=20)
        
        # 尝试加载默认图片
        try:
            image = Image.open("example.jpg")  # 替换为你的图片文件路径
            image.thumbnail((400, 400))  # 调整图片大小
            photo = ImageTk.PhotoImage(image)
            
            # 创建一个Label来显示图片
            image_label = tk.Label(self.root, image=photo)
            image_label.image = photo  # 保持对PhotoImage的引用
            image_label.pack(pady=10)
        except Exception as e:
            print(f"加载图片失败：{e}")
            image_label = tk.Label(self.root, text="无法加载图片，请检查路径！", font=("Arial", 12))
            image_label.pack(pady=10)
        
        # 添加一个按钮，用于选择文件
        img_button = tk.Button(self.root, text="选择图片", command=self.load_image)
        img_button.pack(pady=10)
        
        # 添加一个按钮，用于返回主目录
        return_button = tk.Button(self.root, text="返回主目录", command=self.load_main_directory)
        return_button.pack(pady=10)

    def load_image(self):
        # 打开文件选择对话框，选择图片
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            # 加载图片
            image = Image.open(file_path)
            image.thumbnail((400, 400))  # 调整图片大小
            photo = ImageTk.PhotoImage(image)
            
            # 显示图片
            image_label = tk.Label(self.root, image=photo)
            image_label.image = photo  # 保存对图片的引用，防止被垃圾回收
            image_label.pack(pady=20)

    def clear_widgets(self):
        # 清空当前窗口的所有内容
        for widget in self.root.winfo_children():
            widget.destroy()