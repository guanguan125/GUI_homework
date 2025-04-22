import tkinter as tk
from button_function import App

# 创建主窗口
root = tk.Tk()
root.title("welcome to projetc_fhr")
root.geometry("640x640")  # 设置窗口大小

# 加载主目录界面
app  = App(root)

# 运行主循环
root.mainloop()