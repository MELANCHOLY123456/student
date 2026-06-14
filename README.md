# 学生成绩管理系统

## 项目结构

```
student_grade_system/
├── main.py              # 程序入口，启动登录界面
├── dao/                 # 数据访问层
│   ├── __init__.py
│   ├── db.py            # 数据库连接类 DBConnection
│   ├── user_dao.py      # 用户数据访问对象 UserDAO
│   └── score_dao.py     # 成绩数据访问对象 ScoreDAO
├── service/             # 业务逻辑层
│   ├── __init__.py
│   ├── auth_service.py  # 认证服务 AuthService
│   └── score_service.py # 成绩服务 ScoreService
└── ui/                  # 表现层
    ├── __init__.py
    ├── login_ui.py      # 登录界面
    ├── teacher_ui.py    # 教师界面
    ├── student_ui.py    # 学生界面
    └── admin_ui.py      # 管理员界面
```

## 环境要求

- Python 3.8+
- MySQL 8.0+
- 依赖包: mysql-connector-python

## 安装依赖

```bash
pip install mysql-connector-python
```

## 数据库配置

修改 `dao/db.py` 中的 `DB_CONFIG`：

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '你的密码',  # ← 修改这里
    'database': 'student_grade_system',
    'charset': 'utf8mb4'
}
```

## 运行程序

```bash
cd student_grade_system
python main.py
```

## 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin001 | 123456 |
| 教师 | t2024001 | 123456 |
| 学生 | s20220101 | 123456 |

## 功能说明

### 教师功能
- 成绩录入（平时/期中/期末，自动计算总评和绩点）
- 成绩查询（按学生/按科目）
- 成绩修改
- 成绩统计（平均分/最高分/最低分/及格率）
- 导出报表（CSV格式）

### 学生功能
- 查询个人成绩明细
- 总成绩统计（平均分/绩点/学分）

### 管理员功能
- 用户管理（添加/禁用/删除）
- 系统参数设置（成绩权重）
- 数据备份（SQL导出）
