"""
TeacherUI - 教师操作界面
使用Python+Tkinter实现
包含成绩录入、成绩查询、成绩修改、成绩统计、导出报表按钮
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from service.score_service import ScoreService
from dao.score_dao import ScoreDAO
from dao.user_dao import UserDAO


class TeacherUI:
    """
    教师操作界面

    功能:
    - 成绩录入
    - 成绩查询（按学生/按科目）
    - 成绩修改
    - 成绩统计
    - 导出报表
    """

    def __init__(self, user_info: dict, login_ui):
        """
        初始化教师界面

        Args:
            user_info: 用户信息
            login_ui: 登录界面对象（用于返回登录）
        """
        self.user_info = user_info
        self.login_ui = login_ui
        self.score_service = ScoreService()
        self.score_dao = ScoreDAO()
        self.user_dao = UserDAO()

        self.root = tk.Toplevel()
        self.root.title(f"教师界面 - {user_info['real_name']}")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        self.create_widgets()

        # 窗口关闭时返回登录
        self.root.protocol("WM_DELETE_WINDOW", self.logout)

    def create_widgets(self):
        """创建界面组件"""
        # 顶部信息栏
        header = tk.Frame(self.root, bg="#3498db", height=50)
        header.pack(fill="x")

        tk.Label(
            header,
            text=f"教师: {self.user_info['real_name']} ({self.user_info['username']})",
            font=("Microsoft YaHei", 14, "bold"),
            bg="#3498db",
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
        btn_frame.pack(pady=15)

        buttons = [
            ("📝 成绩录入", self.show_input_frame, "#2ecc71"),
            ("🔍 成绩查询", self.show_query_frame, "#3498db"),
            ("✏️ 成绩修改", self.show_update_frame, "#f39c12"),
            ("📊 成绩统计", self.show_statistics_frame, "#9b59b6"),
            ("📥 导出报表", self.export_report, "#1abc9c"),
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
            ).pack(side="left", padx=8)

        # 内容显示区
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 默认显示成绩查询
        self.show_query_frame()

    def clear_content(self):
        """清空内容区"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_input_frame(self):
        """显示成绩录入界面"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="成绩录入",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=10)

        form = tk.Frame(self.content_frame)
        form.pack(pady=10)

        # 学生ID
        tk.Label(form, text="学生ID:", font=("Microsoft YaHei", 12)).grid(row=0, column=0, pady=8, padx=5, sticky="e")
        self.input_student_id = tk.Entry(form, font=("Microsoft YaHei", 12), width=20)
        self.input_student_id.grid(row=0, column=1, pady=8, padx=5)

        # 科目ID
        tk.Label(form, text="科目ID:", font=("Microsoft YaHei", 12)).grid(row=1, column=0, pady=8, padx=5, sticky="e")
        self.input_subject_id = tk.Entry(form, font=("Microsoft YaHei", 12), width=20)
        self.input_subject_id.grid(row=1, column=1, pady=8, padx=5)

        # 平时成绩
        tk.Label(form, text="平时成绩:", font=("Microsoft YaHei", 12)).grid(row=2, column=0, pady=8, padx=5, sticky="e")
        self.input_daily = tk.Entry(form, font=("Microsoft YaHei", 12), width=20)
        self.input_daily.grid(row=2, column=1, pady=8, padx=5)
        tk.Label(form, text="(0-100, 权重30%)", font=("Microsoft YaHei", 10), fg="#7f8c8d").grid(row=2, column=2, padx=5)

        # 期中成绩
        tk.Label(form, text="期中成绩:", font=("Microsoft YaHei", 12)).grid(row=3, column=0, pady=8, padx=5, sticky="e")
        self.input_midterm = tk.Entry(form, font=("Microsoft YaHei", 12), width=20)
        self.input_midterm.grid(row=3, column=1, pady=8, padx=5)
        tk.Label(form, text="(0-100, 权重20%)", font=("Microsoft YaHei", 10), fg="#7f8c8d").grid(row=3, column=2, padx=5)

        # 期末成绩
        tk.Label(form, text="期末成绩:", font=("Microsoft YaHei", 12)).grid(row=4, column=0, pady=8, padx=5, sticky="e")
        self.input_final = tk.Entry(form, font=("Microsoft YaHei", 12), width=20)
        self.input_final.grid(row=4, column=1, pady=8, padx=5)
        tk.Label(form, text="(0-100, 权重50%)", font=("Microsoft YaHei", 10), fg="#7f8c8d").grid(row=4, column=2, padx=5)

        # 提交按钮
        tk.Button(
            form,
            text="提交成绩",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            width=15,
            command=self.submit_score
        ).grid(row=5, column=1, pady=20)

    def submit_score(self):
        """提交成绩"""
        try:
            student_id = int(self.input_student_id.get().strip())
            subject_id = int(self.input_subject_id.get().strip())
            daily = float(self.input_daily.get().strip()) if self.input_daily.get() else None
            midterm = float(self.input_midterm.get().strip()) if self.input_midterm.get() else None
            final = float(self.input_final.get().strip()) if self.input_final.get() else None
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return

        result = self.score_service.add_score(
            student_id=student_id,
            subject_id=subject_id,
            daily_score=daily,
            midterm_score=midterm,
            final_score=final,
            input_by=self.user_info['user_id']
        )

        if result['success']:
            messagebox.showinfo("成功", result['message'])
            # 清空输入
            for entry in [self.input_student_id, self.input_subject_id, 
                         self.input_daily, self.input_midterm, self.input_final]:
                entry.delete(0, tk.END)
        else:
            messagebox.showerror("错误", result['message'])

    def show_query_frame(self):
        """显示成绩查询界面"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="成绩查询",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=10)

        # 查询条件
        query_frame = tk.Frame(self.content_frame)
        query_frame.pack(pady=10)

        tk.Label(query_frame, text="学生ID:", font=("Microsoft YaHei", 12)).pack(side="left", padx=5)
        self.query_student_id = tk.Entry(query_frame, font=("Microsoft YaHei", 12), width=15)
        self.query_student_id.pack(side="left", padx=5)

        tk.Label(query_frame, text="科目ID:", font=("Microsoft YaHei", 12)).pack(side="left", padx=5)
        self.query_subject_id = tk.Entry(query_frame, font=("Microsoft YaHei", 12), width=15)
        self.query_subject_id.pack(side="left", padx=5)

        tk.Button(
            query_frame,
            text="查询",
            font=("Microsoft YaHei", 11),
            bg="#3498db",
            fg="white",
            command=self.do_query
        ).pack(side="left", padx=10)

        tk.Button(
            query_frame,
            text="查询全部",
            font=("Microsoft YaHei", 11),
            bg="#9b59b6",
            fg="white",
            command=self.query_all
        ).pack(side="left", padx=5)

        # 结果显示表格
        self.create_result_table()

    def create_result_table(self):
        """创建结果表格"""
        # 创建表格框架
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill="both", expand=True, pady=10)

        # 创建滚动条
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")

        # 创建表格
        columns = ("score_id", "student", "subject", "daily", "midterm", "final", "total", "gpa", "status")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )

        # 设置列标题
        self.tree.heading("score_id", text="ID")
        self.tree.heading("student", text="学生")
        self.tree.heading("subject", text="科目")
        self.tree.heading("daily", text="平时")
        self.tree.heading("midterm", text="期中")
        self.tree.heading("final", text="期末")
        self.tree.heading("total", text="总评")
        self.tree.heading("gpa", text="绩点")
        self.tree.heading("status", text="状态")

        # 设置列宽
        self.tree.column("score_id", width=50)
        self.tree.column("student", width=80)
        self.tree.column("subject", width=120)
        self.tree.column("daily", width=60)
        self.tree.column("midterm", width=60)
        self.tree.column("final", width=60)
        self.tree.column("total", width=60)
        self.tree.column("gpa", width=60)
        self.tree.column("status", width=80)

        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

    def do_query(self):
        """执行查询"""
        student_id = self.query_student_id.get().strip()
        subject_id = self.query_subject_id.get().strip()

        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)

        if student_id:
            results = self.score_dao.query_by_student(int(student_id))
        elif subject_id:
            results = self.score_dao.query_by_subject(int(subject_id))
        else:
            messagebox.showwarning("提示", "请输入学生ID或科目ID")
            return

        self.fill_table(results)

    def query_all(self):
        """查询所有成绩"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        results = self.score_dao.query_all()
        self.fill_table(results)

    def fill_table(self, results):
        """填充表格数据"""
        if not results:
            messagebox.showinfo("提示", "未找到记录")
            return

        for r in results:
            self.tree.insert("", "end", values=(
                r.get('score_id', ''),
                r.get('student_name', ''),
                r.get('subject_name', ''),
                r.get('daily_score', ''),
                r.get('midterm_score', ''),
                r.get('final_score', ''),
                r.get('total_score', ''),
                r.get('gpa_point', ''),
                r.get('status', '')
            ))

    def show_update_frame(self):
        """显示成绩修改界面"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="成绩修改",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=10)

        form = tk.Frame(self.content_frame)
        form.pack(pady=10)

        tk.Label(form, text="成绩ID:", font=("Microsoft YaHei", 12)).grid(row=0, column=0, pady=8, padx=5, sticky="e")
        self.update_score_id = tk.Entry(form, font=("Microsoft YaHei", 12), width=20)
        self.update_score_id.grid(row=0, column=1, pady=8, padx=5)

        tk.Label(form, text="平时成绩:", font=("Microsoft YaHei", 12)).grid(row=1, column=0, pady=8, padx=5, sticky="e")
        self.update_daily = tk.Entry(form, font=("Microsoft YaHei", 12), width=20)
        self.update_daily.grid(row=1, column=1, pady=8, padx=5)

        tk.Label(form, text="期中成绩:", font=("Microsoft YaHei", 12)).grid(row=2, column=0, pady=8, padx=5, sticky="e")
        self.update_midterm = tk.Entry(form, font=("Microsoft YaHei", 12), width=20)
        self.update_midterm.grid(row=2, column=1, pady=8, padx=5)

        tk.Label(form, text="期末成绩:", font=("Microsoft YaHei", 12)).grid(row=3, column=0, pady=8, padx=5, sticky="e")
        self.update_final = tk.Entry(form, font=("Microsoft YaHei", 12), width=20)
        self.update_final.grid(row=3, column=1, pady=8, padx=5)

        tk.Label(form, text="状态:", font=("Microsoft YaHei", 12)).grid(row=4, column=0, pady=8, padx=5, sticky="e")
        self.update_status = ttk.Combobox(form, values=["draft", "submitted", "approved", "rejected"], width=18)
        self.update_status.grid(row=4, column=1, pady=8, padx=5)

        tk.Button(
            form,
            text="修改成绩",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#f39c12",
            fg="white",
            width=15,
            command=self.do_update
        ).grid(row=5, column=1, pady=20)

    def do_update(self):
        """执行修改"""
        try:
            score_id = int(self.update_score_id.get().strip())
            daily = float(self.update_daily.get()) if self.update_daily.get() else None
            midterm = float(self.update_midterm.get()) if self.update_midterm.get() else None
            final = float(self.update_final.get()) if self.update_final.get() else None
            status = self.update_status.get() if self.update_status.get() else None
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return

        result = self.score_service.update_score(score_id, daily, midterm, final, status)

        if result['success']:
            messagebox.showinfo("成功", result['message'])
        else:
            messagebox.showerror("错误", result['message'])

    def show_statistics_frame(self):
        """显示成绩统计界面"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="成绩统计",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=10)

        # 科目选择
        query_frame = tk.Frame(self.content_frame)
        query_frame.pack(pady=10)

        tk.Label(query_frame, text="科目ID:", font=("Microsoft YaHei", 12)).pack(side="left", padx=5)
        self.stat_subject_id = tk.Entry(query_frame, font=("Microsoft YaHei", 12), width=15)
        self.stat_subject_id.pack(side="left", padx=5)

        tk.Button(
            query_frame,
            text="统计",
            font=("Microsoft YaHei", 11),
            bg="#9b59b6",
            fg="white",
            command=self.do_statistics
        ).pack(side="left", padx=10)

        # 结果显示
        self.stat_result = tk.Text(self.content_frame, font=("Microsoft YaHei", 12), height=15, width=60)
        self.stat_result.pack(pady=20)

    def do_statistics(self):
        """执行统计"""
        try:
            subject_id = int(self.stat_subject_id.get().strip())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的科目ID")
            return

        stats = self.score_service.get_subject_statistics(subject_id)

        if not stats:
            messagebox.showinfo("提示", "未找到该科目的成绩记录")
            return

        self.stat_result.delete("1.0", tk.END)
        self.stat_result.insert("1.0", f"""
科目统计报告
{'='*40}
参考人数: {stats['total_count']} 人
平均分: {stats['avg_score']} 分
最高分: {stats['max_score']} 分
最低分: {stats['min_score']} 分
及格人数: {stats['pass_count']} 人
及格率: {stats['pass_rate']}%
{'='*40}
        """)

    def export_report(self):
        """导出报表"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv"), ("文本文件", "*.txt")]
        )

        if not file_path:
            return

        results = self.score_dao.query_all()

        try:
            with open(file_path, 'w', encoding='utf-8-sig') as f:
                # 写入表头
                f.write("成绩ID,学生ID,学生姓名,科目ID,科目名称,平时成绩,期中成绩,期末成绩,总评成绩,绩点,状态\n")

                # 写入数据
                for r in results:
                    f.write(f"{r.get('score_id','')},{r.get('student_id','')},{r.get('student_name','')},"
                           f"{r.get('subject_id','')},{r.get('subject_name','')},"
                           f"{r.get('daily_score','')},{r.get('midterm_score','')},{r.get('final_score','')},"
                           f"{r.get('total_score','')},{r.get('gpa_point','')},{r.get('status','')}\n")

            messagebox.showinfo("成功", f"报表已导出到:\n{file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {e}")

    def logout(self):
        """退出登录"""
        self.root.destroy()
        self.login_ui.logout()
