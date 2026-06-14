"""
AdminUI - 管理员界面
使用Python+Tkinter实现
包含用户管理、设置参数、备份数据按钮
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dao.user_dao import UserDAO
from dao.db import DBConnection, DB_CONFIG


class AdminUI:
    """
    管理员操作界面

    功能:
    - 用户管理（查看、添加、禁用/启用、删除）
    - 系统参数设置
    - 数据备份
    """

    def __init__(self, user_info: dict, login_ui):
        """
        初始化管理员界面

        Args:
            user_info: 用户信息
            login_ui: 登录界面对象
        """
        self.user_info = user_info
        self.login_ui = login_ui
        self.user_dao = UserDAO()

        self.root = tk.Toplevel()
        self.root.title(f"管理员界面 - {user_info['real_name']}")
        self.root.geometry("900x650")
        self.root.resizable(True, True)

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.logout)

    def create_widgets(self):
        """创建界面组件"""
        # 顶部信息栏
        header = tk.Frame(self.root, bg="#e74c3c", height=50)
        header.pack(fill="x")

        tk.Label(
            header,
            text=f"管理员: {self.user_info['real_name']} ({self.user_info['username']})",
            font=("Microsoft YaHei", 14, "bold"),
            bg="#e74c3c",
            fg="white"
        ).pack(side="left", padx=20, pady=10)

        tk.Button(
            header,
            text="退出登录",
            font=("Microsoft YaHei", 11),
            bg="#c0392b",
            fg="white",
            command=self.logout
        ).pack(side="right", padx=20, pady=10)

        # 功能按钮区
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)

        buttons = [
            ("👥 用户管理", self.show_user_management, "#3498db"),
            ("⚙️ 设置参数", self.show_settings, "#f39c12"),
            ("💾 备份数据", self.backup_data, "#2ecc71"),
        ]

        for text, command, color in buttons:
            tk.Button(
                btn_frame,
                text=text,
                font=("Microsoft YaHei", 12),
                bg=color,
                fg="white",
                width=12,
                height=2,
                command=command
            ).pack(side="left", padx=10)

        # 内容显示区
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 默认显示用户管理
        self.show_user_management()

    def clear_content(self):
        """清空内容区"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_user_management(self):
        """显示用户管理界面"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="用户管理",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=10)

        # 操作按钮
        ops_frame = tk.Frame(self.content_frame)
        ops_frame.pack(pady=10)

        tk.Button(
            ops_frame,
            text="➕ 添加用户",
            font=("Microsoft YaHei", 11),
            bg="#2ecc71",
            fg="white",
            command=self.show_add_user_dialog
        ).pack(side="left", padx=5)

        tk.Button(
            ops_frame,
            text="🔄 刷新列表",
            font=("Microsoft YaHei", 11),
            bg="#3498db",
            fg="white",
            command=self.refresh_user_list
        ).pack(side="left", padx=5)

        # 用户列表表格
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill="both", expand=True, pady=10)

        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")

        columns = ("user_id", "username", "role", "real_name", "status", "created_at")
        self.user_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )

        self.user_tree.heading("user_id", text="ID")
        self.user_tree.heading("username", text="用户名")
        self.user_tree.heading("role", text="角色")
        self.user_tree.heading("real_name", text="姓名")
        self.user_tree.heading("status", text="状态")
        self.user_tree.heading("created_at", text="创建时间")

        self.user_tree.column("user_id", width=50)
        self.user_tree.column("username", width=120)
        self.user_tree.column("role", width=80)
        self.user_tree.column("real_name", width=100)
        self.user_tree.column("status", width=60)
        self.user_tree.column("created_at", width=150)

        self.user_tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.user_tree.yview)

        # 右键菜单
        self.context_menu = tk.Menu(self.user_tree, tearoff=0)
        self.context_menu.add_command(label="启用/禁用", command=self.toggle_user_status)
        self.context_menu.add_command(label="删除", command=self.delete_user)

        self.user_tree.bind("<Button-3>", self.show_context_menu)

        # 加载用户数据
        self.refresh_user_list()

    def show_context_menu(self, event):
        """显示右键菜单"""
        item = self.user_tree.identify_row(event.y)
        if item:
            self.user_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def refresh_user_list(self):
        """刷新用户列表"""
        # 清空表格
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        # 加载数据
        users = self.user_dao.get_all_users()

        for user in users:
            status_str = "✅启用" if user.get('status') == 1 else "❌禁用"
            self.user_tree.insert("", "end", values=(
                user.get('user_id', ''),
                user.get('username', ''),
                user.get('role', ''),
                user.get('real_name', ''),
                status_str,
                str(user.get('created_at', ''))
            ))

    def show_add_user_dialog(self):
        """显示添加用户对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加用户")
        dialog.geometry("350x300")
        dialog.resizable(False, False)

        # 居中
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"+{x}+{y}")

        form = tk.Frame(dialog)
        form.pack(pady=20, padx=30)

        # 用户名
        tk.Label(form, text="用户名:", font=("Microsoft YaHei", 12)).grid(row=0, column=0, pady=8, sticky="e")
        username_entry = tk.Entry(form, font=("Microsoft YaHei", 12), width=18)
        username_entry.grid(row=0, column=1, pady=8, padx=5)

        # 密码
        tk.Label(form, text="密码:", font=("Microsoft YaHei", 12)).grid(row=1, column=0, pady=8, sticky="e")
        password_entry = tk.Entry(form, font=("Microsoft YaHei", 12), width=18, show="*")
        password_entry.grid(row=1, column=1, pady=8, padx=5)

        # 角色
        tk.Label(form, text="角色:", font=("Microsoft YaHei", 12)).grid(row=2, column=0, pady=8, sticky="e")
        role_var = tk.StringVar(value="student")
        role_combo = ttk.Combobox(form, textvariable=role_var, 
                                   values=["admin", "teacher", "student"], 
                                   width=16, state="readonly")
        role_combo.grid(row=2, column=1, pady=8, padx=5)

        # 姓名
        tk.Label(form, text="姓名:", font=("Microsoft YaHei", 12)).grid(row=3, column=0, pady=8, sticky="e")
        name_entry = tk.Entry(form, font=("Microsoft YaHei", 12), width=18)
        name_entry.grid(row=3, column=1, pady=8, padx=5)

        def do_add():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            role = role_var.get()
            real_name = name_entry.get().strip()

            if not all([username, password, real_name]):
                messagebox.showwarning("提示", "请填写所有必填项", parent=dialog)
                return

            rows = self.user_dao.insert_user(username, password, role, real_name)

            if rows > 0:
                messagebox.showinfo("成功", "用户添加成功", parent=dialog)
                dialog.destroy()
                self.refresh_user_list()
            else:
                messagebox.showerror("错误", "用户添加失败，用户名可能已存在", parent=dialog)

        tk.Button(
            form,
            text="添加",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            width=10,
            command=do_add
        ).grid(row=4, column=1, pady=20)

    def toggle_user_status(self):
        """切换用户状态"""
        selected = self.user_tree.selection()
        if not selected:
            return

        item = self.user_tree.item(selected[0])
        user_id = item['values'][0]
        current_status = item['values'][4]

        new_status = 0 if current_status == "✅启用" else 1
        new_status_str = "禁用" if new_status == 0 else "启用"

        if messagebox.askyesno("确认", f"确定要{new_status_str}该用户吗?"):
            rows = self.user_dao.update_user_status(user_id, new_status)
            if rows > 0:
                messagebox.showinfo("成功", f"用户已{new_status_str}")
                self.refresh_user_list()
            else:
                messagebox.showerror("错误", "操作失败")

    def delete_user(self):
        """删除用户"""
        selected = self.user_tree.selection()
        if not selected:
            return

        item = self.user_tree.item(selected[0])
        user_id = item['values'][0]
        username = item['values'][1]

        if messagebox.askyesno("确认", f"确定要删除用户 '{username}' 吗?"):
            rows = self.user_dao.delete_user(user_id)
            if rows > 0:
                messagebox.showinfo("成功", "用户已删除")
                self.refresh_user_list()
            else:
                messagebox.showerror("错误", "删除失败")

    def show_settings(self):
        """显示系统参数设置界面"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="系统参数设置",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=10)

        settings_frame = tk.Frame(self.content_frame)
        settings_frame.pack(pady=20)

        # 成绩权重设置
        tk.Label(
            settings_frame,
            text="成绩权重配置",
            font=("Microsoft YaHei", 14, "bold"),
            fg="#34495e"
        ).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(settings_frame, text="平时成绩权重 (%):", font=("Microsoft YaHei", 12)).grid(
            row=1, column=0, pady=8, padx=5, sticky="e"
        )
        self.daily_weight = tk.Entry(settings_frame, font=("Microsoft YaHei", 12), width=10)
        self.daily_weight.insert(0, "30")
        self.daily_weight.grid(row=1, column=1, pady=8, padx=5, sticky="w")

        tk.Label(settings_frame, text="期中成绩权重 (%):", font=("Microsoft YaHei", 12)).grid(
            row=2, column=0, pady=8, padx=5, sticky="e"
        )
        self.midterm_weight = tk.Entry(settings_frame, font=("Microsoft YaHei", 12), width=10)
        self.midterm_weight.insert(0, "20")
        self.midterm_weight.grid(row=2, column=1, pady=8, padx=5, sticky="w")

        tk.Label(settings_frame, text="期末成绩权重 (%):", font=("Microsoft YaHei", 12)).grid(
            row=3, column=0, pady=8, padx=5, sticky="e"
        )
        self.final_weight = tk.Entry(settings_frame, font=("Microsoft YaHei", 12), width=10)
        self.final_weight.insert(0, "50")
        self.final_weight.grid(row=3, column=1, pady=8, padx=5, sticky="w")

        # 绩点换算设置
        tk.Label(
            settings_frame,
            text="绩点换算规则",
            font=("Microsoft YaHei", 14, "bold"),
            fg="#34495e"
        ).grid(row=4, column=0, columnspan=2, pady=15)

        rules_frame = tk.Frame(settings_frame)
        rules_frame.grid(row=5, column=0, columnspan=2, pady=5)

        rules = [
            ("90-100分 -> 4.0", "#2ecc71"),
            ("85-89分  -> 3.7", "#27ae60"),
            ("82-84分  -> 3.3", "#3498db"),
            ("78-81分  -> 3.0", "#2980b9"),
            ("75-77分  -> 2.7", "#9b59b6"),
            ("72-74分  -> 2.3", "#8e44ad"),
            ("68-71分  -> 2.0", "#f39c12"),
            ("64-67分  -> 1.5", "#e67e22"),
            ("60-63分  -> 1.0", "#e74c3c"),
            ("<60分    -> 0.0", "#c0392b"),
        ]

        for i, (text, color) in enumerate(rules):
            tk.Label(rules_frame, text=text, font=("Microsoft YaHei", 11), 
                    bg=color, fg="white", width=20).grid(row=i, column=0, pady=2)

        # 保存按钮
        tk.Button(
            settings_frame,
            text="保存设置",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=12,
            command=self.save_settings
        ).grid(row=6, column=0, columnspan=2, pady=20)

    def save_settings(self):
        """保存设置"""
        try:
            daily = int(self.daily_weight.get())
            midterm = int(self.midterm_weight.get())
            final = int(self.final_weight.get())

            if daily + midterm + final != 100:
                messagebox.showerror("错误", "权重之和必须等于100%")
                return

            messagebox.showinfo("成功", "设置已保存")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")

    def backup_data(self):
        """备份数据"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".sql",
            filetypes=[("SQL文件", "*.sql"), ("文本文件", "*.txt")],
            initialfile=f"backup_{self.user_info['username']}_{tk.StringVar().get()}.sql"
        )

        if not file_path:
            return

        try:
            with DBConnection(**DB_CONFIG) as db:
                # 获取所有表数据
                tables = ['user', 'student', 'subject', 'score']

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"-- 学生成绩管理系统数据备份\n")
                    f.write(f"-- 备份时间: {tk.StringVar().get()}\n")
                    f.write(f"-- 备份人: {self.user_info['real_name']}\n\n")

                    for table in tables:
                        f.write(f"-- 表: {table}\n")
                        data = db.execute_query(f"SELECT * FROM {table}")

                        for row in data:
                            columns = ', '.join(row.keys())
                            values = ', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in row.values()])
                            f.write(f"INSERT INTO {table} ({columns}) VALUES ({values});\n")

                        f.write("\n")

            messagebox.showinfo("成功", f"数据已备份到:\n{file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"备份失败: {e}")

    def logout(self):
        """退出登录"""
        self.root.destroy()
        self.login_ui.logout()
