"""
应用常量定义
集中管理所有魔法字符串和常数
"""

# =====================================================
# 用户相关常量
# =====================================================

class UserRole:
    """用户角色"""
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'

    ALL_ROLES = [ADMIN, TEACHER, STUDENT]


class UserStatus:
    """用户账户状态"""
    ACTIVE = 1
    DISABLED = 0

    STATUS_MAP = {
        ACTIVE: '启用',
        DISABLED: '禁用'
    }


# =====================================================
# 成绩相关常量
# =====================================================

class ScoreStatus:
    """成绩状态"""
    DRAFT = 'draft'              # 草稿
    SUBMITTED = 'submitted'      # 已提交
    APPROVED = 'approved'        # 已审核
    REJECTED = 'rejected'        # 已拒绝

    ALL_STATUSES = [DRAFT, SUBMITTED, APPROVED, REJECTED]

    STATUS_MAP = {
        DRAFT: '草稿',
        SUBMITTED: '已提交',
        APPROVED: '已审核',
        REJECTED: '已拒绝'
    }


class GradeLevel:
    """绩点等级"""
    A = 4.0
    A_MINUS = 3.6
    B_PLUS = 3.3
    B = 3.0
    B_MINUS = 2.8
    C_PLUS = 2.5
    C = 2.0
    C_MINUS = 1.5
    D = 1.0
    F = 0.0


class ScoreCalculation:
    """成绩计算相关常数"""
    # 成绩权重（默认值）
    DAILY_WEIGHT = 0.30      # 平时成绩权重 30%
    MIDTERM_WEIGHT = 0.30    # 期中成绩权重 30%
    FINAL_WEIGHT = 0.40      # 期末成绩权重 40%

    # 及格线
    PASS_SCORE = 60

    # 成绩范围
    MIN_SCORE = 0
    MAX_SCORE = 100

    # 绩点计算规则 (总评分数 -> 绩点)
    GRADE_POINT_RULES = [
        (90, 4.0),   # >= 90 -> 4.0
        (80, 3.6),   # >= 80 -> 3.6
        (75, 3.3),   # >= 75 -> 3.3
        (70, 3.0),   # >= 70 -> 3.0
        (67, 2.8),   # >= 67 -> 2.8
        (64, 2.5),   # >= 64 -> 2.5
        (60, 2.0),   # >= 60 -> 2.0
        (0, 0.0),    # <  60 -> 0.0
    ]


# =====================================================
# 验证相关常量
# =====================================================

class ValidationRules:
    """数据验证规则"""
    # 用户名长度
    USERNAME_MIN_LENGTH = 3
    USERNAME_MAX_LENGTH = 20

    # 密码长度
    PASSWORD_MIN_LENGTH = 6
    PASSWORD_MAX_LENGTH = 20

    # 真实姓名长度
    REAL_NAME_MAX_LENGTH = 50

    # 学生ID范围
    STUDENT_ID_MIN = 1
    STUDENT_ID_MAX = 999999

    # 成绩范围验证消息
    INVALID_SCORE_RANGE = f"成绩必须在 {ScoreCalculation.MIN_SCORE} 到 {ScoreCalculation.MAX_SCORE} 之间"
    INVALID_SCORE_TYPE = "成绩必须是数字"


# =====================================================
# 错误消息常量
# =====================================================

class ErrorMessage:
    """统一的错误消息"""
    # 数据库错误
    DB_CONNECTION_FAILED = "❌ 数据库连接失败"
    DB_QUERY_FAILED = "❌ 数据库查询失败"
    DB_UPDATE_FAILED = "❌ 数据库更新失败"

    # 用户相关
    USER_NOT_FOUND = "❌ 用户不存在"
    USER_DISABLED = "❌ 账户已被禁用"
    INVALID_CREDENTIALS = "❌ 用户名或密码错误"
    USERNAME_EXISTS = "❌ 用户名已存在"

    # 成绩相关
    SCORE_NOT_FOUND = "❌ 成绩不存在"
    INVALID_SCORE = "❌ 成绩无效"

    # 权限相关
    PERMISSION_DENIED = "❌ 没有权限执行此操作"

    # 输入验证
    INVALID_INPUT = "❌ 输入信息无效"
    MISSING_REQUIRED_FIELD = "❌ 缺少必填字段"


# =====================================================
# 成功消息常量
# =====================================================

class SuccessMessage:
    """统一的成功消息"""
    OPERATION_SUCCESS = "✅ 操作成功"
    USER_LOGIN_SUCCESS = "✅ 登录成功"
    USER_CREATED = "✅ 用户创建成功"
    USER_UPDATED = "✅ 用户信息已更新"
    USER_DELETED = "✅ 用户已删除"

    SCORE_CREATED = "✅ 成绩已录入"
    SCORE_UPDATED = "✅ 成绩已更新"
    SCORE_DELETED = "✅ 成绩已删除"
