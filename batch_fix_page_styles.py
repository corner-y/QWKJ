#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量为“超级管理员”目录下页面添加专属样式引用：
- 仅在已存在“通用样式.css”后面插入对应页面的专属样式<link>
- 若页面已包含该专属样式则跳过
"""

from pathlib import Path
import re

# 页面 -> 专属样式 映射
PAGE_STYLE_MAP = {
    # 工作台模块
    '工作台.html': '工作台样式.css',
    '平台运营看板.html': '平台看板样式.css',
    '报告规则分析.html': '仪表板样式.css',

    # 用户权限管理模块
    '用户列表.html': '用户管理样式.css',
    '权限管理.html': '权限管理样式.css',
    '科室管理.html': '科室管理样式.css',
    '企业详情.html': '企业详情样式.css',
    '租户管理.html': '租户列表样式.css',
    '租户表单.html': '租户表单样式.css',

    # 审核管理模块
    '事中审核检查.html': '事中审核样式.css',
    '事前审核记录.html': '审核记录样式.css',
    '事后审核任务列表.html': '事后审核任务样式.css',
    '审核结果.html': '审核结果样式.css',

    # 规则管理模块
    '规则参数配置.html': '规则参数样式.css',
    '创建规则.html': '规则配置器样式.css',
    '编辑规则.html': '规则配置器样式.css',
    '规则管理完整版.html': '规则配置样式.css',

    # 系统管理模块
    '知识库目录.html': '知识库样式.css',
    '全局设置.html': '表单样式.css',
    '系统监控.html': '仪表板样式.css',
}

ADMIN_DIR = Path('/Users/baiyumi/Mai/代码/chenyrweb/ybsh/1.0/超级管理员')
STYLES_DIR = Path('/Users/baiyumi/Mai/代码/chenyrweb/ybsh/1.0/样式文件')


def fix_page_specific_styles():
    total = success = skip = fail = 0
    print('开始批量修复页面专属样式引用...')
    print('=' * 60)

    for html_file in ADMIN_DIR.rglob('*.html'):
        # 跳过测试页等
        if html_file.name == 'page-test.html':
            continue
        if html_file.name not in PAGE_STYLE_MAP:
            continue

        style_name = PAGE_STYLE_MAP[html_file.name]
        style_path = STYLES_DIR / style_name
        if not style_path.exists():
            print(f'⚠️ 样式文件不存在: {style_name} (页面: {html_file})')
            continue

        total += 1
        try:
            content = html_file.read_text(encoding='utf-8')

            # 已包含该样式则跳过（不区分查询参数）
            if re.search(rf'href=["\"][^"\"]*{re.escape(style_name)}(?:\?[^"\"]*)?["\"]', content):
                print(f'✅ 已包含专属样式: {html_file.name} -> {style_name}')
                skip += 1
                continue

            # 计算样式相对路径前缀（以“超级管理员”为基点回退，再进入样式文件目录）
            rel = html_file.relative_to(ADMIN_DIR)
            depth = len(rel.parts) - 1
            prefix = '../' * depth + '../样式文件/'
            style_link = f'\n    <link rel="stylesheet" href="{prefix}{style_name}">'

            # 在通用样式.css后插入
            m = re.search(r'(\s*<link\s+rel="stylesheet"\s+href="[^"#]*通用样式\.css[^"#]*"[^>]*>)', content)
            if not m:
                print(f'❌ 未找到通用样式引用位置: {html_file}')
                fail += 1
                continue

            insert_pos = m.end()
            new_content = content[:insert_pos] + style_link + content[insert_pos:]
            html_file.write_text(new_content, encoding='utf-8')
            print(f'✅ 成功添加专属样式: {html_file.name} -> {style_name}')
            success += 1
        except Exception as e:
            print(f'❌ 处理失败: {html_file} - {e}')
            fail += 1

    print('\n' + '=' * 60)
    print('批量修复完成!')
    print(f'总计处理: {total} 个页面')
    print(f'成功添加: {success} 个')
    print(f'已存在跳过: {skip} 个')
    print(f'处理失败: {fail} 个')
    rate = (success / total * 100) if total else 0
    print(f'修复成功率: {rate:.1f}%')


if __name__ == '__main__':
    fix_page_specific_styles()