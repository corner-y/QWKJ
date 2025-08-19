#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单的侧边栏路径修复脚本
"""

import os

# 修复后的绝对路径
CORRECT_PATH = '/1.0/超级管理员/组件/_unified-sidebar.html'

# 需要修复的文件列表 - 直接从之前的搜索结果中提取
files_to_fix = [
    '1.0/超级管理员/规则管理/门诊规则管理.html',
    '1.0/超级管理员/审核管理/审核流程/事后审核任务列表.html',
    '1.0/超级管理员/用户权限管理/权限管理/权限管理.html',
    '1.0/超级管理员/脚本文件/page-test.html',
    '1.0/超级管理员/系统管理/系统监控.html',
    '1.0/超级管理员/规则管理/规则详情.html',
    '1.0/超级管理员/规则管理/编辑规则.html',
    '1.0/超级管理员/规则管理/创建规则.html',
    '1.0/超级管理员/系统管理/全局设置.html',
    '1.0/超级管理员/工作台/报告规则分析.html',
    '1.0/超级管理员/系统管理/知识库目录.html',
    '1.0/超级管理员/用户权限管理/组织管理/企业详情.html',
    '1.0/超级管理员/规则管理/政策规则详情.html',
    '1.0/超级管理员/规则管理/诊疗规则详情.html',
    '1.0/超级管理员/审核管理/审核结果/审核结果.html',
    '1.0/超级管理员/工作台/平台运营看板.html',
    '1.0/超级管理员/用户权限管理/用户管理/用户列表.html',
    '1.0/超级管理员/用户权限管理/组织管理/租户表单.html',
    '1.0/超级管理员/审核管理/审核流程/事前审核记录.html',
    '1.0/超级管理员/用户权限管理/组织管理/租户管理.html',
    '1.0/超级管理员/规则管理/门诊规则详情.html',
    '1.0/超级管理员/用户权限管理/组织管理/科室管理.html',
    '1.0/超级管理员/工作台/工作台.html',
    '1.0/超级管理员/规则管理/慢病规则详情.html'
]

print("开始修复侧边栏路径...")
print(f"将所有侧边栏引用改为: {CORRECT_PATH}")

for file_path in files_to_fix:
    full_path = os.path.join(os.getcwd(), file_path)
    print(f"\n处理文件: {file_path}")
    
    try:
        # 读取文件内容
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找并替换所有侧边栏引用
        # 使用简单的字符串替换，处理常见的模式
        patterns = [
            "fetch('../组件/_unified-sidebar.html')",
            "fetch('../../组件/_unified-sidebar.html')",
            "fetch('../../../组件/_unified-sidebar.html')",
            "fetch( '../组件/_unified-sidebar.html' )",
            "fetch( '../../组件/_unified-sidebar.html' )",
            "fetch( '../../../组件/_unified-sidebar.html' )"
        ]
        
        # 统计替换次数
        replace_count = 0
        original_content = content
        
        for pattern in patterns:
            if pattern in content:
                count = content.count(pattern)
                content = content.replace(pattern, "fetch('" + CORRECT_PATH + "')")
                replace_count += count
        
        # 特殊处理：const response = await fetch('../组件/_unified-sidebar.html');
        pattern_with_const = "const response = await fetch('../组件/_unified-sidebar.html');"
        if pattern_with_const in content:
            count = content.count(pattern_with_const)
            content = content.replace(pattern_with_const, "const response = await fetch('" + CORRECT_PATH + "');")
            replace_count += count
        
        # 如果有替换，就写入文件
        if replace_count > 0:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 成功修复，替换了 {replace_count} 处引用")
        else:
            print(f"⏭️ 未找到需要修复的引用或已经是正确的路径")
            
    except Exception as e:
        print(f"❌ 修复失败: {str(e)}")

print("\n侧边栏路径修复完成！")