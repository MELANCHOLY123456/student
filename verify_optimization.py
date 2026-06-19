#!/usr/bin/env python3
"""
代码优化验证脚本
用于验证所有的代码优化是否已正确实施
"""

import os
import sys
from pathlib import Path


def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - 文件不存在")
        return False


def check_file_content(file_path, search_string, description, should_exist=True):
    """检查文件中是否包含/不包含特定内容"""
    if not os.path.exists(file_path):
        print(f"❌ {description}: 文件 {file_path} 不存在")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if should_exist:
        if search_string in content:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description}: 未找到 '{search_string}'")
            return False
    else:
        if search_string not in content:
            print(f"✅ {description}: 已移除")
            return True
        else:
            print(f"❌ {description}: 仍然包含 '{search_string}'")
            return False


def main():
    """运行所有验证检查"""
    print("\n" + "=" * 60)
    print("📋 代码优化验证报告")
    print("=" * 60 + "\n")
    
    checks = []
    
    # ===== 文件存在检查 =====
    print("📁 新增文件检查：\n")
    checks.append(check_file_exists("config.py", "配置管理文件"))
    checks.append(check_file_exists("constants.py", "常量定义文件"))
    checks.append(check_file_exists("logging_config.py", "日志配置文件"))
    checks.append(check_file_exists(".env.example", "环境变量模板"))
    checks.append(check_file_exists(".gitignore", "Git忽略配置"))
    checks.append(check_file_exists("requirements.txt", "依赖列表"))
    checks.append(check_file_exists("OPTIMIZATION_REPORT.md", "优化报告"))
    
    # ===== 安全性检查 =====
    print("\n🔒 安全性检查：\n")
    checks.append(check_file_content(
        "dao/db.py", 
        "NullHandler",
        "db.py 已使用 NullHandler",
        should_exist=True
    ))
    checks.append(check_file_content(
        "dao/db.py",
        "15929867187xxx",
        "db.py 已移除硬编码密码",
        should_exist=False
    ))
    checks.append(check_file_content(
        "dao/db.py",
        "DB_CONFIG = {",
        "db.py 已移除 DB_CONFIG 硬编码",
        should_exist=False
    ))
    checks.append(check_file_content(
        "dao/user_dao.py",
        "print(f\"[DEBUG]",
        "user_dao.py 已移除 debug print 语句",
        should_exist=False
    ))
    
    # ===== 规范性检查 =====
    print("\n📐 代码规范检查：\n")
    checks.append(check_file_content(
        "dao/score_dao.py",
        "ScoreStatus.SUBMITTED",
        "score_dao.py 已使用常量替代魔法字符串",
        should_exist=True
    ))
    checks.append(check_file_content(
        "dao/score_dao.py",
        "_validate_score_inputs",
        "score_dao.py 已添加输入验证方法",
        should_exist=True
    ))
    checks.append(check_file_content(
        "dao/user_dao.py",
        "_validate_credentials",
        "user_dao.py 已添加凭证验证方法",
        should_exist=True
    ))
    checks.append(check_file_content(
        "dao/score_dao.py",
        "logger.info",
        "score_dao.py 已添加日志记录",
        should_exist=True
    ))
    checks.append(check_file_content(
        "dao/user_dao.py",
        "logger.warning",
        "user_dao.py 已添加日志记录",
        should_exist=True
    ))
    
    # ===== 导入检查 =====
    print("\n📦 模块导入检查：\n")
    checks.append(check_file_content(
        "dao/score_dao.py",
        "from config import Config",
        "score_dao.py 已导入 Config",
        should_exist=True
    ))
    checks.append(check_file_content(
        "dao/score_dao.py",
        "from constants import",
        "score_dao.py 已导入常量",
        should_exist=True
    ))
    checks.append(check_file_content(
        "dao/user_dao.py",
        "from config import Config",
        "user_dao.py 已导入 Config",
        should_exist=True
    ))
    checks.append(check_file_content(
        "dao/user_dao.py",
        "from constants import",
        "user_dao.py 已导入常量",
        should_exist=True
    ))
    
    # ===== 常量定义检查 =====
    print("\n⚙️ 常量定义检查：\n")
    checks.append(check_file_content(
        "constants.py",
        "class UserRole:",
        "constants.py 已定义 UserRole",
        should_exist=True
    ))
    checks.append(check_file_content(
        "constants.py",
        "class ScoreStatus:",
        "constants.py 已定义 ScoreStatus",
        should_exist=True
    ))
    checks.append(check_file_content(
        "constants.py",
        "class ValidationRules:",
        "constants.py 已定义 ValidationRules",
        should_exist=True
    ))
    
    # ===== 配置检查 =====
    print("\n🔧 配置管理检查：\n")
    checks.append(check_file_content(
        "config.py",
        "class Config:",
        "config.py 已定义 Config 类",
        should_exist=True
    ))
    checks.append(check_file_content(
        "config.py",
        "def get_db_config()",
        "config.py 已定义 get_db_config 方法",
        should_exist=True
    ))
    checks.append(check_file_content(
        ".env.example",
        "DB_PASSWORD=",
        ".env.example 已包含配置模板",
        should_exist=True
    ))
    checks.append(check_file_content(
        ".gitignore",
        ".env",
        ".gitignore 已包含 .env 忽略规则",
        should_exist=True
    ))
    
    # ===== 汇总 =====
    print("\n" + "=" * 60)
    passed = sum(checks)
    total = len(checks)
    print(f"验证结果：{passed}/{total} 项检查通过")
    print("=" * 60 + "\n")
    
    if passed == total:
        print("🎉 所有优化已成功实施！\n")
        return 0
    else:
        print(f"⚠️ 还有 {total - passed} 项需要检查\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
