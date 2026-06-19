"""
UserDAO - 用户数据访问对象
实现用户登录验证、用户信息查询等功能
"""

from dao.db import DBConnection
from config import Config
from constants import UserStatus, UserRole, ValidationRules, ErrorMessage
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


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
        self.db_config = db_config or Config.get_db_config()

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
            本系统使用明文密码存储，仅用于教学演示
            生产环境应使用bcrypt等加密方式存储密码
        """
        # 输入验证
        if not self._validate_credentials(username, password):
            logger.warning(f"凭证验证失败: username={username}")
            return None

        with DBConnection(**self.db_config) as db:
            # 查询用户信息
            sql = """
                SELECT user_id, username, password, role, real_name, status 
                FROM user 
                WHERE username = %s AND status = %s
            """
            result = db.execute_query(sql, (username, UserStatus.ACTIVE))

            if not result:
                logger.warning(f"用户不存在或账号已禁用: username={username}")
                return None

            user = result[0]

            # 密码验证（明文比对）
            if user['password'] != password:
                logger.warning(f"密码验证失败: username={username}")
                return None

            # 返回用户信息（不包含密码）
            logger.info(f"用户登录成功: username={username}, role={user['role']}")
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
            if result:
                logger.debug(f"用户查询成功: username={username}")
            return result[0] if result else None

    def find_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """根据用户ID查询用户信息"""
        if user_id <= 0:
            logger.error(f"无效的用户ID: {user_id}")
            return None

        with DBConnection(**self.db_config) as db:
            sql = """
                SELECT user_id, username, role, real_name, status 
                FROM user 
                WHERE user_id = %s
            """
            result = db.execute_query(sql, (user_id,))
            if result:
                logger.debug(f"用户查询成功: user_id={user_id}")
            return result[0] if result else None

    def get_all_users(self) -> list:
        """获取所有用户列表"""
        with DBConnection(**self.db_config) as db:
            sql = """
                SELECT user_id, username, role, real_name, status, created_at 
                FROM user 
                ORDER BY user_id
            """
            result = db.execute_query(sql)
            logger.info(f"获取用户列表, 共 {len(result)} 条记录")
            return result

    def insert_user(self, username: str, password: str, role: str, real_name: str) -> int:
        """
        插入新用户（明文密码）

        Args:
            username: 用户名
            password: 密码
            role: 用户角色（admin/teacher/student）
            real_name: 真实姓名

        Returns:
            int: 影响行数，0表示插入失败
        """
        # 输入验证
        if not self._validate_user_data(username, password, role, real_name):
            logger.error(f"用户数据验证失败: username={username}, role={role}")
            return 0

        with DBConnection(**self.db_config) as db:
            sql = """
                INSERT INTO user (username, password, role, real_name, status) 
                VALUES (%s, %s, %s, %s, %s)
            """
            affected_rows = db.execute_update(sql, (username, password, role, real_name, UserStatus.ACTIVE))
            if affected_rows > 0:
                logger.info(f"新用户已创建: username={username}, role={role}")
            else:
                logger.error(f"用户创建失败: username={username}")
            return affected_rows

    def update_user_status(self, user_id: int, status: int) -> int:
        """
        更新用户状态

        Args:
            user_id: 用户ID
            status: 用户状态（1=启用, 0=禁用）

        Returns:
            int: 影响行数，0表示更新失败
        """
        # 输入验证
        if user_id <= 0:
            logger.error(f"无效的用户ID: {user_id}")
            return 0

        if status not in UserStatus.STATUS_MAP:
            logger.error(f"无效的用户状态: {status}")
            return 0

        with DBConnection(**self.db_config) as db:
            sql = "UPDATE user SET status = %s WHERE user_id = %s"
            affected_rows = db.execute_update(sql, (status, user_id))
            if affected_rows > 0:
                status_text = UserStatus.STATUS_MAP.get(status, '未知')
                logger.info(f"用户状态已更新: user_id={user_id}, status={status_text}")
            else:
                logger.warning(f"用户状态更新失败: user_id={user_id}")
            return affected_rows

    def delete_user(self, user_id: int) -> int:
        """删除用户"""
        with DBConnection(**self.db_config) as db:
            sql = "DELETE FROM user WHERE user_id = %s"
            return db.execute_update(sql, (user_id,))

    @staticmethod
    def _validate_credentials(username: str, password: str) -> bool:
        """
        验证用户名和密码的基本合法性

        Args:
            username: 用户名
            password: 密码

        Returns:
            bool: 验证通过返回True
        """
        # 检查用户名
        if not username or len(username) < ValidationRules.USERNAME_MIN_LENGTH:
            logger.warning(f"用户名过短: {len(username) if username else 0}")
            return False

        if len(username) > ValidationRules.USERNAME_MAX_LENGTH:
            logger.warning(f"用户名过长: {len(username)}")
            return False

        # 检查密码
        if not password or len(password) < ValidationRules.PASSWORD_MIN_LENGTH:
            logger.warning("密码过短")
            return False

        if len(password) > ValidationRules.PASSWORD_MAX_LENGTH:
            logger.warning("密码过长")
            return False

        return True

    @staticmethod
    def _validate_user_data(username: str, password: str, role: str, real_name: str) -> bool:
        """
        验证新用户数据的合法性

        Args:
            username: 用户名
            password: 密码
            role: 用户角色
            real_name: 真实姓名

        Returns:
            bool: 验证通过返回True
        """
        # 验证凭证
        if not UserDAO._validate_credentials(username, password):
            return False

        # 验证角色
        if role not in UserRole.ALL_ROLES:
            logger.warning(f"无效的用户角色: {role}")
            return False

        # 验证真实姓名
        if not real_name or len(real_name) > ValidationRules.REAL_NAME_MAX_LENGTH:
            logger.warning(f"无效的真实姓名长度: {len(real_name) if real_name else 0}")
            return False

        return True
