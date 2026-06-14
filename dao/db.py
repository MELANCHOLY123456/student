"""
MySQL数据库连接类 - DBConnection
支持上下文管理器、异常处理、参数化查询
依赖: pip install mysql-connector-python
"""

import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Optional, Union, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DBConnection:
    """
    MySQL数据库连接类

    功能:
    - 连接/断开数据库
    - 执行查询操作（SELECT）
    - 执行增删改操作（INSERT/UPDATE/DELETE）
    - 支持上下文管理器（with语句）
    - 完整的异常处理和日志记录
    """

    def __init__(
        self,
        host: str = 'localhost',
        port: int = 3306,
        user: str = 'root',
        password: str = '15929867187xxx',
        database: str = 'student_grade_system',
        charset: str = 'utf8mb4'
    ):
        """
        初始化数据库连接参数

        Args:
            host: 数据库主机地址，默认 'localhost'
            port: 数据库端口，默认 3306
            user: 数据库用户名
            password: 数据库密码
            database: 数据库名称
            charset: 字符集，默认 'utf8mb4'
        """
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': '15929867187xxx',
            'database': database,
            'charset': charset,
            'autocommit': False
        }
        self._conn = None
        self._cursor = None

    def connect(self) -> bool:
        """
        建立数据库连接

        Returns:
            bool: 连接成功返回True，失败返回False
        """
        try:
            if self._conn is not None and self._conn.is_connected():
                logger.warning("数据库连接已存在")
                return True

            self._conn = mysql.connector.connect(**self.config)
            self._cursor = self._conn.cursor(dictionary=True)
            logger.info(f"数据库连接成功: {self.config['database']}@{self.config['host']}")
            return True

        except Error as e:
            logger.error(f"数据库连接失败: {e}")
            self._conn = None
            self._cursor = None
            return False

    def execute_query(
        self,
        sql: str,
        params: Optional[Union[Tuple, Dict]] = None
    ) -> List[Dict[str, Any]]:
        """
        执行查询操作（SELECT）

        Args:
            sql: SQL查询语句，使用 %s 作为占位符
            params: 查询参数，防止SQL注入

        Returns:
            List[Dict]: 查询结果列表，每条记录为字典格式
        """
        if not self._ensure_connected():
            return []

        try:
            self._cursor.execute(sql, params or ())
            result = self._cursor.fetchall()
            logger.debug(f"查询成功，返回 {len(result)} 条记录")
            return result

        except Error as e:
            logger.error(f"查询执行失败: {e}, SQL: {sql}, 参数: {params}")
            return []

    def execute_update(
        self,
        sql: str,
        params: Optional[Union[Tuple, List[Tuple], Dict]] = None,
        batch: bool = False
    ) -> int:
        """
        执行增删改操作（INSERT/UPDATE/DELETE）

        Args:
            sql: SQL语句
            params: 操作参数
            batch: 是否批量操作

        Returns:
            int: 影响的行数
        """
        if not self._ensure_connected():
            return 0

        try:
            if batch and isinstance(params, list):
                self._cursor.executemany(sql, params)
            else:
                self._cursor.execute(sql, params or ())

            affected_rows = self._cursor.rowcount
            self._conn.commit()
            logger.info(f"更新成功，影响 {affected_rows} 行")
            return affected_rows

        except Error as e:
            self._conn.rollback()
            logger.error(f"更新执行失败: {e}, SQL: {sql}")
            return 0

    def _ensure_connected(self) -> bool:
        """确保数据库已连接"""
        if self._conn is None or not self._conn.is_connected():
            logger.warning("连接已断开，尝试重新连接...")
            return self.connect()
        return True

    def close(self) -> None:
        """关闭数据库连接"""
        try:
            if self._cursor:
                self._cursor.close()
            if self._conn:
                self._conn.close()
            logger.info("数据库连接已关闭")
        except Error as e:
            logger.error(f"关闭连接时发生错误: {e}")
        finally:
            self._cursor = None
            self._conn = None

    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if exc_type is not None:
            self._conn.rollback() if self._conn else None
        else:
            self._conn.commit() if self._conn else None
        self.close()
        return False

    def __del__(self):
        """析构函数"""
        self.close()


# =====================================================
# 数据库配置（请根据您的环境修改）
# =====================================================
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'Tt1751868410',  # ← 请修改为您的MySQL密码
    'database': 'student_grade_system',
    'charset': 'utf8mb4'
}
