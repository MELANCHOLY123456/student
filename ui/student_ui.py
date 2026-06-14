"""
StudentUI - 学生操作界面
使用Python+Tkinter实现
包含查询个人成绩、查询总成绩按钮
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dao.score_dao import ScoreDAO


class StudentUI:
    """
    学生操作界面

    功能:
    - 查询个人成绩（按科目）
    - 查询总成绩统计（平均分、绩点）
    """

    def __init__(self, user_info: dict, login_ui):
        """
        初始化学生界面

        Args:
            user_info: 用户信息
            login_ui: 登录界面对象
        """
        self.user_info = user_info
        self.login_ui = login_ui
        self.score_dao = ScoreDAO()

        self.root = tk.Toplevel()
        self.root.title(f"学生界面 - {user_info['real_name']}")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.logout)

    def create_widgets(self):
        """创建界面组件"""
        # 顶部信息栏
        header = tk.Frame(self.root, bg="#2ecc71", height=50)
        header.pack(fill="x")

        tk.Label(
            header,
            text=f"学生: {self.user_info['real_name']} ({self.user_info['username']})",
            font=("Microsoft YaHei", 14, "bold"),
            bg="#2ecc71",
            fg="white"
        ).pack(side="left", padx=20, pady=10)

        tk.Button(
            header,
            text="退出登录",
            font=("Microsoft YaHei", 11),
            bg="#e74c3c",
            fg="white",
            command=self.logout
        ).pack(side="right", padx=20, pady=10)

        # 功能按钮区
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="📋 查询个人成绩",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=15,
            height=2,
            command=self.show_personal_scores
        ).pack(side="left", padx=15)

        tk.Button(
            btn_frame,
            text="📊 查询总成绩",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#9b59b6",
            fg="white",
            width=15,
            height=2,
            command=self.show_total_scores
        ).pack(side="left", padx=15)

        # 内容显示区
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 默认显示个人成绩
        self.show_personal_scores()

    def clear_content(self):
        """清空内容区"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_personal_scores(self):
        """显示个人成绩"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="个人成绩明细",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=10)

        # 获取学生ID（根据用户名查询）
        student_id = self._get_student_id()

        if not student_id:
            tk.Label(
                self.content_frame,
                text="未找到学生信息",
                font=("Microsoft YaHei", 14),
                fg="#e74c3c"
            ).pack(pady=50)
            return

        # 查询成绩
        scores = self.score_dao.query_by_student(student_id)

        if not scores:
            tk.Label(
                self.content_frame,
                text="暂无成绩记录",
                font=("Microsoft YaHei", 14),
                fg="#7f8c8d"
            ).pack(pady=50)
            return

        # 创建表格
        self._create_score_table(scores)

    def _create_score_table(self, scores: list):
        """创建成绩表格"""
        # 创建表格框架
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill="both", expand=True, pady=10)

        # 滚动条
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")

        columns = ("subject", "credit", "daily", "midterm", "final", "total", "gpa", "status")
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )

        tree.heading("subject", text="科目")
        tree.heading("credit", text="学分")
        tree.heading("daily", text="平时")
        tree.heading("midterm", text="期中")
        tree.heading("final", text="期末")
        tree.heading("total", text="总评")
        tree.heading("gpa", text="绩点")
        tree.heading("status", text="状态")

        tree.column("subject", width=150)
        tree.column("credit", width=60)
        tree.column("daily", width=60)
        tree.column("midterm", width=60)
        tree.column("final", width=60)
        tree.column("total", width=60)
        tree.column("gpa", width=60)
        tree.column("status", width=80)

        tree.pack(fill="both", expand=True)
        scrollbar.config(command=tree.yview)

        # 填充数据
        for sc in scores:
            status_cn = {
                'draft': '📝草稿',
                'submitted': '⏳待审核',
                'approved': '✅已通过',
                'rejected': '❌已驳回'
            }.get(sc.get('status', ''), sc.get('status', ''))

            tree.insert("", "end", values=(
                sc.get('subject_name', ''),
                sc.get('credit', ''),
                sc.get('daily_score', ''),
                sc.get('midterm_score', ''),
                sc.get('final_score', ''),
                sc.get('total_score', ''),
                sc.get('gpa_point', ''),
                status_cn
            ))

    def show_total_scores(self):
        """显示总成绩统计"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="总成绩统计",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=10)

        student_id = self._get_student_id()

        if not student_id:
            tk.Label(
                self.content_frame,
                text="未找到学生信息",
                font=("Microsoft YaHei", 14),
                fg="#e74c3c"
            ).pack(pady=50)
            return

        # 查询成绩
        scores = self.score_dao.query_by_student(student_id)

        if not scores:
            tk.Label(
                self.content_frame,
                text="暂无成绩记录",
                font=("Microsoft YaHei", 14),
                fg="#7f8c8d"
            ).pack(pady=50)
            return

        # 计算统计信息
        total_courses = len(scores)
        approved_scores = [s for s in scores if s.get('status') == 'approved']

        if approved_scores:
            avg_score = sum(s.get('total_score', 0) for s in approved_scores) / len(approved_scores)
            avg_gpa = sum(s.get('gpa_point', 0) for s in approved_scores) / len(approved_scores)
            total_credits = sum(s.get('credit', 0) for s in approved_scores)
        else:
            avg_score = 0
            avg_gpa = 0
            total_credits = 0

        # 显示统计卡片
        stats_frame = tk.Frame(self.content_frame)
        stats_frame.pack(pady=20)

        stats = [
            ("📚 科目总数", str(total_courses), "#3498db"),
            ("✅ 已审核", str(len(approved_scores)), "#2ecc71"),
            ("📊 平均分", f"{avg_score:.2f}", "#9b59b6"),
            ("🏆 平均绩点", f"{avg_gpa:.2f}", "#f39c12"),
            ("📝 总学分", f"{total_credits:.1f}", "#1abc9c"),
        ]

        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=color, width=120, height=100)
            card.grid(row=0, column=i, padx=10, pady=5)
            card.grid_propagate(False)

            tk.Label(card, text=label, font=("Microsoft YaHei", 11), 
                    bg=color, fg="white").pack(pady=10)
            tk.Label(card, text=value, font=("Microsoft YaHei", 18, "bold"), 
                    bg=color, fg="white").pack()

        # 成绩详情表格
        tk.Label(
            self.content_frame,
            text="成绩详情",
            font=("Microsoft YaHei", 14, "bold"),
            fg="#2c3e50"
        ).pack(pady=15)

        self._create_score_table(scores)

    def _get_student_id(self) -> int:
        """
        根据当前用户获取学生ID

        Returns:
            int: 学生ID，0表示未找到
        """
        from dao.db import DBConnection, DB_CONFIG

        with DBConnection(**DB_CONFIG) as db:
            # 通过user_id查询student_id
            sql = """
                SELECT s.student_id 
                FROM student s
                JOIN user u ON s.user_id = u.user_id
                WHERE u.username = %s
            """
            result = db.execute_query(sql, (self.user_info['username'],))

            if result:
                return result[0]['student_id']
            return 0

    def logout(self):
        """退出登录"""
        self.root.destroy()
        self.login_ui.logout()
