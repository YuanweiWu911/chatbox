import tkinter as tk
from tkinter import ttk

# 设置环境变量确保 GTK 支持输入法
import os
os.environ['GTK_IM_MODULE'] = 'ibus'
os.environ['QT_IM_MODULE'] = 'ibus'
os.environ['XMODIFIERS'] = '@im=ibus'

# 创建主窗口
root = tk.Tk()
root.title("ttk.Entry 示例")

# 创建 ttk.Entry 组件
entry = ttk.Entry(root)
entry.pack(pady=20, padx=20)

# 运行主循环
root.mainloop()

