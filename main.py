"""
main.py - 学生成绩管理系统主程序
启动登录界面
"""

import sys
import os

# 确保项目根目录在Python路径中
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from ui.login_ui import LoginUI


def main():
    """
    程序入口函数

    功能:
    - 初始化登录界面
    - 启动Tkinter主循环
    """
    print("=" * 50)
    print("学生成绩管理系统")
    print("=" * 50)
    print("正在启动登录界面...")
    print()

    # 创建并显示登录界面
    login_app = LoginUI()
    login_app.show()

    print()
    print("=" * 50)
    print("程序已退出")
    print("=" * 50)


if __name__ == "__main__":
    main()
