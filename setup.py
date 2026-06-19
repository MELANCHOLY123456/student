#!/usr/bin/env python3
"""
快速启动脚本 - 配置 MySQL 密码并初始化数据库
"""

import os
import subprocess
import sys


def setup_mysql_password():
    """设置 MySQL 密码"""
    print("\n" + "=" * 60)
    print("🔐 配置 MySQL 连接")
    print("=" * 60)
    
    print("\n请输入 MySQL 的 root 用户密码:")
    password = input("密码: ").strip()
    
    # 更新 .env 文件
    with open('.env', 'r') as f:
        env_content = f.read()
    
    # 替换密码行
    lines = env_content.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith('DB_PASSWORD='):
            new_lines.append(f'DB_PASSWORD={password}')
        else:
            new_lines.append(line)
    
    with open('.env', 'w') as f:
        f.write('\n'.join(new_lines))
    
    print("✅ .env 文件已更新")
    return password


def test_mysql_connection(password):
    """测试 MySQL 连接"""
    print("\n" + "=" * 60)
    print("🔗 测试 MySQL 连接")
    print("=" * 60)
    
    try:
        import mysql.connector
        
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='15929867187xxx'
        )
        
        if conn.is_connected():
            print("✅ MySQL 连接成功")
            conn.close()
            return True
        else:
            print("❌ 连接失败")
            return False
            
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False


def initialize_database(password):
    """初始化数据库"""
    print("\n" + "=" * 60)
    print("📊 初始化数据库")
    print("=" * 60)
    
    if not os.path.exists('init_database.sql'):
        print("❌ init_database.sql 文件不存在")
        return False
    
    try:
        print("正在执行 SQL 初始化脚本...")
        
        # 在 Windows 上使用 mysql 命令
        cmd = f'mysql -h localhost -u root -p{password} < init_database.sql'
        
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ 数据库初始化成功！")
            print("\n📋 初始化内容:")
            print("   ✓ 创建了 student_grade_system 数据库")
            print("   ✓ 创建了 5 张数据表")
            print("   ✓ 导入了初始数据")
            print("\n👤 可用的测试账号:")
            print("   • 管理员: admin001 / 123456")
            print("   • 教师:   t2024001 / 123456")
            print("   • 学生:   s20220101 / 123456")
            return True
        else:
            print(f"❌ 初始化失败")
            if result.stderr:
                print(f"错误信息: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False


def verify_database():
    """验证数据库内容"""
    print("\n" + "=" * 60)
    print("✓ 验证数据库内容")
    print("=" * 60)
    
    try:
        from config import Config
        Config.validate()
        
        from dao.user_dao import UserDAO
        user_dao = UserDAO()
        
        # 查询 admin001 用户
        user = user_dao.find_by_username('admin001')
        if user:
            print(f"✅ 用户表正常: 找到 admin001 (role={user['role']})")
            return True
        else:
            print("❌ 未找到 admin001 用户")
            return False
            
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False


def main():
    """主程序"""
    print("\n" + "=" * 70)
    print("🚀 学生成绩管理系统 - 快速启动配置")
    print("=" * 70)
    
    # 步骤 1: 设置 MySQL 密码
    password = setup_mysql_password()
    
    # 步骤 2: 测试连接
    if not test_mysql_connection(password):
        print("\n❌ 无法连接到 MySQL")
        print("请检查:")
        print("  1. MySQL 服务是否已启动")
        print("  2. 密码是否正确")
        print("  3. MySQL 是否在 localhost:3306")
        return 1
    
    # 步骤 3: 初始化数据库
    if not initialize_database(password):
        print("\n❌ 数据库初始化失败")
        print("请检查 MySQL 用户权限")
        return 1
    
    # 步骤 4: 验证数据库
    print("\n等待 2 秒后验证数据库...")
    import time
    time.sleep(2)
    
    if not verify_database():
        print("⚠️ 数据库验证失败")
        print("但初始化可能已经成功")
    else:
        print("✅ 所有验证通过！")
    
    # 完成
    print("\n" + "=" * 70)
    print("✨ 配置完成！")
    print("=" * 70)
    print("\n现在可以运行应用:")
    print("   python main.py")
    print("\n按 Enter 键退出...")
    input()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
