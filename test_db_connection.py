#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库连接测试脚本
用于测试MySQL数据库连接并显示具体错误信息
"""

import pymysql


def main():
    """主函数"""
    try:
        print("尝试连接MySQL数据库...")
        # 连接数据库
        conn = pymysql.connect(
            host='localhost',
            user='root',  # 默认用户
            password='',  # 空密码
            database='ybsh',
            charset='utf8mb4'
        )
        print("数据库连接成功!")
        
        # 查询数据库中的表
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("数据库中的表:")
        for table in tables:
            print(f"- {table[0]}")
        
        # 关闭连接
        cursor.close()
        conn.close()
        print("数据库连接已关闭")
        
    except Exception as e:
        print(f"数据库连接失败: {str(e)}")


if __name__ == "__main__":
    main()