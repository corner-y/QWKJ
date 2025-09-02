#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用于连接MySQL数据库并检查其中的表结构
"""

import mysql.connector
from mysql.connector import Error


def check_database_tables():
    """\连接MySQL数据库并显示所有表名"""
    try:
        # 数据库连接参数
        # 您可以根据实际情况修改这些参数
        db_config = {
            'host': 'localhost',  # 数据库主机地址
            'user': 'root',       # 数据库用户名
            'password': '',       # 数据库密码
            'database': 'ybsh',   # 数据库名称
            'port': 3306          # 数据库端口
        }

        print("正在连接数据库...")
        # 连接数据库
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"成功连接到MySQL服务器版本: {db_info}")
            
            # 创建游标对象
            cursor = connection.cursor()
            
            # 查询所有表名
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"\n数据库 '{db_config['database']}' 中的表:\n")
                for table in tables:
                    print(f"- {table[0]}")
                print(f"\n总计: {len(tables)} 个表")
            else:
                print(f"\n数据库 '{db_config['database']}' 中没有表。")
    
    except Error as e:
        print(f"连接数据库时发生错误: {e}")
        print("\n请检查以下几点:")
        print("1. MySQL服务是否正在运行")
        print("2. 数据库连接参数是否正确")
        print("3. 用户是否有访问该数据库的权限")
        print("4. 数据库 'ybsh' 是否存在")
        print("\n您可以修改脚本中的连接参数以匹配您的实际配置。")
    
    finally:
        # 关闭数据库连接
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n数据库连接已关闭")


if __name__ == "__main__":
    print("==== MySQL数据库表检查工具 ====")
    check_database_tables()
    print("\n请按任意键退出...")
    input()