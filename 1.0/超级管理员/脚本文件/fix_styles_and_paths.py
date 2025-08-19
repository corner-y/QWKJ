#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一页面样式和修复404路径的脚本
- 统一所有页面的样式引用，只保留通用样式.css和unified-sidebar.css
- 修复404路径，替换错误的相对路径
- 清理重复和错误的资源引用
"""

import os
import re
import glob
from pathlib import Path

# 项目根目录
ROOT_DIR = Path("/Users/baiyumi/Mai/代码/chenyrweb/ybsh/1.0/超级管理员")

# 页面配置映射（路径层级信息）
PAGE_CONFIGS = {
    # 工作台模块 (Level 2)
    '工作台/工作台.html': 2,
    '工作台/平台运营看板.html': 2,
    '工作台/报告规则分析.html': 2,
    
    # 规则管理模块 (Level 3)
    '规则管理/规则列表/规则管理主页.html': 3,
    '规则管理/规则列表/门诊规则管理.html': 3,
    '规则管理/规则列表/医保规则管理系统v2.html': 3,
    '规则管理/规则详情/规则详情.html': 3,
    '规则管理/规则详情/临床规则详情.html': 3,
    '规则管理/规则详情/慢病规则详情.html': 3,
    '规则管理/规则详情/政策规则详情.html': 3,
    '规则管理/规则详情/门诊规则详情.html': 3,
    '规则管理/规则操作/创建规则.html': 3,
    '规则管理/规则操作/编辑规则.html': 3,
    '规则管理/规则操作/规则参数配置.html': 3,
    '规则管理/规则操作/规则管理完整版.html': 3,
    
    # 审核管理模块
    '审核管理/审核流程/事前审核记录.html': 3,
    '审核管理/审核流程/事中审核检查.html': 3,
    '审核管理/审核流程/事后审核任务列表.html': 3,
    '审核管理/审核结果/审核结果.html': 2,
    
    # 用户权限管理模块
    '用户权限管理/用户管理/用户列表.html': 3,
    '用户权限管理/权限管理/权限管理.html': 2,
    '用户权限管理/组织管理/科室管理.html': 3,
    '用户权限管理/组织管理/租户管理.html': 3,
    '用户权限管理/组织管理/租户表单.html': 3,
    '用户权限管理/组织管理/企业详情.html': 3,
    
    # 系统管理模块 (Level 2)
    '系统管理/全局设置.html': 2,
    '系统管理/系统监控.html': 2,
    '系统管理/知识库目录.html': 2
}

# 路径映射配置 - 修复常见的404错误
PATH_FIXES = {
    # 错误的index.html引用
    'href="index.html"': 'href="规则管理主页.html"',
    'href="../index.html"': 'href="../规则列表/规则管理主页.html"',
    'href="dome.html"': 'href="规则管理主页.html"',
    
    # 错误的相对路径引用
    'href="../组件/styles.css"': '',  # 移除这些错误引用
    'href="../组件/dashboard.css"': '',
    'href="样式文件/': 'href="../../../样式文件/',  # 修正样式文件路径
    
    # 修复JS文件路径
    'src="../assets/js/': 'src="../../脚本文件/',
    'src="assets/js/': 'src="../脚本文件/',
    'src="../assets/': 'src="../../资源文件/',
    
    # 修复登录页面路径
    'href="../登录.html"': 'href="../../登录.html"',
    'window.location.href = \'../登录.html\'': 'window.location.href = \'../../登录.html\'',
    
    # 工作台相关路径修复
    'href="工作台.html"': 'href="../工作台/工作台.html"',
    'href="规则管理主页.html"': 'href="../规则管理/规则列表/规则管理主页.html"',
    
    # 面包屑导航修复
    'href="../平台运营看板.html"': 'href="../工作台/平台运营看板.html"',
    
    # 脚本引用修复
    'src="超级管理员/脚本文件/': 'src="../../脚本文件/',
}

def get_style_prefix(level):
    """根据页面层级获取样式文件的相对路径前缀"""
    if level == 1:
        return '../'
    elif level == 2:
        return '../../'
    else:  # level == 3
        return '../../../'

def generate_unified_styles(level):
    """生成统一的样式引用"""
    prefix = get_style_prefix(level)
    return f'''    <link rel="stylesheet" href="{prefix}样式文件/通用样式.css">
    <link rel="stylesheet" href="{prefix}样式文件/unified-sidebar.css">'''

def clean_duplicate_styles(content):
    """清理重复和错误的样式引用"""
    # 移除重复的样式引用
    content = re.sub(r'<link rel="stylesheet" href="[^"]*样式文件/通用样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*样式文件/unified-sidebar\.css"[^>]*>\s*', '', content)
    
    # 移除错误的样式引用
    content = re.sub(r'<link rel="stylesheet" href="[^"]*组件/styles\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*组件/dashboard\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*平台看板样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*租户列表样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*规则配置样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*审核记录样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*事中审核样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*事后审核任务样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*审核结果样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*用户管理样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*科室管理样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*知识库样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*仪表板样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*表单样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*规则参数样式\.css"[^>]*>\s*', '', content)
    content = re.sub(r'<link rel="stylesheet" href="[^"]*企业详情样式\.css"[^>]*>\s*', '', content)
    
    return content

def fix_paths(content):
    """修复404路径问题"""
    for old_path, new_path in PATH_FIXES.items():
        if new_path:  # 如果new_path不为空，则替换
            content = content.replace(old_path, new_path)
        else:  # 如果new_path为空，则移除整行
            # 移除包含该路径的整个link标签
            pattern = r'<link[^>]*' + re.escape(old_path.split('"')[1]) + r'[^>]*>\s*'
            content = re.sub(pattern, '', content)
    
    return content

def process_html_file(file_path):
    """处理单个HTML文件"""
    try:
        # 获取相对路径
        rel_path = file_path.relative_to(ROOT_DIR)
        rel_path_str = str(rel_path).replace('\\', '/')
        
        # 获取页面层级
        level = PAGE_CONFIGS.get(rel_path_str, 3)  # 默认为3级
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 清理重复和错误的样式引用
        content = clean_duplicate_styles(content)
        
        # 2. 在</title>后或<head>末尾插入统一样式
        unified_styles = generate_unified_styles(level)
        
        # 尝试在</title>后插入
        if '</title>' in content:
            content = content.replace('</title>', f'</title>\n{unified_styles}')
        # 如果没有title标签，在</head>前插入
        elif '</head>' in content:
            content = content.replace('</head>', f'{unified_styles}\n</head>')
        
        # 3. 修复404路径问题
        content = fix_paths(content)
        
        # 只有内容发生变化时才写入文件
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
    print("开始统一页面样式和修复404路径...")
    
    fixed_count = 0
    total_count = 0
    
    # 处理所有HTML文件
    for file_pattern in ['**/*.html']:
        for file_path in ROOT_DIR.glob(file_pattern):
            # 跳过组件文件和脚本文件目录
            if '组件' in str(file_path) or '脚本文件' in str(file_path):
                continue
                
            total_count += 1
            if process_html_file(file_path):
                fixed_count += 1
                print(f"✓ 已修复: {file_path.relative_to(ROOT_DIR)}")
    
    print(f"\n修复完成!")
    print(f"总共检查: {total_count} 个文件")
    print(f"成功修复: {fixed_count} 个文件")
    print("\n修复内容:")
    print("1. 统一了所有页面的样式引用（只保留通用样式.css和unified-sidebar.css）")
    print("2. 修复了404路径错误")
    print("3. 清理了重复和错误的资源引用")

if __name__ == "__main__":
    main()