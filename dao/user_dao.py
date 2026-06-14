"""
UserDAO - 用户数据访问对象
实现用户登录验证、用户信息查询等功能
"""

from dao.db import DBConnection, DB_CONFIG
from typing import Optional, Dict, Any


class UserDAO:
    """
    用户数据访问对象

    职责:
    - 用户登录验证（明文密码比对）
    - 用户信息查询
    - 用户角色获取
    """

    def __init__(self, db_config: Optional[Dict[str, Any]] = None):
        """初始化UserDAO"""
        self.db_config = db_config or DB_CONFIG

    def find_by_username_password(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        根据用户名和密码验证用户登录

        Args:
            username: 用户名
            password: 密码（明文）

        Returns:
            Dict: 用户信息字典，包含user_id, username, role, real_name等
            None: 验证失败（用户名不存在或密码错误）

        注意:
            本系统使用明文密码存储，方便课程实验演示
            生产环境应使用bcrypt等加密方式
        """
        with DBConnection(**self.db_config) as db:
            # 查询用户信息
            sql = """
                SELECT user_id, username, password, role, real_name, status 
                FROM user 
                WHERE username = %s AND status = 1
            """
            result = db.execute_query(sql, (username,))

            if not result:
                print(f"[DEBUG] 用户名 '{username}' 不存在或账号被禁用")
                return None

            user = result[0]
            print(f"[DEBUG] 数据库中的密码: '{user['password']}', 输入的密码: '{password}'")

            # 明文密码比对
            if user['password'] != password:
                print(f"[DEBUG] 密码不匹配")
                return None

            # 返回用户信息（不包含密码）
            return {
                'user_id': user['user_id'],
                'username': user['username'],
                'role': user['role'],
                'real_name': user['real_name'],
                'status': user['status']
            }

    def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """根据用户名查询用户信息"""
        with DBConnection(**self.db_config) as db:
            sql = """
                SELECT user_id, username, role, real_name, status 
                FROM user 
                WHERE username = %s
            """
            result = db.execute_query(sql, (username,))
            return result[0] if result else None

    def find_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """根据用户ID查询用户信息"""
        with DBConnection(**self.db_config) as db:
            sql = """
                SELECT user_id, username, role, real_name, status 
                FROM user 
                WHERE user_id = %s
            """
            result = db.execute_query(sql, (user_id,))
            return result[0] if result else None

    def get_all_users(self) -> list:
        """获取所有用户列表"""
        with DBConnection(**self.db_config) as db:
            sql = """
                SELECT user_id, username, role, real_name, status, created_at 
                FROM user 
                ORDER BY user_id
            """
            return db.execute_query(sql)

    def insert_user(self, username: str, password: str, role: str, real_name: str) -> int:
        """插入新用户（明文密码）"""
        with DBConnection(**self.db_config) as db:
            sql = """
                INSERT INTO user (username, password, role, real_name) 
                VALUES (%s, %s, %s, %s)
            """
            return db.execute_update(sql, (username, password, role, real_name))

    def update_user_status(self, user_id: int, status: int) -> int:
        """更新用户状态"""
        with DBConnection(**self.db_config) as db:
            sql = "UPDATE user SET status = %s WHERE user_id = %s"
            return db.execute_update(sql, (status, user_id))

    def delete_user(self, user_id: int) -> int:
        """删除用户"""
        with DBConnection(**self.db_config) as db:
            sql = "DELETE FROM user WHERE user_id = %s"
            return db.execute_update(sql, (user_id,))
