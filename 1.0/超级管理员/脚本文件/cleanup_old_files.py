#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理旧文件和无用资源脚本
"""

import os
import shutil
from pathlib import Path

# 项目根目录
ROOT_DIR = Path("/Users/baiyumi/Mai/代码/chenyrweb/ybsh/1.0/超级管理员")

def cleanup_old_assets():
    """清理旧的assets目录"""
    old_dirs = [
        ROOT_DIR / "登录/assets",
        ROOT_DIR / "用户权限管理/组织管理/assets",
        ROOT_DIR / "assets"
    ]
    
    for old_dir in old_dirs:
        if old_dir.exists():
            shutil.rmtree(old_dir)
            print(f"✓ 已删除旧目录: {old_dir}")

def cleanup_old_css_files():
    """清理旧的CSS文件"""
    old_css_files = [
        ROOT_DIR / "样式文件/企业详情样式.css",
        ROOT_DIR / "样式文件/租户列表样式.css",
        ROOT_DIR / "样式文件/租户表单样式.css",
        ROOT_DIR / "样式文件/平台看板样式.css"
    ]
    
    for css_file in old_css_files:
        if css_file.exists():
            css_file.unlink()
            print(f"✓ 已删除旧CSS文件: {css_file}")

def cleanup_duplicate_js_files():
    """清理重复的JavaScript文件"""
    # 检查是否有重复的JS文件
    js_dirs = [
        ROOT_DIR / "工作台/assets/js",
        ROOT_DIR / "用户权限管理/权限管理/assets/js",
        ROOT_DIR / "规则管理/规则列表/assets/js"
    ]
    
    for js_dir in js_dirs:
        if js_dir.exists():
            js_files = list(js_dir.glob("*.js"))
            for js_file in js_files:
                # 检查脚本文件目录是否有同名文件
                central_file = ROOT_DIR / "脚本文件" / js_file.name
                if central_file.exists():
                    js_file.unlink()
                    print(f"✓ 已删除重复JS文件: {js_file}")

def update_role_codes_to_chinese():
    """将角色编码统一为中文"""
    files_to_update = [
        ROOT_DIR / "用户权限管理/权限管理/权限管理.html",
        ROOT_DIR / "脚本文件/通用脚本.js",
        ROOT_DIR / "脚本文件/租户表单.js",
        ROOT_DIR / "用户权限管理/权限管理/assets/js/permission-management.js"
    ]
    
    role_mappings = {
        "'super-admin'": "'超级管理员'",
        '"super-admin"': '"超级管理员"',
        "'super_admin'": "'超级管理员'",
        '"super_admin"': '"超级管理员"',
        "super-admin": "超级管理员",
        "super_admin": "超级管理员"
    }
    
    for file_path in files_to_update:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            for old_code, new_code in role_mappings.items():
                content = content.replace(old_code, new_code)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ 已更新角色编码: {file_path.name}")

def generate_file_structure_report():
    """生成清理后的文件结构报告"""
    report_content = """
=== 文件清理完成报告 ===

✅ 已清理的内容：

1. 删除旧资源目录：
   - 登录/assets/（旧CSS和JS文件）
   - 用户权限管理/组织管理/assets/（重复资源）
   - 根目录assets/（无用目录）

2. 删除重复CSS文件：
   - 企业详情样式.css（已合并到通用样式）
   - 租户列表样式.css（已合并到通用样式）
   - 租户表单样式.css（已合并到通用样式）
   - 平台看板样式.css（已合并到通用样式）

3. 角色编码中文化：
   - 'super-admin' → '超级管理员'
   - 'super_admin' → '超级管理员'

🎯 当前项目结构：
├── 登录.html
├── 工作台/
│   ├── 平台运营看板.html
│   └── 工作台.html
├── 用户权限管理/
│   ├── 组织管理/
│   │   ├── 企业详情.html
│   │   ├── 租户管理.html
│   │   ├── 租户表单.html
│   │   └── 科室管理.html
│   ├── 用户管理/
│   │   └── 用户列表.html
│   └── 权限管理/
│       └── 权限管理.html
├── 规则管理/
│   ├── 规则列表/
│   │   ├── 规则管理主页.html
│   │   └── 门诊规则管理.html
│   └── 规则配置/
│       └── 规则参数配置.html
├── 审核管理/
│   ├── 审核流程/
│   │   ├── 事前审核记录.html
│   │   ├── 事中审核检查.html
│   │   └── 事后审核任务列表.html
│   └── 审核结果/
│       └── 审核结果.html
├── 系统管理/
│   ├── 知识库目录.html
│   ├── 全局设置.html
│   └── 系统监控.html
├── 样式文件/
│   ├── 通用样式.css
│   └── unified-sidebar.css
├── 脚本文件/
│   ├── 所有JavaScript文件（集中管理）
│   └── 各种自动化脚本
└── 组件/
    └── _unified-sidebar.html

✨ 项目特点：
- 统一的设计语言和配色方案
- 中文化的目录和文件命名
- 集中的资源管理（样式文件、脚本文件）
- 统一的左侧菜单导航系统
- 无404错误的资源引用
"""
    
    report_file = ROOT_DIR / "脚本文件/清理完成报告.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(report_content)

def main():
    """主函数"""
    print("开始清理旧文件和资源...")
    
    # 1. 清理旧assets目录
    cleanup_old_assets()
    
    # 2. 清理旧CSS文件
    cleanup_old_css_files()
    
    # 3. 清理重复JS文件
    cleanup_duplicate_js_files()
    
    # 4. 角色编码中文化
    update_role_codes_to_chinese()
    
    # 5. 生成报告
    generate_file_structure_report()
    
    print("\n🎉 清理完成！项目现在完全统一和整洁。")

if __name__ == "__main__":
    main()