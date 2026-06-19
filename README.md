# 📚 学生成绩管理系统

> 一个基于 Python 的高效、安全的学生成绩管理解决方案，采用三层架构设计，支持多角色权限管理。

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-green.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 目录

- [项目简介](#项目简介)
- [技术栈](#技术栈)
- [系统架构](#系统架构)
- [快速开始](#快速开始)
- [环境要求](#环境要求)
- [安装步骤](#安装步骤)
- [项目结构](#项目结构)
- [功能说明](#功能说明)
- [API 和模块说明](#api-和模块说明)
- [数据库说明](#数据库说明)
- [安全性](#安全性)
- [开发指南](#开发指南)
- [故障排查](#故障排查)
- [许可证](#许可证)

---

## 项目简介

学生成绩管理系统是一个为教育机构设计的综合成绩管理平台。系统支持教师录入和管理成绩，学生查询个人成绩，管理员进行系统配置和数据备份。该系统采用经典的三层架构（表现层-业务逻辑层-数据访问层），确保代码结构清晰、易于维护和扩展。

**主要特点：**
- 🔐 多角色权限管理（管理员、教师、学生）
- 📊 自动化成绩计算和统计分析
- 📈 灵活的报表导出功能
- 🔄 成绩权重可配置
- 💾 数据备份和恢复机制
- 🎯 支持按多维度查询（学生、科目等）

---

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.8+ | 编程语言 |
| MySQL | 8.0+ | 关系型数据库 |
| mysql-connector-python | 8.0+ | MySQL 数据库驱动 |
| Tkinter | 内置 | GUI 框架 |

---

## 系统架构

本项目采用**三层架构**设计模式：

```
┌─────────────────────────────────┐
│       UI 层 (表现层)              │  负责用户交互和界面展示
│  login_ui / teacher_ui / ...    │
└────────────────┬────────────────┘
                 │ 调用
┌─────────────────────────────────┐
│    Service 层 (业务逻辑层)        │  负责业务规则和数据处理
│  auth_service / score_service   │
└────────────────┬────────────────┘
                 │ 调用
┌─────────────────────────────────┐
│      DAO 层 (数据访问层)          │  负责数据库操作
│  user_dao / score_dao / db      │
└────────────────┬────────────────┘
                 │ 访问
┌─────────────────────────────────┐
│        MySQL 数据库              │  数据存储层
└─────────────────────────────────┘
```

**架构优势：**
- 层次清晰，职责分离
- 便于单元测试和集成测试
- 易于功能扩展和维护
- 支持代码复用

---

## 快速开始

### 1. 克隆或下载项目

```bash
# 使用 Git 克隆（若项目在远程仓库）
git clone <repository-url>
cd student_grade_system

# 或直接进入项目目录
cd student_grade_system
```

### 2. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置数据库连接

```bash
# 复制配置模板
cp .env.example .env
```

编辑 `.env` 文件，填入数据库配置信息。

### 5. 初始化数据库

```bash
mysql -h localhost -u root -p student_grade_system < init_database.sql
```

### 6. 启动应用

```bash
python main.py
```

**默认测试账号：**
- 管理员：`admin001` / `123456`
- 教师：`t2024001` / `123456`
- 学生：`s20220101` / `123456`

---

## 环境要求

### 系统要求

- **操作系统**：Windows 7+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **处理器**：Intel i5 及以上或同等级处理器
- **内存**：4GB 及以上（推荐 8GB）
- **硬盘**：100MB 空闲空间

### 软件要求

| 软件 | 最低版本 | 推荐版本 |
|------|---------|---------|
| Python | 3.8 | 3.10+ |
| MySQL | 8.0.0 | 8.0.28+ |
| pip | 21.0 | 最新版本 |

### 检查环境

```bash
# 检查 Python 版本
python --version

# 检查 MySQL 是否安装
mysql --version

# 检查 pip 版本
pip --version
```

---

## 安装步骤

### 第一步：准备 Python 环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 第二步：安装依赖包

```bash
# 升级 pip（可选但推荐）
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

生成 requirements.txt：
```bash
pip freeze > requirements.txt
```

### 第三步：配置数据库

**步骤 3.1：创建数据库和用户**

```bash
mysql -h localhost -u root -p
```

在 MySQL 命令行中执行：

```sql
-- 创建数据库
CREATE DATABASE student_grade_system 
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

-- 创建用户（安全性考虑）
CREATE USER 'sgs_user'@'localhost' IDENTIFIED BY 'strong_password_here';

-- 授予权限
GRANT ALL PRIVILEGES ON student_grade_system.* TO 'sgs_user'@'localhost';
FLUSH PRIVILEGES;
```

**步骤 3.2：初始化表和数据**

```bash
mysql -h localhost -u sgs_user -p student_grade_system < init_database.sql
```

**步骤 3.3：配置应用**

创建 `.env` 文件（复制 `.env.example`）：

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=sgs_user
DB_PASSWORD=strong_password_here
DB_DATABASE=student_grade_system
DB_CHARSET=utf8mb4

# 应用配置
DEBUG=False
LOG_LEVEL=INFO
```

修改 [dao/db.py](dao/db.py) 中的数据库连接代码以读取环境变量：

```python
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_DATABASE', 'student_grade_system'),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4')
}
```

### 第四步：启动应用

```bash
# 确保虚拟环境已激活
python main.py
```

---

## 项目结构

```
student_grade_system/
├── main.py                      # 程序入口，启动登录界面
├── requirements.txt             # 项目依赖清单
├── .env.example                 # 环境变量配置模板
├── README.md                    # 项目文档
├── init_database.sql            # 数据库初始化脚本
│
├── dao/                         # 数据访问层 (Data Access Object)
│   ├── __init__.py             # 包初始化
│   ├── db.py                   # 数据库连接管理类 DBConnection
│   │                           # - 负责数据库连接的创建和关闭
│   │                           # - 提供数据库操作的基础方法
│   ├── user_dao.py             # 用户数据访问对象 UserDAO
│   │                           # - 用户的增删改查
│   │                           # - 权限验证
│   └── score_dao.py            # 成绩数据访问对象 ScoreDAO
│                               # - 成绩的增删改查
│                               # - 成绩统计查询
│
├── service/                     # 业务逻辑层 (Service)
│   ├── __init__.py             # 包初始化
│   ├── auth_service.py         # 认证服务 AuthService
│   │                           # - 用户身份验证
│   │                           # - 权限检查
│   │                           # - 登录状态管理
│   └── score_service.py        # 成绩服务 ScoreService
│                               # - 成绩计算（自动计算总评、绩点）
│                               # - 成绩统计
│                               # - 数据验证
│
└── ui/                          # 表现层 (User Interface)
    ├── __init__.py             # 包初始化
    ├── login_ui.py             # 登录界面
    │                           # - 用户身份验证入口
    │                           # - 基于角色的界面路由
    ├── teacher_ui.py           # 教师功能界面
    │                           # - 成绩录入/查询/修改
    │                           # - 成绩统计和报表导出
    ├── student_ui.py           # 学生功能界面
    │                           # - 成绩查询
    │                           # - 成绩统计
    └── admin_ui.py             # 管理员功能界面
                                # - 用户管理
                                # - 系统参数设置
                                # - 数据备份
```

---

## 功能说明

### 👨‍🏫 教师功能

| 功能 | 说明 |
|------|------|
| **成绩录入** | 支持平时、期中、期末成绩录入，系统自动计算总评和绩点 |
| **成绩查询** | 按学生查询，按科目查询，支持多条件组合查询 |
| **成绩修改** | 修改已录入的成绩，自动重新计算相关统计数据 |
| **成绩统计** | 计算平均分、最高分、最低分、及格率等统计指标 |
| **报表导出** | 将成绩导出为 CSV 格式，便于后续分析 |

**成绩计算公式：**
```
总评 = 平时成绩 × 30% + 期中成绩 × 30% + 期末成绩 × 40%
绩点 = {
    4.0,  if 总评 >= 90
    3.6,  if 总评 >= 80
    3.3,  if 总评 >= 75
    2.8,  if 总评 >= 70
    ...
}
```

### 📚 学生功能

| 功能 | 说明 |
|------|------|
| **成绩查询** | 查询个人所有课程的成绩明细（平时、期中、期末、总评） |
| **成绩统计** | 查看平均分、绩点平均值、学分等综合统计数据 |

### 👨‍💼 管理员功能

| 功能 | 说明 |
|------|------|
| **用户管理** | 添加新用户、禁用/启用用户、删除用户账号 |
| **权限管理** | 分配用户角色（管理员、教师、学生） |
| **系统配置** | 设置成绩计算权重、及格线等系统参数 |
| **数据备份** | 备份数据库为 SQL 脚本，便于恢复和迁移 |

---

## API 和模块说明

### auth_service.py - 认证服务

**主要方法：**

```python
class AuthService:
    def login(username, password) -> bool
        # 验证用户身份，返回登录是否成功
    
    def get_user_role(user_id) -> str
        # 获取用户角色（admin/teacher/student）
    
    def verify_permission(user_id, action) -> bool
        # 验证用户是否有权执行特定操作
```

### score_service.py - 成绩服务

**主要方法：**

```python
class ScoreService:
    def calculate_total_score(usual, midterm, final) -> float
        # 计算总评成绩
    
    def calculate_grade_point(total_score) -> float
        # 根据总评计算绩点
    
    def get_statistics(scores) -> dict
        # 计算成绩统计（平均、最高、最低等）
```

### user_dao.py - 用户数据访问

```python
class UserDAO:
    def get_user(user_id) -> User
    def create_user(user_data) -> bool
    def update_user(user_id, user_data) -> bool
    def delete_user(user_id) -> bool
    def authenticate(username, password) -> User | None
```

### score_dao.py - 成绩数据访问

```python
class ScoreDAO:
    def insert_score(score_data) -> bool
    def update_score(score_id, score_data) -> bool
    def get_score(score_id) -> Score
    def query_scores(filters) -> List[Score]
    def export_to_csv(filename) -> bool
```

---

## 数据库说明

### 数据库初始化

系统使用 [init_database.sql](init_database.sql) 进行初始化，包括：
- 创建用户表
- 创建成绩表
- 创建系统参数表
- 初始化默认数据和索引

### 主要数据表

**users 表**（用户表）
```sql
- user_id (主键)
- username (唯一索引)
- password (加密存储)
- role (角色：admin/teacher/student)
- status (账户状态：active/disabled)
```

**scores 表**（成绩表）
```sql
- score_id (主键)
- student_id (外键→users)
- teacher_id (外键→users)
- course_name (课程名称)
- usual_score (平时成绩)
- midterm_score (期中成绩)
- final_score (期末成绩)
- total_score (总评)
- grade_point (绩点)
- created_at (创建时间)
- updated_at (更新时间)
```

**sys_config 表**（系统配置表）
```sql
- config_id (主键)
- config_key (配置键)
- config_value (配置值)
```

---

## 安全性

### 密码管理 ⚠️

- **不要**在代码中硬编码密码
- 使用环境变量或 `.env` 文件存储敏感信息
- 数据库密码建议使用强密码（至少 12 位，包含大小写字母、数字、特殊字符）

### 示例配置

```python
# ✅ 正确做法
import os
from dotenv import load_dotenv

load_dotenv()
password = os.getenv('DB_PASSWORD')

# ❌ 错误做法
password = '159298687187xxx'  # 不要这样做！
```

### 其他安全建议

- ✅ 定期更换测试账户密码（生产环境）
- ✅ 使用 HTTPS 传输数据（如有网络通信）
- ✅ 实施日志记录，记录所有重要操作
- ✅ 定期备份数据库
- ✅ 限制数据库用户权限（不要使用 root 账户）
- ✅ 对用户输入进行验证和清理

---

## 开发指南

### 代码规范

#### 命名规范

```python
# 类名：大驼峰命名
class UserDAO:
    pass

# 函数/方法：小驼峰命名
def getUserInfo():
    pass

# 常量：全大写
DB_HOST = 'localhost'
MAX_RETRY_COUNT = 3

# 变量：小驼峰命名
userName = 'admin'
```

#### 代码风格

遵循 [PEP 8](https://pep8.org/) 规范：

```python
# 函数定义前后两个空行
def function_one():
    pass


def function_two():
    pass

# 类定义前后两个空行，方法定义前一个空行
class MyClass:
    def method_one(self):
        pass

    def method_two(self):
        pass
```

### 添加新功能

步骤 1：在 DAO 层添加数据库操作
```python
# dao/new_dao.py
class NewDAO:
    def create(self, data):
        pass
```

步骤 2：在 Service 层添加业务逻辑
```python
# service/new_service.py
class NewService:
    def process(self, data):
        pass
```

步骤 3：在 UI 层添加界面
```python
# ui/new_ui.py
def show_new_interface():
    pass
```

### 运行测试

```bash
# 单元测试
python -m unittest discover -s tests -p "test_*.py"
```

### 提交代码

```bash
# 遵循 Git 提交规范
git add .
git commit -m "feat: 描述新增功能"
git commit -m "fix: 修复某个 bug"
git commit -m "docs: 更新文档"
```

---

## 故障排查

### 常见问题

#### Q1: 无法连接数据库

**症状：** `"No module named 'mysql.connector'"`

**解决方案：**
```bash
# 确保依赖已安装
pip install mysql-connector-python

# 重新运行应用
python main.py
```

#### Q2: MySQL 拒绝连接

**症状：** `"Access denied for user 'root'@'localhost'"`

**解决方案：**
- 检查数据库用户名和密码是否正确
- 确保 MySQL 服务正在运行
- 确认 `.env` 文件中的配置无误

```bash
# 验证 MySQL 服务状态
mysql -h localhost -u root -p -e "SELECT 1;"
```

#### Q3: 数据库初始化失败

**症状：** `"ERROR 1007 (HY000): Can't create database"`

**解决方案：**
```bash
# 检查数据库是否已存在
mysql -u root -p -e "SHOW DATABASES LIKE 'student_grade_system';"

# 如果存在，可选择删除后重建
mysql -u root -p -e "DROP DATABASE student_grade_system;"
mysql -u root -p student_grade_system < init_database.sql
```

#### Q4: 界面无法显示

**症状：** 运行后没有看到 GUI 窗口

**解决方案：**
- 检查是否安装了 Tkinter（通常随 Python 一起安装）
- 在 Linux 系统上，可能需要单独安装：`sudo apt-get install python3-tk`
- 检查 [main.py](main.py) 中的入口代码

#### Q5: 性能问题

**症状：** 查询成绩时响应缓慢

**解决方案：**
- 检查数据库索引是否已创建（见 init_database.sql）
- 优化查询条件，避免全表扫描
- 添加必要的数据库索引

```sql
-- 在 scores 表上添加索引
CREATE INDEX idx_student_id ON scores(student_id);
CREATE INDEX idx_teacher_id ON scores(teacher_id);
```

### 获取帮助

- 查看应用日志文件（如有）
- 检查 MySQL 日志：`/var/log/mysql/error.log`
- 在数据库管理工具中手动执行查询，验证数据

---

## 许可证

本项目采用 [MIT License](LICENSE) 许可证。

---

## 更新日志

### v1.0.0 (2026-06-03)
- ✅ 完成核心功能开发
- ✅ 实现三层架构设计
- ✅ 支持多角色权限管理

---

## 联系方式

如有问题或建议，欢迎提交 [Issue](../../issues) 或 [Pull Request](../../pulls)。

**项目维护者：** [Your Name/Team]  
**联系邮箱：** [contact@example.com]

---

**最后更新：** 2024 年  
**文档版本：** 1.0.0
