#!/usr/bin/env python3
"""
系统诊断和初始化脚本
用于诊断数据库连接问题并帮助初始化系统
"""

import os
import sys
import subprocess
from pathlib import Path


def check_env_file():
    """检查 .env 文件"""
    print("\n" + "=" * 60)
    print("1️⃣ 检查 .env 文件")
    print("=" * 60)
    
    if os.path.exists('.env'):
        print("✅ .env 文件存在")
        with open('.env', 'r') as f:
            content = f.read()
            if 'DB_PASSWORD' in content and not content.strip().endswith('='):
                print("✅ .env 文件已配置")
                return True
            else:
                print("❌ .env 文件未完整配置")
                return False
    else:
        print("❌ .env 文件不存在")
        print("\n📋 需要创建 .env 文件，请选择:")
        print("1. 使用默认配置自动创建")
        print("2. 手动输入配置")
        
        choice = input("\n请选择 (1/2): ").strip()
        if choice == '1':
            create_env_auto()
            return True
        elif choice == '2':
            create_env_manual()
            return True
        else:
            print("❌ 取消操作")
            return False


def create_env_auto():
    """使用默认配置自动创建 .env"""
    print("\n正在创建 .env 文件...")
    
    env_content = """# ========================================
# 学生成绩管理系统 - 环境变量配置
# ========================================

# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=student_grade_system
DB_CHARSET=utf8mb4

# 应用配置
DEBUG=False
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env 文件已创建")
    print("\n⚠️ 请编辑 .env 文件，填入数据库密码:")
    print("   DB_PASSWORD=your_mysql_password")


def create_env_manual():
    """手动输入配置创建 .env"""
    print("\n请输入数据库配置:")
    
    host = input("数据库主机 (localhost): ").strip() or "localhost"
    port = input("数据库端口 (3306): ").strip() or "3306"
    user = input("数据库用户 (root): ").strip() or "root"
    password = input("数据库密码: ").strip()
    dbname = input("数据库名称 (student_grade_system): ").strip() or "student_grade_system"
    
    env_content = f"""# ========================================
# 学生成绩管理系统 - 环境变量配置
# ========================================

# 数据库配置
DB_HOST={host}
DB_PORT={port}
DB_USER={user}
DB_PASSWORD={password}
DB_NAME={dbname}
DB_CHARSET=utf8mb4

# 应用配置
DEBUG=False
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env 文件已创建")


def check_mysql_service():
    """检查 MySQL 服务"""
    print("\n" + "=" * 60)
    print("2️⃣ 检查 MySQL 服务")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ['mysql', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ MySQL 已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ 无法验证 MySQL")
            return False
    except FileNotFoundError:
        print("❌ MySQL 不在 PATH 中")
        print("   请确保 MySQL 已安装并添加到系统 PATH")
        return False
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False


def check_database_connection():
    """检查数据库连接"""
    print("\n" + "=" * 60)
    print("3️⃣ 检查数据库连接")
    print("=" * 60)
    
    try:
        from config import Config
        Config.validate()
        print("✅ 配置验证通过")
        
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )
            
            if conn.is_connected():
                print(f"✅ 已连接到 MySQL: {Config.DB_HOST}:{Config.DB_PORT}")
                
                # 检查数据库是否存在
                cursor = conn.cursor()
                cursor.execute(f"SHOW DATABASES LIKE '{Config.DB_NAME}'")
                result = cursor.fetchone()
                
                if result:
                    print(f"✅ 数据库 '{Config.DB_NAME}' 存在")
                    
                    # 检查表是否存在
                    cursor.execute(f"USE {Config.DB_NAME}")
                    cursor.execute("SHOW TABLES LIKE 'user'")
                    if cursor.fetchone():
                        print("✅ 用户表存在")
                        return True
                    else:
                        print("❌ 用户表不存在，需要初始化数据库")
                        return False
                else:
                    print(f"❌ 数据库 '{Config.DB_NAME}' 不存在")
                    return False
            
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False
            
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        return False


def initialize_database():
    """初始化数据库"""
    print("\n" + "=" * 60)
    print("4️⃣ 初始化数据库")
    print("=" * 60)
    
    from config import Config
    
    if not os.path.exists('init_database.sql'):
        print("❌ init_database.sql 文件不存在")
        return False
    
    try:
        print("正在执行 SQL 初始化脚本...")
        
        # 构建 mysql 命令
        cmd = [
            'mysql',
            '-h', Config.DB_HOST,
            '-P', str(Config.DB_PORT),
            '-u', Config.DB_USER,
            f'-p{Config.DB_PASSWORD}',
            '-e',
            f'source init_database.sql'
        ]
        
        # 执行命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ 数据库初始化成功")
            print("\n初始化后的数据库状态:")
            print("- 用户表: 5条记录")
            print("- 学生表: 3条记录")
            print("- 科目表: 3条记录")
            print("- 成绩表: 5条记录")
            print("\n默认账号:")
            print("  管理员: admin001 / 123456")
            print("  教师:   t2024001 / 123456")
            print("  学生:   s20220101 / 123456")
            return True
        else:
            print(f"❌ 初始化失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 初始化出错: {e}")
        return False


def main():
    """主程序"""
    print("\n" + "=" * 60)
    print("🔧 学生成绩管理系统 - 诊断和初始化工具")
    print("=" * 60)
    
    # 第一步：检查 .env 文件
    if not check_env_file():
        print("\n❌ 诊断中止")
        return 1
    
    # 第二步：检查 MySQL 服务
    if not check_mysql_service():
        print("\n⚠️ 警告: MySQL 可能未正确安装或配置")
    
    # 第三步：检查数据库连接
    if not check_database_connection():
        print("\n❓ 数据库连接失败或数据库未初始化")
        
        # 询问是否初始化数据库
        choice = input("\n是否现在初始化数据库? (y/n): ").strip().lower()
        if choice == 'y':
            if initialize_database():
                print("\n✅ 所有问题已解决！")
                print("现在可以运行: python main.py")
                return 0
            else:
                print("\n❌ 数据库初始化失败")
                return 1
        else:
            print("\n❌ 无法继续")
            return 1
    else:
        print("\n✅ 所有检查通过！")
        print("现在可以运行: python main.py")
        return 0


if __name__ == '__main__':
    sys.exit(main())
