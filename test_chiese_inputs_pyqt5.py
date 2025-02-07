import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget

# 设置环境变量确保 Qt 支持输入法
import os
os.environ['QT_IM_MODULE'] = 'ibus'
os.environ['XMODIFIERS'] = '@im=ibus'

# 创建一个主窗口类
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QLineEdit 示例")
        
        # 创建 QLineEdit 输入框
        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText("请输入中文")
        
        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.entry)

        # 设置主窗口的中央部件
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

# 创建应用实例
app = QApplication(sys.argv)

# 创建主窗口
window = MyWindow()
window.show()

# 运行应用
sys.exit(app.exec_())

