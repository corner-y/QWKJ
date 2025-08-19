#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复残留路径问题的脚本
- 修复企业详情和租户管理中的老菜单系统和错误路径
- 移除重复的菜单容器
- 统一所有路径为中文路径
"""

import os
import re
from pathlib import Path

# 项目根目录
ROOT_DIR = Path("/Users/baiyumi/Mai/代码/chenyrweb/ybsh/1.0/超级管理员")

def fix_remaining_issues():
    """修复特定文件的残留问题"""
    
    # 修复企业详情页
    enterprise_file = ROOT_DIR / "用户权限管理/组织管理/企业详情.html"
    if enterprise_file.exists():
        with open(enterprise_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除老菜单系统的HTML部分
        content = re.sub(
            r'<div id="sidebar-container"></div>\s*<div class="sidebar-header">.*?</div>\s*</div>',
            '<div id="sidebar-container"></div>',
            content,
            flags=re.DOTALL
        )
        
        # 修复错误的CSS引用
        content = content.replace('href="../assets/css/common.css?v=1.0"', '')
        content = content.replace('href="../assets/css/platform-dashboard.css?v=1.0"', '')
        content = re.sub(r'<link rel="stylesheet" href="样式文件/企业详情样式\.css"[^>]*>\s*', '', content)
        
        # 修复面包屑中的路径
        content = content.replace('href="../super-admin/tenant-list.html"', 'href="租户管理.html"')
        
        with open(enterprise_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 已修复: 企业详情.html")
    
    # 修复租户管理页
    tenant_file = ROOT_DIR / "用户权限管理/组织管理/租户管理.html"
    if tenant_file.exists():
        with open(tenant_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除老菜单系统的HTML部分
        content = re.sub(
            r'<div id="sidebar-container"></div>\s*<div class="sidebar-header">.*?</div>\s*</div>',
            '<div id="sidebar-container"></div>',
            content,
            flags=re.DOTALL
        )
        
        # 修复英文路径为中文
        path_mappings = {
            'href="platform-dashboard.html"': 'href="../../工作台/平台运营看板.html"',
            'href="tenant-list.html"': 'href="租户管理.html"',
            'href="rule-management.html"': 'href="../../规则管理/规则列表/规则管理主页.html"',
            'href="pre-audit.html"': 'href="../../审核管理/审核流程/事前审核记录.html"',
            'href="in-process-audit.html"': 'href="../../审核管理/审核流程/事中审核检查.html"',
            'href="post-audit.html"': 'href="../../审核管理/审核流程/事后审核任务列表.html"',
            'href="chronic-disease-audit.html"': 'href="../../审核管理/审核流程/事后审核任务列表.html"',
            'href="department-management.html"': 'href="科室管理.html"',
            'href="knowledge-base.html"': 'href="../../系统管理/知识库目录.html"',
            'href="user-management.html"': 'href="../用户管理/用户列表.html"',
            'href="permission-management.html"': 'href="../权限管理/权限管理.html"',
            'href="system-monitor.html"': 'href="../../系统管理/系统监控.html"',
            'href="global-settings.html"': 'href="../../系统管理/全局设置.html"',
        }
        
        for old_path, new_path in path_mappings.items():
            content = content.replace(old_path, new_path)
        
        with open(tenant_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 已修复: 租户管理.html")
    
    # 修复租户表单页
    tenant_form_file = ROOT_DIR / "用户权限管理/组织管理/租户表单.html"
    if tenant_form_file.exists():
        with open(tenant_form_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除错误的CSS引用
        content = content.replace('href="../assets/css/common.css?v=1.0"', '')
        content = content.replace('href="../assets/css/platform-dashboard.css?v=1.0"', '')
        
        with open(tenant_form_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 已修复: 租户表单.html")

def add_unified_menu_loading():
    """为缺少统一菜单的页面添加菜单加载脚本"""
    
    files_need_menu = [
        "用户权限管理/组织管理/企业详情.html",
        "用户权限管理/组织管理/租户管理.html",
        "用户权限管理/组织管理/租户表单.html"
    ]
    
    menu_script = """
    <!-- 加载统一菜单 -->
<script>
    // 加载统一菜单组件
    fetch('../../../组件/_unified-sidebar.html')
        .then(response => response.text())
        .then(html => {
            const sidebarContainer = document.getElementById('sidebar-container');
            sidebarContainer.innerHTML = html;
            // 手动执行插入的脚本
            const scripts = sidebarContainer.querySelectorAll('script');
            scripts.forEach(script => {
                const newScript = document.createElement('script');
                if (script.src) {
                    newScript.src = script.src;
                } else {
                    newScript.textContent = script.textContent;
                }
                document.head.appendChild(newScript);
                script.remove();
            });
            // 等待脚本执行后再初始化菜单
            setTimeout(() => {
                if (typeof initSidebar === 'function') {
                    initSidebar();
                }
            }, 100);
        })
        .catch(error => console.error('Error loading sidebar:', error));
</script>"""
    
    for file_path in files_need_menu:
        full_path = ROOT_DIR / file_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已有菜单加载脚本
            if '_unified-sidebar.html' not in content:
                # 在</body>前插入菜单加载脚本
                content = content.replace('</body>', f'{menu_script}\n</body>')
                
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ 已添加统一菜单: {file_path}")

def main():
    """主函数"""
    print("开始修复残留路径问题...")
    
    # 修复特定文件的问题
    fix_remaining_issues()
    
    # 添加统一菜单
    add_unified_menu_loading()
    
    print("\n残留问题修复完成!")
    print("修复内容:")
    print("1. 移除了企业详情和租户管理页面的重复菜单HTML")
    print("2. 修复了英文路径为中文路径")
    print("3. 移除了错误的CSS引用")
    print("4. 为缺少统一菜单的页面添加了菜单加载脚本")

if __name__ == "__main__":
    main()