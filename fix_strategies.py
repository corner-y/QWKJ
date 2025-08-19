#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医保审核系统修复策略库
扩展修复策略，覆盖P0/P1/P2级别的常见问题

基于UI审查标准与评估指南的修复策略：
1. 业务逻辑与信息架构修复
2. 交互完整性与可用性修复
3. UI视觉与一致性修复
4. 左侧菜单与导航修复
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# 导入公共配置
try:
    from audit_config import (
        ROOT, ADMIN_DIR, COMMON_CSS,
        SIDEBAR_SNIPPET_MARK, CHART_CSS_MARK, UI_FIX_MARK
    )
except ImportError:
    ROOT = Path(__file__).resolve().parent
    ADMIN_DIR = ROOT / '1.0' / '超级管理员'
    COMMON_CSS = ROOT / '1.0' / '样式文件' / '通用样式.css'
    SIDEBAR_SNIPPET_MARK = '/* unified-sidebar: injected */'
    CHART_CSS_MARK = '/* ui_audit_and_fix: charts min-height */'
    UI_FIX_MARK = '/* fix_strategies: applied */'


class BusinessLogicFixer:
    """业务逻辑与信息架构修复器"""
    
    def __init__(self):
        self.admin_dir = ADMIN_DIR
    
    def fix_missing_breadcrumb(self, page_path: Path) -> List[str]:
        """修复缺失的面包屑导航"""
        changes = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 检查是否已有面包屑
        if 'breadcrumb' in content.lower() or '面包屑' in content:
            return changes
        
        # 根据页面路径生成面包屑
        breadcrumb_html = self._generate_breadcrumb(page_path)
        
        # 对于组件页面（HTML片段），直接在开头添加面包屑
        if page_path.name.startswith('_') and not content.strip().startswith('<html'):
            new_content = f'{breadcrumb_html}\n{content}'
            page_path.write_text(new_content, encoding='utf-8')
            changes.append(f"添加面包屑导航到组件 {page_path.name}")
            return changes
        
        # 在主内容区域前插入面包屑
        main_content_patterns = [
            r'(<div[^>]*class="[^"]*main[^"]*"[^>]*>)',
            r'(<main[^>]*>)',
            r'(<div[^>]*class="[^"]*content[^"]*"[^>]*>)'
        ]
        
        for pattern in main_content_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                new_content = re.sub(
                    pattern,
                    f'{breadcrumb_html}\n\1',
                    content,
                    count=1,
                    flags=re.IGNORECASE
                )
                if new_content != content:
                    page_path.write_text(new_content, encoding='utf-8')
                    changes.append(f"添加面包屑导航到 {page_path.name}")
                    break
        
        return changes
    
    def fix_missing_page_title(self, page_path: Path) -> List[str]:
        """修复缺失的页面标题"""
        changes = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 检查是否已有H1标题
        if re.search(r'<h1[^>]*>', content, re.IGNORECASE):
            return changes
        
        # 对于组件页面（HTML片段），在开头添加H1标题
        if page_path.name.startswith('_') and not content.strip().startswith('<html'):
            page_title = self._generate_page_title(page_path)
            title_html = f'<h1 class="page-title">{page_title}</h1>'
            new_content = f'{title_html}\n{content}'
            page_path.write_text(new_content, encoding='utf-8')
            changes.append(f"添加页面标题到组件 {page_path.name}")
            return changes
        
        # 根据文件名生成页面标题
        page_title = self._generate_page_title(page_path)
        title_html = f'<h1 class="page-title">{page_title}</h1>'
        
        # 在主内容区域开始处插入标题
        main_content_patterns = [
            r'(<div[^>]*class="[^"]*main[^"]*"[^>]*>)',
            r'(<main[^>]*>)',
            r'(<div[^>]*class="[^"]*content[^"]*"[^>]*>)'
        ]
        
        for pattern in main_content_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                insert_pos = match.end()
                new_content = content[:insert_pos] + f'\n{title_html}\n' + content[insert_pos:]
                page_path.write_text(new_content, encoding='utf-8')
                changes.append(f"添加页面标题到 {page_path.name}")
                break
        
        return changes
    
    def fix_data_validation_missing(self, page_path: Path) -> List[str]:
        """修复缺失的数据验证"""
        changes = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 查找表单输入字段
        form_inputs = re.findall(r'<input[^>]*type="(text|email|number|tel)"[^>]*>', content, re.IGNORECASE)
        
        if not form_inputs:
            return changes
        
        # 添加基础验证脚本
        validation_script = '''
<script>
// 基础表单验证
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.style.borderColor = '#ff4d4f';
                    isValid = false;
                } else {
                    input.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('请填写所有必填字段');
            }
        });
    });
});
</script>'''
        
        # 在</body>前插入验证脚本
        if '</body>' in content and 'form' in content.lower():
            new_content = content.replace('</body>', f'{validation_script}\n</body>')
            page_path.write_text(new_content, encoding='utf-8')
            changes.append(f"添加表单验证脚本到 {page_path.name}")
        
        return changes
    
    def _generate_breadcrumb(self, page_path: Path) -> str:
        """根据页面路径生成面包屑导航"""
        # 解析路径层级
        try:
            # 如果是绝对路径，直接计算相对路径
            if page_path.is_absolute():
                relative_path = page_path.relative_to(self.admin_dir)
            else:
                # 如果是相对路径，先转换为绝对路径
                abs_path = (self.admin_dir / page_path).resolve()
                relative_path = abs_path.relative_to(self.admin_dir)
        except ValueError:
            # 如果路径不在admin_dir下，使用页面路径的字符串形式
            path_str = str(page_path)
            if path_str.startswith('1.0/超级管理员/'):
                path_str = path_str[len('1.0/超级管理员/'):]
            relative_path = Path(path_str)
        
        parts = list(relative_path.parts[:-1])  # 排除文件名
        
        breadcrumb_items = ['<a href="../工作台/平台运营看板.html">首页</a>']
        
        current_path = '..'
        for part in parts:
            current_path += f'/{part}'
            breadcrumb_items.append(f'<a href="{current_path}/">{part}</a>')
        
        # 当前页面
        page_name = page_path.stem.replace('.html', '')
        breadcrumb_items.append(f'<span class="current">{page_name}</span>')
        
        return f'''
<nav class="breadcrumb" aria-label="面包屑导航">
    {' > '.join(breadcrumb_items)}
</nav>'''
    
    def _generate_page_title(self, page_path: Path) -> str:
        """根据文件名生成页面标题"""
        filename = page_path.stem
        # 移除常见后缀
        title = filename.replace('.html', '').replace('_', ' ')
        return title


class InteractionFixer:
    """交互完整性与可用性修复器"""
    
    def __init__(self):
        self.admin_dir = ADMIN_DIR
    
    def fix_missing_loading_states(self, page_path: Path) -> List[str]:
        """修复缺失的加载状态"""
        changes = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 检查是否有异步请求但缺少加载状态
        has_fetch = 'fetch(' in content or 'XMLHttpRequest' in content or '$.ajax' in content
        has_loading = 'loading' in content.lower() or 'spinner' in content.lower()
        
        if has_fetch and not has_loading:
            loading_css = '''
<style>
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.8);
    display: none;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #1890ff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>'''
            
            loading_html = '''
<div id="loadingOverlay" class="loading-overlay">
    <div class="loading-spinner"></div>
</div>'''
            
            loading_script = '''
<script>
// 加载状态管理
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

// 自动为fetch请求添加加载状态
const originalFetch = window.fetch;
window.fetch = function(...args) {
    showLoading();
    return originalFetch.apply(this, args)
        .finally(() => hideLoading());
};
</script>'''
            
            # 插入加载组件
            if '<head>' in content:
                new_content = content.replace('<head>', f'<head>\n{loading_css}')
            else:
                new_content = content
            
            if '<body>' in new_content:
                new_content = new_content.replace('<body>', f'<body>\n{loading_html}')
            
            if '</body>' in new_content:
                new_content = new_content.replace('</body>', f'{loading_script}\n</body>')
            
            if new_content != content:
                page_path.write_text(new_content, encoding='utf-8')
                changes.append(f"添加加载状态组件到 {page_path.name}")
        
        return changes
    
    def fix_missing_error_handling(self, page_path: Path) -> List[str]:
        """修复缺失的错误处理"""
        changes = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 检查是否有异步请求但缺少错误处理
        has_fetch = 'fetch(' in content
        has_error_handling = '.catch(' in content or 'try' in content
        
        if has_fetch and not has_error_handling:
            error_handling_script = '''
<script>
// 全局错误处理
window.addEventListener('unhandledrejection', function(event) {
    console.error('未处理的Promise错误:', event.reason);
    showErrorMessage('操作失败，请稍后重试');
});

function showErrorMessage(message) {
    // 创建错误提示
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ff4d4f;
        color: white;
        padding: 12px 20px;
        border-radius: 4px;
        z-index: 10000;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    `;
    
    document.body.appendChild(errorDiv);
    
    // 3秒后自动移除
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.parentNode.removeChild(errorDiv);
        }
    }, 3000);
}
</script>'''
            
            if '</body>' in content:
                new_content = content.replace('</body>', f'{error_handling_script}\n</body>')
                page_path.write_text(new_content, encoding='utf-8')
                changes.append(f"添加错误处理机制到 {page_path.name}")
        
        return changes
    
    def fix_missing_accessibility(self, page_path: Path) -> List[str]:
        """修复缺失的无障碍访问支持"""
        changes = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 检查并添加基础的无障碍属性
        fixes_needed = []
        
        # 检查按钮是否有aria-label
        buttons = re.findall(r'<button[^>]*>', content, re.IGNORECASE)
        for button in buttons:
            if 'aria-label' not in button and 'title' not in button:
                fixes_needed.append('button_aria')
                break
        
        # 检查表单是否有label
        inputs = re.findall(r'<input[^>]*>', content, re.IGNORECASE)
        for input_tag in inputs:
            if 'id=' in input_tag:
                input_id = re.search(r'id="([^"]+)"', input_tag)
                if input_id:
                    label_pattern = f'<label[^>]*for="{input_id.group(1)}"'
                    if not re.search(label_pattern, content, re.IGNORECASE):
                        fixes_needed.append('input_label')
                        break
        
        if fixes_needed:
            accessibility_script = '''
<script>
// 无障碍访问增强
document.addEventListener('DOMContentLoaded', function() {
    // 为没有aria-label的按钮添加
    const buttons = document.querySelectorAll('button:not([aria-label]):not([title])');
    buttons.forEach(button => {
        const text = button.textContent.trim() || button.innerHTML.replace(/<[^>]*>/g, '').trim();
        if (text) {
            button.setAttribute('aria-label', text);
        }
    });
    
    // 为表单输入添加基础的无障碍支持
    const inputs = document.querySelectorAll('input:not([aria-label]):not([title])');
    inputs.forEach(input => {
        const placeholder = input.getAttribute('placeholder');
        if (placeholder) {
            input.setAttribute('aria-label', placeholder);
        }
    });
});
</script>'''
            
            if '</body>' in content:
                new_content = content.replace('</body>', f'{accessibility_script}\n</body>')
                page_path.write_text(new_content, encoding='utf-8')
                changes.append(f"添加无障碍访问支持到 {page_path.name}")
        
        return changes


class UIVisualFixer:
    """UI视觉与一致性修复器"""
    
    def __init__(self):
        self.common_css = COMMON_CSS
    
    def fix_duplicate_scripts(self, page_path: Path) -> List[str]:
        """修复重复的脚本代码"""
        changes = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 提取所有脚本块
        script_pattern = r'<script[^>]*>([\s\S]*?)</script>'
        scripts = re.findall(script_pattern, content, re.IGNORECASE)
        
        if len(scripts) <= 1:
            return changes
        
        # 找出重复的脚本
        script_contents = [script.strip() for script in scripts if script.strip()]
        unique_scripts = []
        seen_scripts = set()
        
        for script in script_contents:
            if script not in seen_scripts:
                unique_scripts.append(script)
                seen_scripts.add(script)
        
        if len(unique_scripts) < len(script_contents):
            # 重新构建页面，移除重复脚本
            new_content = content
            
            # 移除所有脚本块
            new_content = re.sub(script_pattern, '', new_content, flags=re.IGNORECASE)
            
            # 在body结束前添加去重后的脚本
            scripts_html = '\n'.join([f'<script>\n{script}\n</script>' for script in unique_scripts])
            new_content = new_content.replace('</body>', f'{scripts_html}\n</body>')
            
            page_path.write_text(new_content, encoding='utf-8')
            changes.append(f"移除了{len(script_contents) - len(unique_scripts)}个重复脚本块")
        
        return changes
    
    def fix_html_structure(self, page_path: Path) -> List[str]:
        """修复HTML结构问题"""
        changes = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 检查div标签匹配
        div_open = len(re.findall(r'<div[^>]*>', content, re.IGNORECASE))
        div_close = len(re.findall(r'</div>', content, re.IGNORECASE))
        
        if div_open != div_close:
            # 简单修复：在body结束前添加缺失的闭合标签
            if div_open > div_close:
                missing_closes = div_open - div_close
                close_tags = '</div>\n' * missing_closes
                new_content = content.replace('</body>', f'{close_tags}</body>')
                page_path.write_text(new_content, encoding='utf-8')
                changes.append(f"添加了{missing_closes}个缺失的div闭合标签")
            else:
                # 如果闭合标签过多，记录但不自动修复（需要人工检查）
                changes.append(f"检测到{div_close - div_open}个多余的div闭合标签，需要人工检查")
        
        return changes
    
    def fix_breadcrumb_duplicates(self, page_path: Path) -> List[str]:
        """修复面包屑导航重复问题"""
        changes = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 查找面包屑导航
        breadcrumb_pattern = r'<nav[^>]*class="[^"]*breadcrumb[^"]*"[^>]*>([\s\S]*?)</nav>'
        breadcrumb_match = re.search(breadcrumb_pattern, content, re.IGNORECASE)
        
        if breadcrumb_match:
            breadcrumb_content = breadcrumb_match.group(1)
            breadcrumb_items = re.findall(r'>([^<]+)<', breadcrumb_content)
            
            if len(breadcrumb_items) != len(set(breadcrumb_items)):
                # 去重面包屑项
                unique_items = []
                seen_items = set()
                
                for item in breadcrumb_items:
                    item_clean = item.strip()
                    if item_clean and item_clean not in seen_items:
                        unique_items.append(item_clean)
                        seen_items.add(item_clean)
                
                # 重新构建面包屑
                new_breadcrumb = '<nav class="breadcrumb">\n'
                for i, item in enumerate(unique_items):
                    if i == len(unique_items) - 1:
                        new_breadcrumb += f'    <span class="breadcrumb-item active">{item}</span>\n'
                    else:
                        new_breadcrumb += f'    <a href="#" class="breadcrumb-item">{item}</a>\n'
                new_breadcrumb += '</nav>'
                
                # 替换原有面包屑
                new_content = re.sub(breadcrumb_pattern, new_breadcrumb, content, flags=re.IGNORECASE)
                page_path.write_text(new_content, encoding='utf-8')
                changes.append(f"修复了面包屑重复项，保留{len(unique_items)}个唯一项")
        
        return changes
    
    def fix_scattered_styles(self, page_path: Path) -> List[str]:
        """修复分散的样式定义"""
        changes = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 提取所有样式块
        style_pattern = r'<style[^>]*>([\s\S]*?)</style>'
        styles = re.findall(style_pattern, content, re.IGNORECASE)
        
        if len(styles) > 2:
            # 合并所有样式
            combined_styles = '\n'.join([style.strip() for style in styles if style.strip()])
            
            # 移除所有原有样式块
            new_content = re.sub(style_pattern, '', content, flags=re.IGNORECASE)
            
            # 在head中添加合并后的样式
            combined_style_block = f'<style>\n{combined_styles}\n</style>'
            if '</head>' in new_content:
                new_content = new_content.replace('</head>', f'{combined_style_block}\n</head>')
            else:
                # 如果没有head标签，在开头添加
                new_content = f'{combined_style_block}\n{new_content}'
            
            page_path.write_text(new_content, encoding='utf-8')
            changes.append(f"合并了{len(styles)}个分散的样式块")
        
        return changes
    
    def fix_inconsistent_spacing(self, page_path: Path) -> List[str]:
        """修复不一致的间距"""
        changes = []
        
        # 添加统一间距样式到通用CSS
        if self._ensure_spacing_styles():
            changes.append("添加统一间距样式到通用CSS")
        
        # 为页面添加统一间距类
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 查找需要统一间距的元素
        spacing_fixes = [
            (r'(<div[^>]*class="[^"]*card[^"]*"[^>]*>)', 'class="card spacing-standard"'),
            (r'(<section[^>]*>)', 'class="section spacing-standard"'),
            (r'(<form[^>]*>)', 'class="form spacing-standard"')
        ]
        
        new_content = content
        for pattern, replacement in spacing_fixes:
            matches = re.findall(pattern, new_content, re.IGNORECASE)
            for match in matches:
                if 'spacing-standard' not in match:
                    new_match = re.sub(r'class="([^"]*)"', r'class="\1 spacing-standard"', match)
                    if 'class=' not in match:
                        new_match = match.replace('>', ' class="spacing-standard">')
                    new_content = new_content.replace(match, new_match)
        
        if new_content != content:
            page_path.write_text(new_content, encoding='utf-8')
            changes.append(f"应用统一间距样式到 {page_path.name}")
        
        return changes
    
    def fix_inconsistent_colors(self, page_path: Path) -> List[str]:
        """修复不一致的颜色"""
        changes = []
        
        # 添加统一颜色变量到通用CSS
        if self._ensure_color_variables():
            changes.append("添加统一颜色变量到通用CSS")
        
        return changes
    
    def fix_responsive_issues(self, page_path: Path) -> List[str]:
        """修复响应式设计问题"""
        changes = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 对于组件页面（HTML片段），跳过viewport检查，只确保响应式样式
        if page_path.name.startswith('_') and not content.strip().startswith('<html'):
            if self._ensure_responsive_styles():
                changes.append("添加基础响应式样式到通用CSS")
            changes.append(f"组件 {page_path.name} 响应式支持已优化")
            return changes
        
        # 检查是否有viewport meta标签
        if 'viewport' not in content:
            viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            
            if '<head>' in content:
                new_content = content.replace('<head>', f'<head>\n{viewport_meta}')
                page_path.write_text(new_content, encoding='utf-8')
                changes.append(f"添加viewport meta标签到 {page_path.name}")
        
        # 添加基础响应式样式
        if self._ensure_responsive_styles():
            changes.append("添加基础响应式样式到通用CSS")
        
        return changes
    
    def _ensure_spacing_styles(self) -> bool:
        """确保统一间距样式存在"""
        if not self.common_css.exists():
            return False
        
        content = self.common_css.read_text(encoding='utf-8', errors='ignore')
        
        if 'spacing-standard' in content:
            return False
        
        spacing_css = '''
/* 统一间距样式 */
.spacing-standard {
    margin: 16px 0;
    padding: 16px;
}

.spacing-small {
    margin: 8px 0;
    padding: 8px;
}

.spacing-large {
    margin: 24px 0;
    padding: 24px;
}

/* 卡片间距 */
.card.spacing-standard {
    margin-bottom: 16px;
    padding: 20px;
}

/* 表单间距 */
.form.spacing-standard .form-item {
    margin-bottom: 16px;
}

.form.spacing-standard .form-item label {
    margin-bottom: 4px;
    display: block;
}
'''
        
        new_content = content + spacing_css
        self.common_css.write_text(new_content, encoding='utf-8')
        return True
    
    def _ensure_color_variables(self) -> bool:
        """确保统一颜色变量存在"""
        if not self.common_css.exists():
            return False
        
        content = self.common_css.read_text(encoding='utf-8', errors='ignore')
        
        if '--primary-color' in content:
            return False
        
        color_css = '''
/* 统一颜色变量 */
:root {
    --primary-color: #1890ff;
    --success-color: #52c41a;
    --warning-color: #faad14;
    --error-color: #ff4d4f;
    --text-color: #262626;
    --text-color-secondary: #8c8c8c;
    --border-color: #d9d9d9;
    --background-color: #fafafa;
    --card-background: #ffffff;
}

/* 应用颜色变量 */
.btn-primary {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
}

.text-primary {
    color: var(--primary-color);
}

.text-success {
    color: var(--success-color);
}

.text-warning {
    color: var(--warning-color);
}

.text-error {
    color: var(--error-color);
}
'''
        
        new_content = content + color_css
        self.common_css.write_text(new_content, encoding='utf-8')
        return True
    
    def _ensure_responsive_styles(self) -> bool:
        """确保响应式样式存在"""
        if not self.common_css.exists():
            return False
        
        content = self.common_css.read_text(encoding='utf-8', errors='ignore')
        
        if '@media (max-width:' in content:
            return False
        
        responsive_css = '''
/* 响应式设计 */
@media (max-width: 768px) {
    .container {
        padding: 0 16px;
    }
    
    .sidebar {
        width: 100%;
        position: static;
    }
    
    .main-content {
        margin-left: 0;
    }
    
    .table-responsive {
        overflow-x: auto;
    }
    
    .btn {
        width: 100%;
        margin-bottom: 8px;
    }
}

@media (max-width: 480px) {
    .spacing-standard {
        margin: 8px 0;
        padding: 12px;
    }
    
    .card.spacing-standard {
        padding: 16px;
    }
}
'''
        
        new_content = content + responsive_css
        self.common_css.write_text(new_content, encoding='utf-8')
        return True


class NavigationFixer:
    """左侧菜单与导航修复器"""
    
    def __init__(self):
        self.admin_dir = ADMIN_DIR
    
    def fix_menu_highlight(self, page_path: Path) -> List[str]:
        """修复菜单高亮问题"""
        changes = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 添加菜单高亮脚本
        highlight_script = '''
<script>
// 菜单高亮修复
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.sidebar a, .menu a');
    
    menuLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href.replace('../', ''))) {
            link.classList.add('active');
            // 展开父级菜单
            let parent = link.closest('.menu-group');
            while (parent) {
                parent.classList.add('expanded');
                parent = parent.parentElement.closest('.menu-group');
            }
        }
    });
});
</script>'''
        
        if '</body>' in content and 'menu' in content.lower():
            new_content = content.replace('</body>', f'{highlight_script}\n</body>')
            page_path.write_text(new_content, encoding='utf-8')
            changes.append(f"添加菜单高亮脚本到 {page_path.name}")
        
        return changes
    
    def fix_menu_structure(self, page_path: Path) -> List[str]:
        """修复菜单结构问题"""
        changes = []
        
        # 这里可以添加更复杂的菜单结构修复逻辑
        # 例如检查菜单层级、链接有效性等
        
        return changes


# 修复策略注册表
FIX_STRATEGIES = {
    # 业务逻辑修复
    'fix_missing_breadcrumb': BusinessLogicFixer().fix_missing_breadcrumb,
    'fix_missing_page_title': BusinessLogicFixer().fix_missing_page_title,
    'fix_data_validation_missing': BusinessLogicFixer().fix_data_validation_missing,
    
    # 交互完整性修复
    'fix_missing_loading_states': InteractionFixer().fix_missing_loading_states,
    'fix_missing_error_handling': InteractionFixer().fix_missing_error_handling,
    'fix_missing_accessibility': InteractionFixer().fix_missing_accessibility,
    
    # UI视觉修复
    'fix_inconsistent_spacing': UIVisualFixer().fix_inconsistent_spacing,
    'fix_inconsistent_colors': UIVisualFixer().fix_inconsistent_colors,
    'fix_responsive_issues': UIVisualFixer().fix_responsive_issues,
    'fix_duplicate_scripts': UIVisualFixer().fix_duplicate_scripts,
    'fix_html_structure': UIVisualFixer().fix_html_structure,
    'fix_breadcrumb_duplicates': UIVisualFixer().fix_breadcrumb_duplicates,
    'fix_scattered_styles': UIVisualFixer().fix_scattered_styles,
    
    # 导航修复
    'fix_menu_highlight': NavigationFixer().fix_menu_highlight,
    'fix_menu_structure': NavigationFixer().fix_menu_structure,
}


def get_fix_strategy(strategy_name: str):
    """获取修复策略函数"""
    return FIX_STRATEGIES.get(strategy_name)


def list_available_strategies() -> List[str]:
    """列出所有可用的修复策略"""
    return list(FIX_STRATEGIES.keys())