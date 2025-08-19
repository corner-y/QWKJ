#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理并标准化所有页面的"加载统一菜单"脚本块，解决重复<script>与嵌套注释导致的大面积报错问题。
主要修复：
1. 移除重复的脚本块和注释
2. 确保单一规范的统一菜单加载逻辑
3. 修复语法错误
"""

import os
import re

def fix_file(file_path):
    """修复单个文件的统一菜单脚本块"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f'读取失败: {e}'
    
    # 跳过组件文件本身
    if '_unified-sidebar.html' in file_path:
        return False, '跳过组件文件'
    
    # 只处理包含统一菜单的文件
    if 'sidebar-container' not in content or '_unified-sidebar.html' not in content:
        return False, '无统一菜单'
    
    # 检测相对路径
    fetch_match = re.search(r"fetch\(['\"]([^'\"]*组件/_unified-sidebar\.html)['\"]\)", content)
    if not fetch_match:
        return False, '无fetch调用'
    
    relative_path = fetch_match.group(1)
    
    # 标准化脚本模板
    standard_script = f'''<!-- 加载统一菜单 -->
<script>
    // 加载统一菜单组件
    fetch('{relative_path}')
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
    
    # 移除所有现有的统一菜单相关脚本块（包括注释和重复内容）
    # 匹配从"<!-- 加载统一菜单 -->"开始到"</script>"结束的所有内容，包括重复部分
    pattern = r'<!--\s*加载统一菜单\s*-->[\s\S]*?</script>(?:\s*</script>)*'
    
    # 替换为标准脚本
    new_content = re.sub(pattern, standard_script, content, flags=re.IGNORECASE)
    
    # 如果内容有变化，写入文件
    if new_content != content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, '修复成功'
        except Exception as e:
            return False, f'写入失败: {e}'
    else:
        return False, '无需修改'

def main():
    """主函数"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    admin_dir = os.path.dirname(script_dir)
    
    print('开始修复统一菜单脚本块...')
    
    fixed_count = 0
    error_count = 0
    
    for root, dirs, files in os.walk(admin_dir):
        for file in files:
            if not file.endswith('.html'):
                continue
                
            file_path = os.path.join(root, file)
            success, message = fix_file(file_path)
            
            if success:
                fixed_count += 1
                print(f'✓ 修复: {file_path}')
            elif '失败' in message:
                error_count += 1
                print(f'✗ 错误: {file_path} - {message}')
            # 静默跳过无关文件
    
    print(f'修复完成。成功: {fixed_count} 个，错误: {error_count} 个')

if __name__ == '__main__':
    main()