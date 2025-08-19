#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
修复登录页面样式路径和CSS变量问题
"""

import os
import re

def fix_login_page():
    """修复登录页面的样式问题"""
    login_file = "/Users/baiyumi/Mai/代码/chenyrweb/ybsh/1.0/超级管理员/登录.html"
    
    print("🔧 修复登录页面样式...")
    
    with open(login_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 修复样式文件路径（从 ../../../ 改为 ../）
    content = re.sub(
        r'href="../../../样式文件/',
        'href="../样式文件/',
        content
    )
    
    # 2. 移除不必要的 unified-sidebar.css 引用
    content = re.sub(
        r'<link rel="stylesheet" href="../样式文件/unified-sidebar\.css">\n',
        '',
        content
    )
    
    # 3. 统一CSS变量名（匹配通用样式.css中的变量）
    css_var_mapping = {
        'var(--color-white)': 'var(--bg-primary)',
        'var(--radius-2xl)': 'var(--radius-xl)',
        'var(--space-4)': 'var(--spacing-lg)',
        'var(--space-8)': 'var(--spacing-2xl)',
        'var(--space-2)': 'var(--spacing-sm)',
        'var(--space-1)': 'var(--spacing-xs)',
        'var(--space-6)': 'var(--spacing-xl)',
        'var(--color-primary)': 'var(--primary-color)',
        'var(--color-text-primary)': 'var(--text-primary)',
        'var(--color-text-secondary)': 'var(--text-secondary)',
        'var(--color-text-tertiary)': 'var(--text-tertiary)',
        'var(--color-border)': 'var(--border-primary)',
        'var(--radius-lg)': 'var(--radius-large)',
        'var(--font-size-2xl)': 'var(--font-size-2xl)',
        'var(--font-size-xl)': 'var(--font-size-xl)',
        'var(--font-size-sm)': 'var(--font-size-sm)',
        'var(--font-size-base)': 'var(--font-size-md)',
        'var(--font-size-xs)': 'var(--font-size-xs)',
        'var(--font-weight-bold)': 'var(--font-weight-bold)',
        'var(--font-weight-medium)': 'var(--font-weight-medium)',
        'var(--font-weight-semibold)': 'var(--font-weight-semibold)',
        'var(--duration-fast)': '0.2s',
        'var(--ease)': 'cubic-bezier(0.4, 0, 0.2, 1)',
        'var(--color-primary-50)': 'rgba(22, 93, 255, 0.1)',
        'var(--color-primary-dark)': 'var(--primary-active)',
        'var(--shadow-lg)': 'var(--shadow-medium)',
        'var(--color-error-bg)': 'var(--error-light)',
        'var(--color-error)': 'var(--error-color)',
        'var(--space-3)': 'var(--spacing-md)',
    }
    
    for old_var, new_var in css_var_mapping.items():
        content = content.replace(old_var, new_var)
    
    with open(login_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 登录页面样式已修复")

def fix_all_css_paths():
    """修复所有页面的CSS路径问题"""
    print("\n🔧 修复所有页面的CSS路径...")
    
    base_dir = "/Users/baiyumi/Mai/代码/chenyrweb/ybsh/1.0/超级管理员"
    
    # 根据目录层级确定正确的路径前缀
    path_fixes = {
        # 根目录文件应使用 ../
        base_dir: '../',
        # 一级子目录应使用 ../../
        os.path.join(base_dir, '工作台'): '../../',
        # 二级子目录应使用 ../../../
        os.path.join(base_dir, '用户权限管理', '组织管理'): '../../../',
        os.path.join(base_dir, '用户权限管理', '用户管理'): '../../../',
        os.path.join(base_dir, '规则管理', '规则列表'): '../../../',
        os.path.join(base_dir, '规则管理', '规则操作'): '../../../',
        os.path.join(base_dir, '规则管理', '规则详情'): '../../../',
        os.path.join(base_dir, '审核管理', '审核流程'): '../../../',
    }
    
    fixed_count = 0
    
    for directory, correct_prefix in path_fixes.items():
        if not os.path.exists(directory):
            continue
            
        for root, dirs, files in os.walk(directory):
            # 只处理当前目录级别，不递归
            if root != directory:
                continue
                
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # 修复错误的路径
                    content = re.sub(
                        r'href="../../../样式文件/',
                        f'href="{correct_prefix}样式文件/',
                        content
                    )
                    
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        fixed_count += 1
                        print(f"  ✅ 修复: {file}")
    
    print(f"✅ 共修复 {fixed_count} 个文件的CSS路径")

if __name__ == '__main__':
    print("🚀 开始修复登录页面样式问题...")
    
    fix_login_page()
    fix_all_css_paths()
    
    print("\n🎉 所有样式问题修复完成！")
    print("\n📋 修复内容:")
    print("  • 修复了登录页面的CSS文件路径")
    print("  • 移除了登录页面不必要的sidebar样式引用")
    print("  • 统一了CSS变量名，匹配通用样式文件")
    print("  • 修复了所有页面的样式文件路径问题")
    print("\n🌐 请访问: http://localhost:8081/登录.html 查看修复效果")