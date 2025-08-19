#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复统一侧边栏脚本执行问题的批量处理脚本
"""

import os
import re

def fix_sidebar_script_loading(file_path):
    """修复单个文件的侧边栏脚本加载问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找并替换旧的脚本加载模式
        pattern = r'(fetch\([\'"]([^\'"]*)组件/_unified-sidebar\.html[\'"])\)\s*\.then\(response => response\.text\(\)\)\s*\.then\(html => \{\s*document\.getElementById\([\'"]sidebar-container[\'"].*?\}\)\s*\.catch\(error => console\.error.*?\);'
        
        if re.search(pattern, content, re.DOTALL):
            # 获取相对路径前缀
            fetch_match = re.search(r'fetch\([\'"]([^\'"]*)组件/_unified-sidebar\.html[\'"]', content)
            if fetch_match:
                prefix = fetch_match.group(1)
                
                # 新的脚本加载代码
                new_script = f'''    <!-- 加载统一菜单 -->
    <script>
        // 加载统一菜单组件
        fetch('{prefix}组件/_unified-sidebar.html')
            .then(response => response.text())
            .then(html => {{
                const sidebarContainer = document.getElementById('sidebar-container');
                sidebarContainer.innerHTML = html;
                
                // 手动执行插入的脚本
                const scripts = sidebarContainer.querySelectorAll('script');
                scripts.forEach(script => {{
                    const newScript = document.createElement('script');
                    if (script.src) {{
                        newScript.src = script.src;
                    }} else {{
                        newScript.textContent = script.textContent;
                    }}
                    document.head.appendChild(newScript);
                    script.remove();
                }});
                
                // 等待脚本执行后再初始化菜单
                setTimeout(() => {{
                    if (typeof initSidebar === 'function') {{
                        initSidebar();
                    }}
                }}, 100);
            }})
            .catch(error => console.error('Error loading sidebar:', error));
    </script>'''
                
                # 替换整个脚本块
                content = re.sub(pattern, new_script, content, flags=re.DOTALL)
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False
    
    return False

def scan_and_fix_files(root_dir):
    """扫描并修复所有相关文件"""
    fixed_files = []
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                # 跳过组件文件自身
                if '_unified-sidebar.html' in file_path:
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 检查是否包含需要修复的模式
                    if 'sidebar-container' in content and 'fetch(' in content and '_unified-sidebar.html' in content:
                        if fix_sidebar_script_loading(file_path):
                            fixed_files.append(file_path)
                            print(f"✓ 已修复: {file_path}")
                        else:
                            print(f"- 跳过: {file_path} (已是新格式或无需修复)")
                    
                except Exception as e:
                    print(f"读取文件 {file_path} 时出错: {e}")
    
    return fixed_files

if __name__ == "__main__":
    # 获取脚本所在目录的父目录（超级管理员目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    admin_dir = os.path.dirname(script_dir)
    
    print("开始修复统一侧边栏脚本加载问题...")
    print(f"扫描目录: {admin_dir}")
    print("=" * 60)
    
    fixed_files = scan_and_fix_files(admin_dir)
    
    print("=" * 60)
    print(f"修复完成! 共处理了 {len(fixed_files)} 个文件:")
    for file_path in fixed_files:
        print(f"  - {os.path.relpath(file_path, admin_dir)}")