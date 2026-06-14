"""
AuthService - 用户认证服务
实现用户登录验证，返回用户角色
"""

from dao.user_dao import UserDAO
from typing import Optional, Dict, Any


class AuthService:
    """
    用户认证服务

    职责:
    - 用户登录验证
    - 密码加密验证（bcrypt）
    - 返回用户角色和基本信息
    """

    def __init__(self):
        """初始化认证服务"""
        self.user_dao = UserDAO()

    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        用户登录验证

        Args:
            username: 用户名
            password: 密码（明文）

        Returns:
            Dict: 登录成功返回用户信息，包含:
                - user_id: 用户ID
                - username: 用户名
                - role: 角色（admin/teacher/student）
                - real_name: 真实姓名
            None: 登录失败（用户名不存在或密码错误）

        示例:
            >>> auth = AuthService()
            >>> result = auth.login("t2024001", "123456")
            >>> print(result)
            {'user_id': 2, 'username': 't2024001', 'role': 'teacher', 'real_name': '张教授'}
        """
        # 调用DAO验证用户名密码
        user = self.user_dao.find_by_username_password(username, password)

        if user is None:
            return None

        # 返回用户基本信息（不包含密码）
        return {
            'user_id': user['user_id'],
            'username': user['username'],
            'role': user['role'],
            'real_name': user['real_name']
        }

    def check_role(self, username: str) -> Optional[str]:
        """
        查询用户角色

        Args:
            username: 用户名

        Returns:
            str: 角色名称（admin/teacher/student）
            None: 用户不存在
        """
        user = self.user_dao.find_by_username(username)
        return user['role'] if user else None

    def has_permission(self, username: str, required_role: str) -> bool:
        """
        检查用户是否有指定角色权限

        Args:
            username: 用户名
            required_role: 要求的角色

        Returns:
            bool: 有权限返回True
        """
        user_role = self.check_role(username)

        if user_role is None:
            return False

        # 角色权限层级: admin > teacher > student
        role_levels = {
            'admin': 3,
            'teacher': 2,
            'student': 1
        }

        user_level = role_levels.get(user_role, 0)
        required_level = role_levels.get(required_role, 0)

        return user_level >= required_level
