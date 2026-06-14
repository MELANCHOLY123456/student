"""
LoginUI - 登录界面
使用Python+Tkinter实现
包含用户名输入框、密码输入框、角色选择下拉框、登录按钮
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from service.auth_service import AuthService


class LoginUI:
    """
    登录界面类

    功能:
    - 用户名输入
    - 密码输入（隐藏显示）
    - 角色选择（教师/学生/管理员）
    - 登录验证
    - 根据角色跳转到不同界面
    """

    def __init__(self):
        """初始化登录界面"""
        self.auth_service = AuthService()

        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("学生成绩管理系统 - 登录")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        # 设置窗口居中
        self.center_window()

        self.create_widgets()

    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = 400
        height = 350
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_label = tk.Label(
            self.root,
            text="学生成绩管理系统",
            font=("Microsoft YaHei", 20, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=20)

        # 表单框架
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10, padx=40)

        # 用户名
        tk.Label(form_frame, text="用户名:", font=("Microsoft YaHei", 12)).grid(
            row=0, column=0, sticky="e", pady=10, padx=5
        )
        self.username_entry = tk.Entry(form_frame, font=("Microsoft YaHei", 12), width=20)
        self.username_entry.grid(row=0, column=1, pady=10, padx=5)
        self.username_entry.focus()

        # 密码
        tk.Label(form_frame, text="密码:", font=("Microsoft YaHei", 12)).grid(
            row=1, column=0, sticky="e", pady=10, padx=5
        )
        self.password_entry = tk.Entry(form_frame, font=("Microsoft YaHei", 12), 
                                       width=20, show="*")
        self.password_entry.grid(row=1, column=1, pady=10, padx=5)

        # 角色选择
        tk.Label(form_frame, text="角色:", font=("Microsoft YaHei", 12)).grid(
            row=2, column=0, sticky="e", pady=10, padx=5
        )

        self.role_var = tk.StringVar(value="teacher")
        role_combo = ttk.Combobox(
            form_frame,
            textvariable=self.role_var,
            values=["admin", "teacher", "student"],
            font=("Microsoft YaHei", 12),
            width=18,
            state="readonly"
        )
        role_combo.grid(row=2, column=1, pady=10, padx=5)

        # 登录按钮
        login_btn = tk.Button(
            self.root,
            text="登 录",
            font=("Microsoft YaHei", 14, "bold"),
            bg="#3498db",
            fg="white",
            width=15,
            height=1,
            command=self.login
        )
        login_btn.pack(pady=20)

        # 绑定回车键
        self.root.bind('<Return>', lambda event: self.login())

        # 底部信息
        info_label = tk.Label(
            self.root,
            text="默认账号: 教师(t2024001/123456) 学生(s20220101/123456) 管理员(admin001/123456)",
            font=("Microsoft YaHei", 9),
            fg="#7f8c8d"
        )
        info_label.pack(side="bottom", pady=10)

    def login(self):
        """登录验证"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        # 输入验证
        if not username:
            messagebox.showwarning("提示", "请输入用户名")
            return
        if not password:
            messagebox.showwarning("提示", "请输入密码")
            return

        # 调用认证服务
        result = self.auth_service.login(username, password)

        if result is None:
            messagebox.showerror("错误", "用户名或密码错误")
            return

        # 验证角色
        if result['role'] != role:
            messagebox.showerror("错误", f"身份不匹配！该用户角色为: {result['role']}")
            return

        # 登录成功
        messagebox.showinfo("成功", f"欢迎, {result['real_name']}!")

        # 保存当前用户信息
        self.current_user = result

        # 根据角色打开对应界面
        self.open_main_window(role, result)

    def open_main_window(self, role: str, user_info: dict):
        """
        根据角色打开主界面

        Args:
            role: 角色
            user_info: 用户信息
        """
        self.root.withdraw()  # 隐藏登录窗口

        if role == "admin":
            from ui.admin_ui import AdminUI
            AdminUI(user_info, self)
        elif role == "teacher":
            from ui.teacher_ui import TeacherUI
            TeacherUI(user_info, self)
        elif role == "student":
            from ui.student_ui import StudentUI
            StudentUI(user_info, self)

    def show(self):
        """显示登录界面"""
        self.root.mainloop()

    def logout(self):
        """退出登录，返回登录界面"""
        self.root.deiconify()  # 显示登录窗口
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus()


if __name__ == "__main__":
    app = LoginUI()
    app.show()
