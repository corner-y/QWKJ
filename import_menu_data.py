#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
菜单数据导入脚本
用于将菜单管理页面中的静态菜单数据导入到MySQL数据库
"""

import re
import json
import pymysql
from datetime import datetime


def parse_menu_data_from_html(html_file_path):
    """从HTML文件中解析menuData对象"""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 使用正则表达式提取menuData对象
        menu_data_match = re.search(r'const menuData = (\{.*?\});', html_content, re.DOTALL)
        if not menu_data_match:
            print("未找到menuData对象")
            return {}
        
        # 提取并解析JSON数据
        menu_data_str = menu_data_match.group(1)
        # 处理JavaScript对象中的特殊语法（如末尾逗号）
        menu_data_str = menu_data_str.replace(',\n                }', '\n                }')
        
        # 转换为Python字典
        menu_data = json.loads(menu_data_str)
        return menu_data
        
    except Exception as e:
        print(f"解析HTML文件出错: {e}")
        return {}


def connect_to_database():
    """连接到MySQL数据库"""
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',  # 默认用户
            password='',  # 空密码
            database='ybsh',
            charset='utf8mb4'
        )
        print("数据库连接成功")
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None


def import_menu_data_to_database(conn, menu_data):
    """将菜单数据导入到数据库"""
    if not conn or not menu_data:
        return
    
    try:
        cursor = conn.cursor()
        
        # 清空现有菜单数据（可选）
        # cursor.execute("DELETE FROM sys_menu")
        
        # 插入菜单数据
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        inserted_count = 0
        
        for menu_id, menu_info in menu_data.items():
            # 构建插入SQL语句
            sql = """
            INSERT INTO sys_menu (
                scale_menu_id, menu_path, menu_name, menu_iconcls, 
                menu_type, menu_status, menu_parentid, menu_order, 
                create_time, update_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                menu_path = VALUES(menu_path),
                menu_name = VALUES(menu_name),
                menu_iconcls = VALUES(menu_iconcls),
                menu_type = VALUES(menu_type),
                menu_status = VALUES(menu_status),
                menu_parentid = VALUES(menu_parentid),
                menu_order = VALUES(menu_order),
                update_time = VALUES(update_time)
            """
            
            # 确定菜单类型（1-一级菜单，2-二级菜单）
            menu_type = '1' if menu_info['parent'] == '0' else '2'
            
            # 准备参数
            params = (
                f"M{int(menu_id):06d}",  # 转换为数据库中的ID格式
                menu_info['path'],
                menu_info['name'],
                menu_info['icon'],
                menu_type,
                '1' if menu_info['status'] == 'enabled' else '2',  # 1-启用，2-禁用
                f"M{int(menu_info['parent']):06d}" if menu_info['parent'] != '0' else '',
                menu_info['sort'],
                current_time,
                current_time
            )
            
            # 执行SQL
            cursor.execute(sql, params)
            inserted_count += 1
        
        # 提交事务
        conn.commit()
        print(f"成功导入 {inserted_count} 条菜单数据")
        
    except Exception as e:
        print(f"导入菜单数据出错: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()


def main():
    """主函数"""
    # HTML文件路径
    html_file_path = r"e:\qw\code\ybsh\ybsh\ybsh\1.0\超级管理员\系统管理\菜单管理.html"
    
    # 解析HTML文件中的菜单数据
    menu_data = parse_menu_data_from_html(html_file_path)
    if not menu_data:
        print("未能解析到菜单数据，程序退出")
        return
    
    # 连接数据库
    conn = connect_to_database()
    if not conn:
        print("数据库连接失败，程序退出")
        return
    
    # 导入菜单数据
    import_menu_data_to_database(conn, menu_data)
    
    # 关闭数据库连接
    conn.close()
    print("数据库连接已关闭")


if __name__ == "__main__":
    main()