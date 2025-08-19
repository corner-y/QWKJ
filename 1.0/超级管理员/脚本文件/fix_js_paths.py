#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复JS文件引用路径的脚本
- 将错误的 脚本文件/ 引用还原为正确的 assets/js/ 路径
- 只修复那些实际存在的JS文件
"""

import os
import re
from pathlib import Path

# 项目根目录
ROOT_DIR = Path("/Users/baiyumi/Mai/代码/chenyrweb/ybsh/1.0/超级管理员")

# JS文件路径修复映射
JS_PATH_FIXES = {
    # 登录相关
    'src="../脚本文件/login.js': 'src="登录/assets/js/login.js',
    
    # 工作台相关 - 这些文件实际存在于脚本文件目录，保持不变
    # 'src="../脚本文件/看板组件.js': 保持不变
    # 'src="../脚本文件/图表.js': 保持不变
    # 'src="../脚本文件/平台看板.js': 保持不变
    
    # 规则管理相关
    'src="../../脚本文件/common.js"': 'src="../assets/js/common.js"',
    'src="../../脚本文件/rule-parameters.js"': 'src="../assets/js/rule-parameters.js"',
    
    # 用户权限管理相关
    'src="../../脚本文件/user-management.js"': 'src="../assets/js/user-management.js"',
    'src="../../脚本文件/department-management.js"': 'src="../assets/js/department-management.js"',
    'src="../../脚本文件/permission-management.js"': 'src="../assets/js/permission-management.js"',
    'src="../../脚本文件/tenant-list.js"': 'src="../assets/js/tenant-list.js"',
    
    # 审核管理相关
    'src="../../脚本文件/operator-dashboard.js"': 'src="../assets/js/operator-dashboard.js"',
    'src="../../脚本文件/audit-results.js"': 'src="../assets/js/audit-results.js"',
    'src="../../脚本文件/in-process-check.js"': 'src="../assets/js/in-process-check.js"',
    'src="../../脚本文件/pre-audit-records.js"': 'src="../assets/js/pre-audit-records.js"',
    'src="../../脚本文件/post-audit-task-list.js"': 'src="../assets/js/post-audit-task-list.js"',
    
    # 系统管理相关
    'src="../../脚本文件/knowledge-base.js"': 'src="../assets/js/knowledge-base.js"',
}

def fix_js_paths_in_file(file_path):
    """修复单个文件中的JS路径"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 应用路径修复
        for old_path, new_path in JS_PATH_FIXES.items():
            content = content.replace(old_path, new_path)
        
        # 修复工作台的双重路径问题
        content = content.replace('src="../../超级管理员/脚本文件/', 'src="../脚本文件/')
        
        # 如果内容发生变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("开始修复JS文件引用路径...")
    
    fixed_count = 0
    total_count = 0
    
    # 处理所有HTML文件
    for file_pattern in ['**/*.html']:
        for file_path in ROOT_DIR.glob(file_pattern):
            # 跳过组件文件和脚本文件目录
            if '组件' in str(file_path) or '脚本文件' in str(file_path):
                continue
                
            total_count += 1
            if fix_js_paths_in_file(file_path):
                fixed_count += 1
                print(f"✓ 已修复JS路径: {file_path.relative_to(ROOT_DIR)}")
    
    print(f"\nJS路径修复完成!")
    print(f"总共检查: {total_count} 个文件")
    print(f"成功修复: {fixed_count} 个文件")

if __name__ == "__main__":
    main()