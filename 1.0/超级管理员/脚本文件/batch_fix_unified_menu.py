#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复页面统一菜单引用脚本
根据测试报告，为所有带WARNING的页面自动添加统一菜单三要素：
1. 统一菜单样式引用
2. 统一菜单容器
3. 统一菜单加载脚本
"""
import os
import re
import json
from pathlib import Path

# 需要修复的页面列表（来自测试报告的WARNING项）
WARNING_PAGES = [
    # 规则管理模块
    '../规则管理/规则列表/门诊规则管理.html',
    '../规则管理/规则列表/医保规则管理系统v2.html',
    '../规则管理/规则详情/规则详情.html',
    '../规则管理/规则详情/临床规则详情.html',
    '../规则管理/规则详情/慢病规则详情.html',
    '../规则管理/规则详情/政策规则详情.html',
    '../规则管理/规则详情/门诊规则详情.html',
    '../规则管理/规则操作/创建规则.html',
    '../规则管理/规则操作/编辑规则.html',
    '../规则管理/规则操作/规则参数配置.html',
    '../规则管理/规则操作/规则管理完整版.html',
    # 审核管理模块
    '../审核管理/审核流程/事中审核检查.html',
    '../审核管理/审核流程/事后审核任务列表.html',
    '../审核管理/审核结果/审核结果.html',
    # 用户权限管理模块
    '../用户权限管理/权限管理/权限管理.html',
    '../用户权限管理/组织管理/科室管理.html',
    '../用户权限管理/组织管理/租户管理.html',
    '../用户权限管理/组织管理/租户表单.html',
    '../用户权限管理/组织管理/企业详情.html'
]

# 基础目录
BASE_DIR = Path('/Users/baiyumi/Mai/代码/chenyrweb/ybsh/1.0/超级管理员')

def get_menu_config(relative_path):
    """根据页面路径获取菜单配置"""
    page_configs = {
        # 规则管理模块
        '规则管理/规则列表/门诊规则管理.html': {'menu': 'rules-outpatient', 'level': 3},
        '规则管理/规则列表/医保规则管理系统v2.html': {'menu': 'rules-medical', 'level': 3},
        '规则管理/规则详情/规则详情.html': {'menu': 'rules-detail-general', 'level': 3},
        '规则管理/规则详情/临床规则详情.html': {'menu': 'rules-detail-clinical', 'level': 3},
        '规则管理/规则详情/慢病规则详情.html': {'menu': 'rules-detail-chronic', 'level': 3},
        '规则管理/规则详情/政策规则详情.html': {'menu': 'rules-detail-policy', 'level': 3},
        '规则管理/规则详情/门诊规则详情.html': {'menu': 'rules-detail-outpatient', 'level': 3},
        '规则管理/规则操作/创建规则.html': {'menu': 'rules-create', 'level': 3},
        '规则管理/规则操作/编辑规则.html': {'menu': 'rules-edit', 'level': 3},
        '规则管理/规则操作/规则参数配置.html': {'menu': 'rules-config', 'level': 3},
        '规则管理/规则操作/规则管理完整版.html': {'menu': 'rules-full', 'level': 3},
        # 审核管理模块
        '审核管理/审核流程/事中审核检查.html': {'menu': 'audit-during', 'level': 3},
        '审核管理/审核流程/事后审核任务列表.html': {'menu': 'audit-post', 'level': 3},
        '审核管理/审核结果/审核结果.html': {'menu': 'audit-results', 'level': 2},
        # 用户权限管理模块
        '用户权限管理/权限管理/权限管理.html': {'menu': 'permission', 'level': 2},
        '用户权限管理/组织管理/科室管理.html': {'menu': 'department', 'level': 3},
        '用户权限管理/组织管理/租户管理.html': {'menu': 'tenant', 'level': 3},
        '用户权限管理/组织管理/租户表单.html': {'menu': 'tenant-form', 'level': 3},
        '用户权限管理/组织管理/企业详情.html': {'menu': 'enterprise', 'level': 3}
    }
    
    # 移除相对路径前缀 '../'
    clean_path = relative_path.replace('../', '')
    return page_configs.get(clean_path, {'menu': 'unknown', 'level': 2})

def generate_style_links(level):
    """生成样式文件引用"""
    prefix = '../' * level
    return f'    <link rel="stylesheet" href="{prefix}样式文件/unified-sidebar.css">'

def generate_sidebar_container():
    """生成统一菜单容器"""
    return '        <div id="sidebar-container"></div>'

def generate_menu_script(menu_id, level):
    """生成菜单加载脚本"""
    prefix = '../' * level
    return f'''    <!-- 加载统一菜单 -->
    <script>
        // 加载统一菜单组件
        fetch('{prefix}组件/_unified-sidebar.html')
            .then(response => response.text())
            .then(html => {{
                document.getElementById('sidebar-container').innerHTML = html;
                // 初始化菜单
                if (typeof initSidebar === 'function') {{
                    initSidebar();
                }}
                // 设置当前页面菜单高亮
                const currentMenuItem = document.querySelector('[data-menu="{menu_id}"]');
                if (currentMenuItem) {{
                    currentMenuItem.classList.add('active');
                    // 展开父级菜单组
                    let parent = currentMenuItem.closest('.nav-group, .nav-subgroup');
                    while (parent) {{
                        parent.classList.add('expanded');
                        const submenu = parent.querySelector('.nav-submenu');
                        if (submenu) {{
                            submenu.style.display = 'block';
                        }}
                        parent = parent.parentElement.closest('.nav-group, .nav-subgroup');
                    }}
                }}
            }})
            .catch(error => console.error('Error loading sidebar:', error));
    </script>'''

def fix_single_page(page_path):
    """修复单个页面"""
    # 转换相对路径为绝对路径
    abs_path = BASE_DIR / page_path.replace('../', '')
    
    if not abs_path.exists():
        print(f"❌ 文件不存在: {abs_path}")
        return False
    
    try:
        # 读取文件内容
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取菜单配置
        config = get_menu_config(page_path)
        menu_id = config['menu']
        level = config['level']
        
        # 检查是否已有统一菜单引用
        has_unified_css = 'unified-sidebar.css' in content
        has_sidebar_container = 'sidebar-container' in content
        has_unified_sidebar_html = '_unified-sidebar.html' in content
        
        fixes_needed = []
        if not has_unified_css:
            fixes_needed.append('样式引用')
        if not has_sidebar_container:
            fixes_needed.append('菜单容器')
        if not has_unified_sidebar_html:
            fixes_needed.append('加载脚本')
        
        if not fixes_needed:
            print(f"✅ {abs_path.name} - 已有统一菜单引用，无需修复")
            return True
        
        print(f"🔧 {abs_path.name} - 需要添加: {', '.join(fixes_needed)}")
        
        # 1. 添加样式引用（在head中</head>之前）
        if not has_unified_css:
            style_link = generate_style_links(level)
            content = re.sub(
                r'(\s*</head>)',
                f'\n{style_link}\n\\1',
                content
            )
        
        # 2. 添加菜单容器（在body开始后）
        if not has_sidebar_container:
            sidebar_container = generate_sidebar_container()
            # 查找合适的插入位置
            if '<div class="dashboard-container">' in content:
                # 在dashboard-container内部插入
                content = re.sub(
                    r'(<div class="dashboard-container">\s*)',
                    f'\\1\n{sidebar_container}\n        \n',
                    content
                )
            elif '<body>' in content:
                # 在body开始后插入
                content = re.sub(
                    r'(<body[^>]*>\s*)',
                    f'\\1\n    <div class="dashboard-container">\n{sidebar_container}\n        \n        <div class="main-content">\n',
                    content
                )
                # 在body结束前关闭容器
                content = re.sub(
                    r'(\s*</body>)',
                    '\n        </div>\n    </div>\n\\1',
                    content
                )
        
        # 3. 添加菜单加载脚本（在body结束前）
        if not has_unified_sidebar_html:
            menu_script = generate_menu_script(menu_id, level)
            content = re.sub(
                r'(\s*</body>)',
                f'\n{menu_script}\n\\1',
                content
            )
        
        # 写回文件
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {abs_path.name} - 修复完成")
        return True
        
    except Exception as e:
        print(f"❌ {abs_path.name} - 修复失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始批量修复页面统一菜单引用...")
    print(f"📋 需要修复的页面数量: {len(WARNING_PAGES)}")
    print("-" * 60)
    
    success_count = 0
    failed_count = 0
    
    for page_path in WARNING_PAGES:
        try:
            if fix_single_page(page_path):
                success_count += 1
            else:
                failed_count += 1
        except Exception as e:
            print(f"❌ 处理 {page_path} 时发生错误: {e}")
            failed_count += 1
    
    print("-" * 60)
    print(f"📊 修复完成统计:")
    print(f"   ✅ 成功: {success_count}")
    print(f"   ❌ 失败: {failed_count}")
    print(f"   📈 成功率: {success_count/(success_count+failed_count)*100:.1f}%")
    
    if success_count > 0:
        print("\n🎉 建议重新运行测试脚本验证修复效果！")

if __name__ == '__main__':
    main()