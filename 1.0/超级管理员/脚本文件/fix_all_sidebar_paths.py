#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复所有页面中侧边栏组件的引用路径
将所有相对路径引用的_unified-sidebar.html统一改为绝对路径
"""

import os
import re
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
# 修复后的绝对路径
CORRECT_PATH = '/1.0/超级管理员/组件/_unified-sidebar.html'
# 要搜索的文件模式
FILE_PATTERNS = ['*.html']
# 排除的目录
EXCLUDE_DIRS = ['node_modules', '.git', '__pycache__', '.wdm', 'logs', 'img']
# 要搜索的正则表达式模式
SIDEBAR_PATTERN = r'fetch\(["\'].*?_unified-sidebar\.html["\']\)'


def find_files_to_fix():
    """查找所有需要修复的HTML文件"""
    files_to_fix = []
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # 排除不需要搜索的目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if any(file.endswith(pattern) for pattern in FILE_PATTERNS):
                file_path = Path(root) / file
                files_to_fix.append(file_path)
    
    return files_to_fix


def fix_sidebar_path(file_path):
    """修复文件中的侧边栏路径引用"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找所有匹配的侧边栏引用
        matches = re.findall(SIDEBAR_PATTERN, content)
        if not matches:
            return False, "无匹配的侧边栏引用"
        
        # 记录修复前的内容用于比较
        original_content = content
        
        # 替换所有侧边栏引用为正确的绝对路径
        def replace_match(match):
            # 保留fetch()函数的结构，只替换路径部分
            return f"fetch('{CORRECT_PATH}')"
        
        content = re.sub(SIDEBAR_PATTERN, replace_match, content)
        
        # 如果内容没有变化，说明已经是正确的路径
        if content == original_content:
            return False, "路径已经正确，无需修复"
        
        # 写入修复后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, f"修复成功，替换了 {len(matches)} 处引用"
        
    except Exception as e:
        return False, f"修复失败: {str(e)}"


def main():
    """主函数"""
    print("开始批量修复侧边栏路径引用...")
    print(f"目标目录: {PROJECT_ROOT}")
    print(f"修复为绝对路径: {CORRECT_PATH}")
    
    # 查找所有需要修复的文件
    files_to_fix = find_files_to_fix()
    print(f"找到 {len(files_to_fix)} 个可能需要修复的HTML文件")
    
    # 统计信息
    success_count = 0
    failed_count = 0
    skipped_count = 0
    
    # 修复每个文件
    for file_path in files_to_fix:
        rel_path = file_path.relative_to(PROJECT_ROOT)
        print(f"\n正在处理: {rel_path}")
        
        success, message = fix_sidebar_path(file_path)
        if success:
            success_count += 1
            print(f"  ✅ {message}")
        elif "无需修复" in message:
            skipped_count += 1
            print(f"  ⏭️ {message}")
        else:
            failed_count += 1
            print(f"  ❌ {message}")
    
    # 输出统计结果
    print(f"\n修复完成！")
    print(f"成功修复: {success_count}")
    print(f"无需修复: {skipped_count}")
    print(f"修复失败: {failed_count}")
    print("\n所有侧边栏组件引用已统一为绝对路径，这应该解决了多次点击后出现的404错误。")


if __name__ == '__main__':
    main()