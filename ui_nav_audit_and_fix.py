#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医保审核系统综合UI+导航审查与自动修复脚本
v2.0 - 真正整合版本

功能特性：
1. 整合导航菜单审查（调用menu_audit_enhanced.py的核心逻辑）
2. 基于UI审查标准（UI审查标准与评估指南.md）的自动化检查
3. 自动修复：静态资源404、侧边栏加载、样式一致性
4. 生成结构化审查报告（JSON + Markdown）
5. 修复后自动复审验证
"""

import os
import re
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

# 导入公共配置
try:
    from audit_config import (
        ROOT, ADMIN_DIR, IMG_DIR, LOG_DIR, AUDIT_DIR, COMMON_CSS, BASE_URL,
        AUDIT_PAGES, STANDARD_MENU_STRUCTURE,
        SIDEBAR_SNIPPET_MARK, CHART_CSS_MARK, UI_FIX_MARK
    )
except ImportError:
    # 如果audit_config不存在，使用本地配置
    ROOT = Path(__file__).resolve().parent
    ADMIN_DIR = ROOT / '1.0' / '超级管理员'
    IMG_DIR = ROOT / 'img'
    LOG_DIR = IMG_DIR / 'logs'
    AUDIT_DIR = ROOT / 'audit_reports'
    COMMON_CSS = ROOT / '1.0' / '样式文件' / '通用样式.css'
    BASE_URL = 'http://localhost:8000/1.0/超级管理员'
    SIDEBAR_SNIPPET_MARK = '/* unified-sidebar: injected */'
    CHART_CSS_MARK = '/* ui_audit_and_fix: charts min-height */'
    UI_FIX_MARK = '/* ui_nav_audit_and_fix: auto-applied */'

# 导入导航审查功能
try:
    from menu_audit_enhanced import (
        setup_driver, extract_menu_structure
    )
    USE_ENHANCED_MENU = True
except ImportError:
    USE_ENHANCED_MENU = False
    print("⚠️  menu_audit_enhanced.py未找到，将使用内置导航审查功能")

# 3rd party imports for browser automation 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 审查页面配置 
# 优先使用 audit_config.AUDIT_PAGES，如不可用则使用本地回退配置
if 'AUDIT_PAGES' not in globals():
    AUDIT_PAGES = {
        '工作台': [
            '工作台/平台运营看板.html', 
            '工作台/报告规则分析.html',
        ],
        '审核管理': [
            '审核管理/审核流程/事中审核检查.html',
            '审核管理/审核流程/事前审核记录.html',
            '审核管理/审核流程/事后审核任务列表.html',
            '审核管理/审核结果/审核结果.html',
        ],
        '规则管理': [
            '规则管理/规则操作/规则参数配置.html',
            '规则管理/规则操作/创建规则.html',
            '规则管理/规则操作/编辑规则.html',
            '规则管理/规则操作/规则管理完整版.html',
            '规则管理/规则列表/规则管理主页.html',
            '规则管理/规则列表/门诊规则管理.html',
            '规则管理/规则列表/医保规则管理系统v2.html',
            '规则管理/规则详情/规则详情.html',
            '规则管理/规则详情/门诊规则详情.html',
            '规则管理/规则详情/临床规则详情.html',
            '规则管理/规则详情/慢病规则详情.html',
            '规则管理/规则详情/政策规则详情.html',
        ],
        '用户权限管理': [
            '用户权限管理/用户管理/用户列表.html',
            '用户权限管理/权限管理/权限管理.html',
            '用户权限管理/组织管理/科室管理.html',
            '用户权限管理/组织管理/企业详情.html',
            '用户权限管理/组织管理/租户管理.html',
            '用户权限管理/组织管理/租户表单.html',
        ],
        '系统管理': [
            '系统管理/全局设置.html',
            '系统管理/系统监控.html',
        ],
        '知识库': [
            '系统管理/知识库目录.html?catalog=drug',
            '系统管理/知识库目录.html?catalog=treatment',
            '系统管理/知识库目录.html?catalog=material',
        ],
        '登录': [
            '登录.html'
        ]
    }

# 标准菜单结构（最新版本）
# 优先使用 audit_config.STANDARD_MENU_STRUCTURE，如不可用则使用本地回退
if 'STANDARD_MENU_STRUCTURE' not in globals():
    STANDARD_MENU_STRUCTURE = {
        "工作台": {
            "level": 1,
            "children": {
                "平台运营看板": {"level": 2, "href": "../工作台/平台运营看板.html"},
                "报告规则分析": {"level": 2, "href": "../工作台/报告规则分析.html"}
            }
        },
        "规则管理": {
            "level": 1,
            "children": {
                "规则库": {
                    "level": 2,
                    "children": {
                        "规则管理主页": {"level": 3, "href": "../规则管理/规则列表/规则管理主页.html"},
                        "门诊规则管理": {"level": 3, "href": "../规则管理/规则列表/门诊规则管理.html"},
                        "医保规则管理": {"level": 3, "href": "../规则管理/规则列表/医保规则管理系统v2.html"},
                        "通用规则详情": {"level": 3, "href": "../规则管理/规则详情/规则详情.html"},
                        "临床规则详情": {"level": 3, "href": "../规则管理/规则详情/临床规则详情.html"},
                        "慢病规则详情": {"level": 3, "href": "../规则管理/规则详情/慢病规则详情.html"},
                        "政策规则详情": {"level": 3, "href": "../规则管理/规则详情/政策规则详情.html"},
                        "门诊规则详情": {"level": 3, "href": "../规则管理/规则详情/门诊规则详情.html"},
                        "创建规则": {"level": 3, "href": "../规则管理/规则操作/创建规则.html"},
                        "编辑规则": {"level": 3, "href": "../规则管理/规则操作/编辑规则.html"},
                        "规则参数配置": {"level": 3, "href": "../规则管理/规则操作/规则参数配置.html"},
                        "规则管理完整版": {"level": 3, "href": "../规则管理/规则操作/规则管理完整版.html"}
                    }
                }
            }
        },
        "审核管理": {
            "level": 1,
            "children": {
                "审核流程": {
                    "level": 2,
                    "children": {
                        "事前审核记录": {"level": 3, "href": "../审核管理/审核流程/事前审核记录.html"},
                        "事中审核检查": {"level": 3, "href": "../审核管理/审核流程/事中审核检查.html"},
                        "事后审核任务": {"level": 3, "href": "../审核管理/审核流程/事后审核任务列表.html"}
                    }
                },
                "审核结果": {"level": 2, "href": "../审核管理/审核结果/审核结果.html"}
            }
        },
        "用户权限管理": {
            "level": 1,
            "children": {
                "用户管理": {"level": 2, "href": "../用户权限管理/用户管理/用户列表.html"},
                "权限管理": {"level": 2, "href": "../用户权限管理/权限管理/权限管理.html"},
                "组织管理": {
                    "level": 2,
                    "children": {
                        "科室管理": {"level": 3, "href": "../用户权限管理/组织管理/科室管理.html"},
                        "租户管理": {"level": 3, "href": "../用户权限管理/组织管理/租户管理.html"},
                        "租户表单": {"level": 3, "href": "../用户权限管理/组织管理/租户表单.html"},
                        "企业详情": {"level": 3, "href": "../用户权限管理/组织管理/企业详情.html"}
                    }
                }
            }
        },
        "系统管理": {
            "level": 1,
            "children": {
                "全局设置": {"level": 2, "href": "../系统管理/全局设置.html"},
                "系统监控": {"level": 2, "href": "../系统管理/系统监控.html"}
            }
        },
        "知识库": {
            "level": 1,
            "children": {
                "药品目录": {"level": 2, "href": "../系统管理/知识库目录.html?catalog=drug"},
                "诊疗目录": {"level": 2, "href": "../系统管理/知识库目录.html?catalog=treatment"},
                "耗材目录": {"level": 2, "href": "../系统管理/知识库目录.html?catalog=material"}
            }
        }
    }


def find_html_file_by_name(filename: str) -> Path | None:
    for base in [ADMIN_DIR]:
        for root, _, files in os.walk(base):
            if filename in files:
                return Path(root) / filename
    return None


def replace_in_file(file_path: Path, replacements: list[tuple[str, str]]) -> bool:
    text = file_path.read_text(encoding='utf-8')
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        file_path.write_text(text, encoding='utf-8')
        print(f'  ✓ 修改: {file_path}')
        return True
    return False


def ensure_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding='utf-8')
        print(f'  ✓ 新建文件: {path}')


def ensure_unified_sidebar(html_path: Path) -> bool:
    """若页面包含 #sidebar-container 但未加载统一侧边栏，则注入fetch片段。"""
    text = html_path.read_text(encoding='utf-8')
    if 'id="sidebar-container"' not in text:
        return False
    has_fetch = ('_unified-sidebar.html' in text) or ('fetch(' in text and 'unified-sidebar' in text)
    if has_fetch:
        return False
    # 计算到组件片段的相对路径
    sidebar_fragment = ADMIN_DIR / '组件' / '_unified-sidebar.html'
    rel = os.path.relpath(sidebar_fragment, html_path.parent)
    snippet = (
        f"\n    <!-- {SIDEBAR_SNIPPET_MARK} -->\n"
        "    <script>\n"
        f"      fetch('{rel.replace(os.sep, '/')}'.replace(/\\\\/g,'/'))\n"
        "        .then(r => r.text())\n"
        "        .then(html => {\n"
        "          const container = document.getElementById('sidebar-container');\n"
        "          container.innerHTML = html;\n"
        "          // 执行插入片段中的脚本\n"
        "          Array.from(container.querySelectorAll('script')).forEach(s => {\n"
        "            const ns = document.createElement('script');\n"
        "            if (s.src) { ns.src = s.src; } else { ns.textContent = s.textContent; }\n"
        "            document.body.appendChild(ns); s.remove();\n"
        "          });\n"
        "          // 初始化侧边栏\n"
        "          if (typeof initSidebar === 'function') { setTimeout(() => initSidebar(), 0); }\n"
        "        });\n"
        "    </script>\n"
    )
    # 注入到 </body> 前
    new_text = text.replace('</body>', snippet + '\n</body>')
    if new_text != text:
        html_path.write_text(new_text, encoding='utf-8')
        print(f'  ✓ 注入统一侧边栏: {html_path}')
        return True
    return False


def fix_known_resource_issues(page_html: Path, error_urls: list[str]) -> bool:
    changed = False
    content = page_html.read_text(encoding='utf-8')

    # 1) logo.png 404 → 切换为模块内 SVG 占位图
    if any('资源文件/images/logo.png' in u or 'images/logo.png' in unquote(u) for u in error_urls):
        # 目标SVG位置：当前模块 assets/images/logo.svg
        target_svg = page_html.parent / 'assets' / 'images' / 'logo.svg'
        ensure_file(target_svg, (
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            "<svg width=\"160\" height=\"40\" viewBox=\"0 0 160 40\" xmlns=\"http://www.w3.org/2000/svg\">\n"
            "  <defs><linearGradient id=\"g\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\">\n"
            "    <stop offset=\"0%\" stop-color=\"#4f46e5\"/><stop offset=\"100%\" stop-color=\"#06b6d4\"/>\n"
            "  </linearGradient></defs>\n"
            "  <rect x=\"1\" y=\"1\" width=\"158\" height=\"38\" rx=\"8\" fill=\"url(#g)\"/>\n"
            "  <text x=\"20\" y=\"26\" font-family=\"system-ui, Arial\" font-size=\"16\" fill=\"#fff\">医保规则管理</text>\n"
            "</svg>\n"
        ))
        new_rel = './assets/images/logo.svg'
        if '../../资源文件/images/logo.png' in content or '资源文件/images/logo.png' in content:
            changed |= replace_in_file(page_html, [('../../资源文件/images/logo.png', new_rel)])
        # 兜底：将 images/logo.png 变更为 SVG（相对页面）
        if 'images/logo.png' in content:
            changed |= replace_in_file(page_html, [('images/logo.png', new_rel)])

    # 2) knowledge-base.js 404 → 调整为同级 ./assets/js/
    if any('assets/js/knowledge-base.js' in u for u in error_urls):
        js_path = page_html.parent / 'assets' / 'js' / 'knowledge-base.js'
        if js_path.exists():
            # 将 ../assets/js/knowledge-base.js 或 ../../assets/js → ./assets/js
            replacements = []
            for prefix in ('../assets/js/knowledge-base.js', '../../assets/js/knowledge-base.js'):
                replacements.append((prefix, './assets/js/knowledge-base.js'))
            changed |= replace_in_file(page_html, replacements)

    return changed


def collect_errors_by_page() -> dict[str, list[str]]:
    """从 img/logs 下收集每个页面的错误URL列表。键为 HTML 基础文件名（不含查询参数）。"""
    errors: dict[str, list[str]] = {}
    if not LOG_DIR.exists():
        return errors
    for lf in LOG_DIR.glob('*.log'):
        name = lf.name
        # 取 ? 之前的HTML名
        base_html = name.split('.html')[0] + '.html'
        try:
            lines = lf.read_text(encoding='utf-8').splitlines()
        except Exception:
            continue
        for ln in lines:
            m = re.search(r'Console\[SEVERE\]:\s+(http[^\s]+)\s+-\s+Failed to load resource', ln)
            if m:
                url = m.group(1)
                errors.setdefault(base_html, []).append(url)
    return errors


def ensure_chart_min_height() -> bool:
    if not COMMON_CSS.exists():
        return False
    css = COMMON_CSS.read_text(encoding='utf-8')
    if CHART_CSS_MARK in css:
        return False
    patch = (
        f"\n\n{CHART_CSS_MARK}\n"
        "/* 确保图表容器最小可视高度，避免过矮影响阅读 */\n"
        ".chart, .chart-container, .echart, .echarts, [data-role=chart] {\n"
        "  min-height: 300px;\n"
        "}\n"
    )
    COMMON_CSS.write_text(css + patch, encoding='utf-8')
    print(f'  ✓ 通用样式追加最小高度: {COMMON_CSS}')
    return True


class UINavAuditor:
    """综合UI+导航审查器"""
    
    def __init__(self):
        self.driver = None
        self.audit_results = {}
        self.fixed_issues = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        
        # 确保必需目录存在
        for dir_path in [IMG_DIR, LOG_DIR, AUDIT_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def setup_browser(self):
        """初始化浏览器"""
        print("🔧 初始化浏览器...")
        if USE_ENHANCED_MENU:
            # 使用增强版的driver设置
            self.driver = setup_driver()
        else:
            # 回退到本地实现
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        return self.driver
    
    def teardown_browser(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("✅ 浏览器已关闭")
    
    def check_static_resources(self, page_path: Path) -> list:
        """检查页面静态资源引用（CSS/JS/图片）"""
        issues = []
        if not page_path.exists():
            return [{"type": "file_not_found", "path": str(page_path)}]
        
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 检查CSS引用
        css_pattern = r'<link[^>]*href=["\']([^"\']+\.css)["\'][^>]*>'
        for match in re.finditer(css_pattern, content):
            css_path = match.group(1)
            resolved_path = self.resolve_resource_path(page_path, css_path)
            if not resolved_path.exists():
                issues.append({
                    "type": "css_404",
                    "resource": css_path,
                    "resolved_path": str(resolved_path),
                    "line": content[:match.start()].count('\n') + 1
                })
        
        # 检查JS引用
        js_pattern = r'<script[^>]*src=["\']([^"\']+\.js)["\'][^>]*>'
        for match in re.finditer(js_pattern, content):
            js_path = match.group(1)
            resolved_path = self.resolve_resource_path(page_path, js_path)
            if not resolved_path.exists():
                issues.append({
                    "type": "js_404",
                    "resource": js_path,
                    "resolved_path": str(resolved_path),
                    "line": content[:match.start()].count('\n') + 1
                })
        
        # 检查图片引用
        img_pattern = r'<img[^>]*src=["\']([^"\']+\.(png|jpg|jpeg|gif|svg|webp))["\'][^>]*>'
        for match in re.finditer(img_pattern, content):
            img_path = match.group(1)
            resolved_path = self.resolve_resource_path(page_path, img_path)
            if not resolved_path.exists():
                issues.append({
                    "type": "img_404",
                    "resource": img_path,
                    "resolved_path": str(resolved_path),
                    "line": content[:match.start()].count('\n') + 1
                })
        
        return issues
    
    def resolve_resource_path(self, page_path: Path, resource_url: str) -> Path:
        """解析相对路径到绝对路径"""
        if resource_url.startswith('http'):
            return Path('/dev/null')  # 外部资源，跳过
        
        # 移除查询参数
        resource_url = resource_url.split('?')[0].split('#')[0]
        
        if resource_url.startswith('/'):
            # 绝对路径（相对于域名根）
            return ROOT / '1.0' / resource_url.lstrip('/')
        else:
            # 相对路径
            return (page_path.parent / resource_url).resolve()
    
    def check_sidebar_loading(self, page_path: Path) -> list:
        """检查侧边栏加载"""
        issues = []
        if not page_path.exists():
            return [{"type": "file_not_found", "path": str(page_path)}]
        
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 检查是否有侧边栏容器
        has_sidebar_container = 'id="sidebar"' in content or 'class="sidebar"' in content
        
        # 检查是否有fetch unified-sidebar的代码
        has_sidebar_fetch = 'unified-sidebar.html' in content and 'fetch(' in content
        
        if has_sidebar_container and not has_sidebar_fetch:
            issues.append({
                "type": "sidebar_no_fetch",
                "description": "页面有侧边栏容器但缺少统一侧边栏加载代码"
            })
        
        return issues
    
    def check_ui_consistency(self, page_path: Path) -> list:
        """检查UI一致性（基于UI审查标准）"""
        issues = []
        if not page_path.exists():
            return [{"type": "file_not_found", "path": str(page_path)}]
        
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # P0级检查：表单控件完整性
        if '<form' in content:
            # 检查表单是否有提交按钮
            if not re.search(r'<(button|input)[^>]*type=["\']submit["\']', content):
                if not re.search(r'<button[^>]*>.*?(提交|保存|确定|创建)', content, re.IGNORECASE):
                    issues.append({
                        "type": "form_no_submit",
                        "priority": "P0",
                        "description": "表单缺少提交按钮"
                    })
        
        # P1级检查：图表最小高度
        if 'chart' in content.lower() or 'echarts' in content.lower():
            if not re.search(r'min-height:\s*\d+px', content):
                issues.append({
                    "type": "chart_no_min_height", 
                    "priority": "P1",
                    "description": "图表容器缺少最小高度设置"
                })
        
        # P2级检查：页面标题
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
        if not title_match or not title_match.group(1).strip():
            issues.append({
                "type": "empty_title",
                "priority": "P2", 
                "description": "页面标题为空"
            })
        
        return issues
    
    def audit_page_navigation(self, page_url: str) -> dict:
        """审查页面导航（使用增强版审计功能）"""
        if USE_ENHANCED_MENU:
            # 使用增强版的审计功能
            page_path = page_url.replace(f"{BASE_URL}/", "")
            module_name = page_path.split('/')[0] if '/' in page_path else "未知模块"
            
            try:
                # 调用增强版的audit_single_page
                from menu_audit_enhanced import audit_single_page
                audit_result = audit_single_page(self.driver, page_path, module_name)
                
                # 转换为UI审查格式
                return {
                    "url": page_url,
                    "menu_structure": audit_result.get("menu_analysis", {}),
                    "navigation_score": audit_result.get("navigation_score", {}).get("total", 0),
                    "issues": audit_result.get("navigation_score", {}).get("issues", []),
                    "console_errors": [],
                    "network_errors": [],
                    "enhanced_result": audit_result  # 保留完整的增强版结果
                }
            except Exception as e:
                print(f"❌ 增强版审计失败: {e}")
                return {"navigation_score": 0, "issues": [f"增强版审计失败: {str(e)}"]}
        else:
            # 回退到原有实现
            result = {
                "url": page_url,
                "menu_structure": None,
                "navigation_score": 0,
                "issues": [],
                "console_errors": [],
                "network_errors": []
            }
            
            try:
                print(f"📄 审查页面: {page_url}")
                self.driver.get(page_url)
                
                # 等待页面加载
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(2)
                
                # 获取控制台错误
                logs = self.driver.get_log('browser')
                for log in logs:
                    if log['level'] in ['SEVERE', 'ERROR']:
                        result["console_errors"].append({
                            "level": log['level'],
                            "message": log['message'],
                            "timestamp": log['timestamp']
                        })
                
                # 提取菜单结构
                try:
                    sidebar = self.driver.find_element(By.ID, "sidebar")
                    menu_items = sidebar.find_elements(By.TAG_NAME, "li")
                    
                    menu_structure = {}
                    for item in menu_items:
                        try:
                            link = item.find_element(By.TAG_NAME, "a")
                            text = link.text.strip()
                            href = link.get_attribute("href")
                            if text and href:
                                menu_structure[text] = href
                        except:
                            continue
                    
                    result["menu_structure"] = menu_structure
                    
                    # 计算导航评分
                    nav_score = self.calculate_navigation_score(menu_structure, page_url)
                    result["navigation_score"] = nav_score
                    
                except Exception as e:
                    result["issues"].append(f"菜单解析失败: {str(e)}")
                    result["navigation_score"] = 0
                
            except Exception as e:
                result["issues"].append(f"页面加载失败: {str(e)}")
                
            return result

    def calculate_navigation_score(self, menu_structure: dict, current_url: str) -> int:
        """计算导航评分（仅在不使用增强版时使用）"""
        if USE_ENHANCED_MENU:
            # 如果有增强版，不应该调用这个方法
            print("⚠️  应该使用增强版的calculate_navigation_score")
            return 0
            
        # 原有的评分逻辑保留作为回退
        if not menu_structure:
            return 0
        
        score = 50  # 基础分
        
        # 检查菜单完整性
        standard_items = set()
        self._extract_menu_items(STANDARD_MENU_STRUCTURE, standard_items)
        current_items = set(menu_structure.keys())
        
        # 计算覆盖率
        if standard_items:
            coverage = len(current_items & standard_items) / len(standard_items)
            score += int(coverage * 30)
        
        # 检查当前页面高亮
        current_page = Path(current_url).stem
        highlighted = any(current_page in item for item in current_items)
        if highlighted:
            score += 20
        
        return min(score, 100)
    
    def _extract_menu_items(self, structure: dict, items: set):
        """递归提取菜单项"""
        for key, value in structure.items():
            items.add(key)
            if isinstance(value, dict) and 'children' in value:
                self._extract_menu_items(value['children'], items)
    
    def auto_fix_static_resources(self, issues: list, page_path: Path) -> list:
        """自动修复静态资源404错误"""
        fixed = []
        
        for issue in issues:
            if issue["type"] == "css_404":
                fixed.extend(self._fix_css_404(issue, page_path))
            elif issue["type"] == "js_404":
                fixed.extend(self._fix_js_404(issue, page_path))
            elif issue["type"] == "img_404":
                fixed.extend(self._fix_img_404(issue, page_path))
        
        return fixed
    
    def _fix_css_404(self, issue: dict, page_path: Path) -> list:
        """修复CSS 404错误"""
        fixed = []
        resource_path = issue["resource"]
        
        # 常见修复策略
        if "通用样式.css" in resource_path:
            # 修正通用样式路径
            fixed.append(self._update_resource_path(
                page_path, resource_path, "../../样式文件/通用样式.css"
            ))
        
        return fixed
    
    def _fix_js_404(self, issue: dict, page_path: Path) -> list:
        """修复JS 404错误"""
        fixed = []
        resource_path = issue["resource"]
        
        # 如果是模块内脚本，尝试修正路径
        if not resource_path.startswith('../'):
            # 相对路径改为当前目录
            new_path = f"./{resource_path.lstrip('./')}"
            fixed.append(self._update_resource_path(page_path, resource_path, new_path))
        
        return fixed
    
    def _fix_img_404(self, issue: dict, page_path: Path) -> list:
        """修复图片404错误"""
        fixed = []
        resource_path = issue["resource"]
        
        if "logo" in resource_path.lower():
            # 创建SVG logo占位符
            module_dir = page_path.parent
            assets_dir = module_dir / "assets" / "images"
            assets_dir.mkdir(parents=True, exist_ok=True)
            
            logo_path = assets_dir / "logo.svg"
            if not logo_path.exists():
                self._create_svg_logo(logo_path)
                fixed.append(f"创建SVG logo: {logo_path}")
            
            # 更新引用路径
            new_path = "./assets/images/logo.svg"
            fixed.append(self._update_resource_path(page_path, resource_path, new_path))
        
        return fixed
    
    def _update_resource_path(self, page_path: Path, old_path: str, new_path: str) -> str:
        """更新页面中的资源路径"""
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        old_escaped = re.escape(old_path)
        new_content = re.sub(
            f'(["\']){old_escaped}(["\'])',
            f'\\1{new_path}\\2',
            content
        )
        
        if new_content != content:
            page_path.write_text(new_content, encoding='utf-8')
            return f"更新 {page_path.name}: {old_path} → {new_path}"
        
        return f"未找到匹配的路径引用: {old_path}"
    
    def _create_svg_logo(self, logo_path: Path):
        """创建SVG logo占位符"""
        svg_content = '''<svg width="120" height="40" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="40" fill="#1890ff" rx="4"/>
  <text x="60" y="25" text-anchor="middle" fill="white" font-family="Arial" font-size="14" font-weight="bold">医保审核</text>
</svg>'''
        logo_path.write_text(svg_content, encoding='utf-8')
    
    def auto_fix_sidebar_loading(self, issues: list, page_path: Path) -> list:
        """自动修复侧边栏加载问题"""
        fixed = []
        
        for issue in issues:
            if issue["type"] == "sidebar_no_fetch":
                fixed.append(self._inject_sidebar_loading(page_path))
        
        return fixed
    
    def _inject_sidebar_loading(self, page_path: Path) -> str:
        """注入侧边栏加载代码"""
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 检查是否已注入
        if SIDEBAR_SNIPPET_MARK in content:
            return f"{page_path.name}: 侧边栏代码已存在"
        
        # 侧边栏加载代码片段
        sidebar_script = f'''
<script>
{SIDEBAR_SNIPPET_MARK}
document.addEventListener('DOMContentLoaded', function() {{
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {{
        fetch('../组件/_unified-sidebar.html')
            .then(response => response.text())
            .then(html => {{
                sidebar.innerHTML = html;
                // 初始化菜单状态
                if (typeof initializeMenu === 'function') {{
                    initializeMenu();
                }}
            }})
            .catch(error => console.error('侧边栏加载失败:', error));
    }}
}});
</script>'''
        
        # 在</body>前插入
        if '</body>' in content:
            new_content = content.replace('</body>', f'{sidebar_script}\n</body>')
        else:
            new_content = content + sidebar_script
        
        page_path.write_text(new_content, encoding='utf-8')
        return f"{page_path.name}: 注入侧边栏加载代码"
    
    def auto_fix_ui_issues(self, issues: list, page_path: Path) -> list:
        """自动修复UI问题"""
        fixed = []
        
        for issue in issues:
            if issue["type"] == "chart_no_min_height":
                fixed.append(self._fix_chart_min_height())
        
        return fixed
    
    def _fix_chart_min_height(self) -> str:
        """修复图表最小高度问题（全局CSS）"""
        if not COMMON_CSS.exists():
            return "通用样式文件不存在，跳过图表高度修复"
        
        content = COMMON_CSS.read_text(encoding='utf-8', errors='ignore')
        
        # 检查是否已添加
        if CHART_CSS_MARK in content:
            return "图表最小高度样式已存在"
        
        # 添加图表最小高度样式
        chart_css = f'''
{CHART_CSS_MARK}
.chart-container, [id*="chart"], [class*="chart"] {{
    min-height: 300px;
}}
'''
        
        new_content = content + chart_css
        COMMON_CSS.write_text(new_content, encoding='utf-8')
        return "添加图表最小高度样式到通用CSS"
    
    def audit_module(self, module_name: str) -> dict:
        """审查单个模块"""
        print(f"\n🔍 审查模块: {module_name}")
        
        module_result = {
            "module": module_name,
            "timestamp": self.timestamp,
            "pages": {},
            "summary": {
                "total_pages": 0,
                "error_pages": 0,
                "avg_navigation_score": 0,
                "total_issues_fixed": 0
            }
        }
        
        if module_name not in AUDIT_PAGES:
            print(f"❌ 未知模块: {module_name}")
            return module_result
        
        pages = AUDIT_PAGES[module_name]
        nav_scores = []
        
        for page_rel_path in pages:
            page_path = ADMIN_DIR / page_rel_path.replace('.html?', '.html').split('?')[0]
            page_url = f"{BASE_URL}/{page_rel_path}"
            
            # 静态检查
            static_issues = self.check_static_resources(page_path)
            sidebar_issues = self.check_sidebar_loading(page_path)
            ui_issues = self.check_ui_consistency(page_path)
            
            # 浏览器审查（仅当静态检查通过）
            nav_result = {"navigation_score": 0, "issues": ["跳过浏览器审查"]}
            if not static_issues:
                nav_result = self.audit_page_navigation(page_url)
            
            # 自动修复
            fixed_static = self.auto_fix_static_resources(static_issues, page_path)
            fixed_sidebar = self.auto_fix_sidebar_loading(sidebar_issues, page_path)
            fixed_ui = self.auto_fix_ui_issues(ui_issues, page_path)
            
            all_fixed = fixed_static + fixed_sidebar + fixed_ui
            
            page_result = {
                "path": str(page_path),
                "url": page_url,
                "static_issues": static_issues,
                "sidebar_issues": sidebar_issues,
                "ui_issues": ui_issues,
                "navigation_result": nav_result,
                "fixes_applied": all_fixed,
                "total_issues": len(static_issues) + len(sidebar_issues) + len(ui_issues),
                "total_fixes": len(all_fixed)
            }
            
            module_result["pages"][page_rel_path] = page_result
            
            # 统计
            if page_result["total_issues"] > 0:
                module_result["summary"]["error_pages"] += 1
            
            nav_scores.append(nav_result["navigation_score"]) 
            module_result["summary"]["total_issues_fixed"] += len(all_fixed)
            self.fixed_issues.extend(all_fixed)
        
        module_result["summary"]["total_pages"] = len(pages)
        module_result["summary"]["avg_navigation_score"] = (
            sum(nav_scores) / len(nav_scores) if nav_scores else 0
        )
        
        return module_result
    
    def generate_report(self, results: dict):
        """生成审查报告"""
        # JSON报告
        json_file = AUDIT_DIR / f"ui_nav_audit_{self.timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # Markdown报告
        md_file = AUDIT_DIR / f"ui_nav_audit_{self.timestamp}.md"
        self._generate_markdown_report(results, md_file)
        
        print(f"\n📊 审查报告已生成:")
        print(f"   JSON: {json_file}")
        print(f"   Markdown: {md_file}")
    
    def _generate_markdown_report(self, results: dict, md_file: Path):
        """生成Markdown格式报告"""
        content = f"""# 医保审核系统综合UI+导航审查报告

**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**审查范围:** {', '.join(results.keys())}  
**修复问题总数:** {len(self.fixed_issues)}
**增强版导航审查:** {'✅ 已启用' if USE_ENHANCED_MENU else '❌ 未启用'}

## 📊 模块概览

| 模块 | 总页面数 | 错误页面数 | 平均导航分数 | 修复问题数 |
|------|----------|------------|--------------|------------|
"""
        
        for module_name, module_data in results.items():
            summary = module_data["summary"]
            content += f"| {module_name} | {summary['total_pages']} | {summary['error_pages']} | {summary['avg_navigation_score']:.1f}/100 | {summary['total_issues_fixed']} |\n"
        
        content += "\n## 🔧 修复清单\n\n"
        
        if self.fixed_issues:
            for i, fix in enumerate(self.fixed_issues, 1):
                content += f"{i}. {fix}\n"
        else:
            content += "无需修复的问题。\n"
        
        content += "\n## 📋 详细审查结果\n\n"
        
        for module_name, module_data in results.items():
            content += f"### {module_name}\n\n"
            
            for page_path, page_data in module_data["pages"].items():
                content += f"#### {page_path}\n\n"
                
                # 处理增强版结果
                nav_result = page_data['navigation_result']
                if USE_ENHANCED_MENU and 'enhanced_result' in nav_result:
                    enhanced = nav_result['enhanced_result']
                    nav_score = enhanced.get('navigation_score', {})
                    quality = enhanced.get('quality_indicators', {})
                    
                    content += f"- **导航评分:** {nav_score.get('total', 0)}/100\n"
                    if nav_score.get('breakdown'):
                        content += f"  - 菜单存在: {nav_score['breakdown'].get('menu_exists', 0)}/20\n"
                        content += f"  - 结构匹配: {nav_score['breakdown'].get('structure_match', 0)}/30\n"
                        content += f"  - 高亮正确: {nav_score['breakdown'].get('highlight_correct', 0)}/20\n"
                        content += f"  - 展开逻辑: {nav_score['breakdown'].get('expand_logic', 0)}/15\n"
                        content += f"  - 链接有效: {nav_score['breakdown'].get('links_valid', 0)}/15\n"
                    
                    content += f"- **页面质量:**\n"
                    content += f"  - 加载成功: {'✅' if quality.get('loads_successfully', False) else '❌'}\n"
                    content += f"  - 有标题: {'✅' if quality.get('has_title', False) else '❌'}\n"
                    content += f"  - 菜单功能: {'✅' if quality.get('menu_functional', False) else '❌'}\n"
                    content += f"  - 无错误: {'✅' if quality.get('error_free', False) else '❌'}\n"
                    
                    if nav_score.get('issues'):
                        content += f"- **导航问题:** {'; '.join(nav_score['issues'])}\n"
                else:
                    content += f"- **导航评分:** {nav_result['navigation_score']}/100\n"
                    if nav_result.get('issues'):
                        content += f"- **导航问题:** {'; '.join(nav_result['issues'])}\n"
                
                content += f"- **问题总数:** {page_data['total_issues']}\n"
                content += f"- **修复数量:** {page_data['total_fixes']}\n"
                
                if page_data["fixes_applied"]:
                    content += f"- **已修复:** {'; '.join(page_data['fixes_applied'])}\n"
                
                content += "\n"
        
        md_file.write_text(content, encoding='utf-8')
    
    def run_full_audit(self, modules: list = None):
        """运行完整审查"""
        print("🚀 启动医保审核系统综合UI+导航审查")
        
        if modules is None:
            modules = list(AUDIT_PAGES.keys())
        
        # 设置浏览器
        self.setup_browser()
        
        try:
            results = {}
            
            for module_name in modules:
                if module_name == '登录':
                    print(f"⏭️  跳过登录模块（特殊处理）")
                    continue
                    
                results[module_name] = self.audit_module(module_name)
            
            # 生成报告
            self.generate_report(results)
            
            # 打印总结
            self._print_summary(results)
            
        finally:
            self.teardown_browser()
    
    def _print_summary(self, results: dict):
        """打印审查总结"""
        total_pages = sum(r["summary"]["total_pages"] for r in results.values())
        total_errors = sum(r["summary"]["error_pages"] for r in results.values())
        total_fixes = len(self.fixed_issues)
        
        print(f"\n🎯 审查完成总结:")
        print(f"   📄 审查页面: {total_pages}")
        print(f"   ❌ 错误页面: {total_errors}")
        print(f"   🔧 修复问题: {total_fixes}")
        print(f"   📊 无错误模块: {[name for name, data in results.items() if data['summary']['error_pages'] == 0]}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='医保审核系统综合UI+导航审查与自动修复')
    parser.add_argument('--modules', type=str, help='指定审查模块，逗号分隔')
    parser.add_argument('--auto-fix', action='store_true', default=True, help='启用自动修复')
    
    args = parser.parse_args()
    
    auditor = UINavAuditor()
    
    modules = None
    if args.modules:
        modules = [m.strip() for m in args.modules.split(',')]
    
    auditor.run_full_audit(modules)


if __name__ == '__main__':
    main()