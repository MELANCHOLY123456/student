"""
应用配置管理模块
从环境变量读取敏感配置，确保安全性
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()


class Config:
    """应用配置类"""

    # 数据库配置
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')  # ⚠️ 必须从 .env 提供
    DB_NAME = os.getenv('DB_NAME', 'student_grade_system')
    DB_CHARSET = os.getenv('DB_CHARSET', 'utf8mb4')

    # 应用配置
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # 日志配置
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')

    @staticmethod
    def get_db_config() -> dict:
        """
        获取数据库配置字典

        Returns:
            dict: MySQL连接配置
        """
        return {
            'host': Config.DB_HOST,
            'port': Config.DB_PORT,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD,
            'database': Config.DB_NAME,
            'charset': Config.DB_CHARSET
        }

    @staticmethod
    def validate():
        """验证必需的配置项"""
        if not Config.DB_PASSWORD:
            raise ValueError(
                "❌ 数据库密码未配置！\n"
                "请创建 .env 文件并设置 DB_PASSWORD\n"
                "参考 .env.example 文件的格式"
            )
        print("✅ 配置验证通过")
