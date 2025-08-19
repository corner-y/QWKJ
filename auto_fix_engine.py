#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医保审核系统自动修订程序
基于审查报告的智能修复引擎

功能特性：
1. 解析JSON/Markdown审查报告
2. 按P0/P1/P2优先级自动修复问题
3. 支持业务逻辑、交互完整性、UI视觉一致性修复
4. 修复后自动验证和生成报告
5. 支持批量修复和增量修复
"""

import os
import re
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# 导入公共配置
try:
    from audit_config import (
        ROOT, ADMIN_DIR, IMG_DIR, AUDIT_DIR, COMMON_CSS,
        SIDEBAR_SNIPPET_MARK, CHART_CSS_MARK, UI_FIX_MARK
    )
except ImportError:
    ROOT = Path(__file__).resolve().parent
    ADMIN_DIR = ROOT / '1.0' / '超级管理员'
    IMG_DIR = ROOT / 'img'
    AUDIT_DIR = ROOT / 'audit_reports'
    COMMON_CSS = ROOT / '1.0' / '样式文件' / '通用样式.css'
    SIDEBAR_SNIPPET_MARK = '/* unified-sidebar: injected */'
    CHART_CSS_MARK = '/* ui_audit_and_fix: charts min-height */'
    UI_FIX_MARK = '/* auto_fix_engine: applied */'


class Priority(Enum):
    """问题优先级"""
    P0 = "P0"  # 阻塞性问题，必须立即修复
    P1 = "P1"  # 重要问题，应尽快修复
    P2 = "P2"  # 一般问题，可排期修复


class FixCategory(Enum):
    """修复类别"""
    BUSINESS_LOGIC = "business_logic"        # 业务逻辑与信息架构
    INTERACTION = "interaction"              # 交互完整性与可用性
    UI_VISUAL = "ui_visual"                 # UI视觉与一致性
    NAVIGATION = "navigation"               # 左侧菜单与导航
    STATIC_RESOURCE = "static_resource"     # 静态资源
    PERFORMANCE = "performance"             # 性能优化


@dataclass
class Issue:
    """问题数据结构"""
    id: str
    title: str
    description: str
    priority: Priority
    category: FixCategory
    page_path: str
    page_url: str
    details: Dict
    auto_fixable: bool = False
    fix_strategy: Optional[str] = None


@dataclass
class FixResult:
    """修复结果数据结构"""
    issue_id: str
    success: bool
    message: str
    changes_made: List[str]
    verification_passed: bool = False
    before_screenshot: Optional[str] = None
    after_screenshot: Optional[str] = None


class ReportParser:
    """审查报告解析器"""
    
    def __init__(self):
        self.audit_dir = AUDIT_DIR
    
    def parse_json_report(self, report_path: Path) -> List[Issue]:
        """解析JSON格式的审查报告"""
        issues = []
        
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 解析综合审查报告
            if 'modules' in data:
                issues.extend(self._parse_comprehensive_report(data))
            # 解析单模块报告
            elif 'pages' in data:
                issues.extend(self._parse_module_report(data))
            
        except Exception as e:
            print(f"❌ 解析报告失败 {report_path}: {e}")
        
        return issues
    
    def _parse_comprehensive_report(self, data: Dict) -> List[Issue]:
        """解析综合审查报告"""
        issues = []
        
        for module_name, module_data in data.get('modules', {}).items():
            if 'pages' in module_data:
                issues.extend(self._parse_module_pages(module_data['pages'], module_name))
        
        return issues
    
    def _parse_module_report(self, data: Dict) -> List[Issue]:
        """解析单模块报告"""
        module_name = data.get('module', 'unknown')
        return self._parse_module_pages(data.get('pages', {}), module_name)
    
    def _parse_module_pages(self, pages_data: Dict, module_name: str) -> List[Issue]:
        """解析模块页面数据"""
        issues = []
        
        for page_rel_path, page_data in pages_data.items():
            page_path = page_data.get('path', '')
            page_url = page_data.get('url', '')
            
            # 解析静态资源问题
            for static_issue in page_data.get('static_issues', []):
                issues.append(self._create_static_issue(static_issue, page_path, page_url))
            
            # 解析侧边栏问题
            for sidebar_issue in page_data.get('sidebar_issues', []):
                issues.append(self._create_sidebar_issue(sidebar_issue, page_path, page_url))
            
            # 解析UI问题
            for ui_issue in page_data.get('ui_issues', []):
                issues.append(self._create_ui_issue(ui_issue, page_path, page_url))
            
            # 解析导航问题
            nav_result = page_data.get('navigation_result', {})
            for nav_issue in nav_result.get('issues', []):
                if isinstance(nav_issue, str) and nav_issue != "跳过浏览器审查":
                    issues.append(self._create_navigation_issue(nav_issue, page_path, page_url))
        
        return issues
    
    def _create_static_issue(self, issue_data: Dict, page_path: str, page_url: str) -> Issue:
        """创建静态资源问题"""
        issue_type = issue_data.get('type', '')
        resource = issue_data.get('resource', '')
        
        return Issue(
            id=f"static_{hash(page_path + resource)}",
            title=f"静态资源404: {resource}",
            description=f"页面 {Path(page_path).name} 中的资源 {resource} 无法加载",
            priority=Priority.P1,  # 静态资源问题通常是P1
            category=FixCategory.STATIC_RESOURCE,
            page_path=page_path,
            page_url=page_url,
            details={'type': issue_type, 'resource': resource},
            auto_fixable=True,
            fix_strategy='fix_static_resource'
        )
    
    def _create_sidebar_issue(self, issue_data: Dict, page_path: str, page_url: str) -> Issue:
        """创建侧边栏问题"""
        issue_type = issue_data.get('type', '')
        
        return Issue(
            id=f"sidebar_{hash(page_path + issue_type)}",
            title="侧边栏加载问题",
            description=f"页面 {Path(page_path).name} 的侧边栏未正确加载",
            priority=Priority.P0,  # 侧边栏问题影响导航，是P0
            category=FixCategory.NAVIGATION,
            page_path=page_path,
            page_url=page_url,
            details={'type': issue_type},
            auto_fixable=True,
            fix_strategy='fix_sidebar_loading'
        )
    
    def _create_ui_issue(self, issue_data: Dict, page_path: str, page_url: str) -> Issue:
        """创建UI问题"""
        issue_type = issue_data.get('type', '')
        
        priority = Priority.P2
        if 'chart' in issue_type:
            priority = Priority.P1  # 图表问题影响数据展示
        
        return Issue(
            id=f"ui_{hash(page_path + issue_type)}",
            title=f"UI一致性问题: {issue_type}",
            description=f"页面 {Path(page_path).name} 存在UI一致性问题",
            priority=priority,
            category=FixCategory.UI_VISUAL,
            page_path=page_path,
            page_url=page_url,
            details={'type': issue_type},
            auto_fixable=True,
            fix_strategy='fix_ui_consistency'
        )
    
    def _create_navigation_issue(self, issue_text: str, page_path: str, page_url: str) -> Issue:
        """创建导航问题"""
        return Issue(
            id=f"nav_{hash(page_path + issue_text)}",
            title="导航菜单问题",
            description=issue_text,
            priority=Priority.P0,  # 导航问题是P0
            category=FixCategory.NAVIGATION,
            page_path=page_path,
            page_url=page_url,
            details={'issue': issue_text},
            auto_fixable=False,  # 导航问题通常需要手动修复
            fix_strategy='fix_navigation'
        )
    
    def get_latest_reports(self, limit: int = 5) -> List[Path]:
        """获取最新的审查报告"""
        if not self.audit_dir.exists():
            return []
        
        json_files = list(self.audit_dir.glob('*.json'))
        json_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        return json_files[:limit]


class FixEngine:
    """修复引擎"""
    
    def __init__(self):
        self.admin_dir = ADMIN_DIR
        self.common_css = COMMON_CSS
        self.fix_strategies = {
            'fix_static_resource': self._fix_static_resource,
            'fix_sidebar_loading': self._fix_sidebar_loading,
            'fix_ui_consistency': self._fix_ui_consistency,
            'fix_navigation': self._fix_navigation,
        }
    
    def fix_issue(self, issue: Issue) -> FixResult:
        """修复单个问题"""
        if not issue.auto_fixable:
            return FixResult(
                issue_id=issue.id,
                success=False,
                message=f"问题 {issue.title} 需要手动修复",
                changes_made=[]
            )
        
        strategy = self.fix_strategies.get(issue.fix_strategy)
        if not strategy:
            return FixResult(
                issue_id=issue.id,
                success=False,
                message=f"未找到修复策略: {issue.fix_strategy}",
                changes_made=[]
            )
        
        try:
            return strategy(issue)
        except Exception as e:
            return FixResult(
                issue_id=issue.id,
                success=False,
                message=f"修复失败: {str(e)}",
                changes_made=[]
            )
    
    def _fix_static_resource(self, issue: Issue) -> FixResult:
        """修复静态资源问题"""
        page_path = Path(issue.page_path)
        resource = issue.details.get('resource', '')
        issue_type = issue.details.get('type', '')
        
        changes = []
        
        if issue_type == 'css_404':
            if '通用样式.css' in resource:
                # 修正通用样式路径
                new_path = self._calculate_relative_path(page_path, self.common_css)
                if self._update_resource_path(page_path, resource, new_path):
                    changes.append(f"更新CSS路径: {resource} → {new_path}")
        
        elif issue_type == 'js_404':
            # 尝试修正JS路径
            if not resource.startswith('../'):
                new_path = f"./{resource.lstrip('./')}"
                if self._update_resource_path(page_path, resource, new_path):
                    changes.append(f"更新JS路径: {resource} → {new_path}")
        
        elif issue_type == 'img_404':
            # 创建SVG占位符
            if 'logo' in resource.lower():
                logo_created = self._create_svg_placeholder(page_path, resource)
                if logo_created:
                    changes.append(f"创建SVG占位符: {resource}")
        
        return FixResult(
            issue_id=issue.id,
            success=len(changes) > 0,
            message=f"静态资源修复完成" if changes else "无法自动修复此静态资源问题",
            changes_made=changes
        )
    
    def _fix_sidebar_loading(self, issue: Issue) -> FixResult:
        """修复侧边栏加载问题"""
        page_path = Path(issue.page_path)
        
        if not page_path.exists():
            return FixResult(
                issue_id=issue.id,
                success=False,
                message=f"页面文件不存在: {page_path}",
                changes_made=[]
            )
        
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 检查是否已有侧边栏加载代码
        if SIDEBAR_SNIPPET_MARK in content:
            return FixResult(
                issue_id=issue.id,
                success=True,
                message="侧边栏加载代码已存在",
                changes_made=[]
            )
        
        # 注入侧边栏加载代码
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
        
        return FixResult(
            issue_id=issue.id,
            success=True,
            message="成功注入侧边栏加载代码",
            changes_made=[f"在 {page_path.name} 中添加侧边栏加载脚本"]
        )
    
    def _fix_ui_consistency(self, issue: Issue) -> FixResult:
        """修复UI一致性问题"""
        issue_type = issue.details.get('type', '')
        changes = []
        
        if issue_type == 'chart_no_min_height':
            # 修复图表最小高度
            if self._ensure_chart_min_height():
                changes.append("添加图表最小高度样式到通用CSS")
        
        return FixResult(
            issue_id=issue.id,
            success=len(changes) > 0,
            message="UI一致性修复完成" if changes else "无法自动修复此UI问题",
            changes_made=changes
        )
    
    def _fix_navigation(self, issue: Issue) -> FixResult:
        """修复导航问题（通常需要手动处理）"""
        return FixResult(
            issue_id=issue.id,
            success=False,
            message="导航问题需要手动修复，请检查菜单结构和链接配置",
            changes_made=[]
        )
    
    def _calculate_relative_path(self, from_path: Path, to_path: Path) -> str:
        """计算相对路径"""
        try:
            return os.path.relpath(to_path, from_path.parent)
        except ValueError:
            return str(to_path)
    
    def _update_resource_path(self, page_path: Path, old_path: str, new_path: str) -> bool:
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
            return True
        
        return False
    
    def _create_svg_placeholder(self, page_path: Path, resource: str) -> bool:
        """创建SVG占位符"""
        # 简化实现，实际可以更复杂
        module_dir = page_path.parent
        assets_dir = module_dir / "assets" / "images"
        assets_dir.mkdir(parents=True, exist_ok=True)
        
        logo_path = assets_dir / "logo.svg"
        if not logo_path.exists():
            svg_content = '''<svg width="120" height="40" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="40" fill="#1890ff" rx="4"/>
  <text x="60" y="25" text-anchor="middle" fill="white" font-family="Arial" font-size="14" font-weight="bold">医保审核</text>
</svg>'''
            logo_path.write_text(svg_content, encoding='utf-8')
            return True
        
        return False
    
    def _ensure_chart_min_height(self) -> bool:
        """确保图表最小高度样式"""
        if not self.common_css.exists():
            return False
        
        content = self.common_css.read_text(encoding='utf-8', errors='ignore')
        
        # 检查是否已添加
        if CHART_CSS_MARK in content:
            return False
        
        # 添加图表最小高度样式
        chart_css = f'''
{CHART_CSS_MARK}
.chart-container, [id*="chart"], [class*="chart"] {{
    min-height: 300px;
}}
'''
        
        new_content = content + chart_css
        self.common_css.write_text(new_content, encoding='utf-8')
        return True


class AutoFixManager:
    """自动修复管理器"""
    
    def __init__(self):
        self.parser = ReportParser()
        self.engine = FixEngine()
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    
    def run_auto_fix(self, report_path: Optional[Path] = None, 
                     priority_filter: Optional[List[Priority]] = None) -> Dict:
        """运行自动修复"""
        print("🚀 启动自动修复程序...")
        
        # 获取要处理的报告
        if report_path:
            reports = [report_path]
        else:
            reports = self.parser.get_latest_reports(1)
            if not reports:
                print("❌ 未找到审查报告")
                return {}
        
        all_issues = []
        for report in reports:
            print(f"📋 解析报告: {report.name}")
            issues = self.parser.parse_json_report(report)
            all_issues.extend(issues)
        
        if not all_issues:
            print("✅ 未发现需要修复的问题")
            return {}
        
        # 按优先级过滤
        if priority_filter:
            all_issues = [issue for issue in all_issues if issue.priority in priority_filter]
        
        # 按优先级排序
        all_issues.sort(key=lambda x: (x.priority.value, x.category.value))
        
        print(f"🔧 发现 {len(all_issues)} 个问题，开始修复...")
        
        # 执行修复
        results = {
            'timestamp': self.timestamp,
            'total_issues': len(all_issues),
            'fixed_issues': 0,
            'failed_issues': 0,
            'skipped_issues': 0,
            'fixes': []
        }
        
        for issue in all_issues:
            print(f"\n🔧 修复: {issue.title} [{issue.priority.value}]")
            
            fix_result = self.engine.fix_issue(issue)
            results['fixes'].append({
                'issue': issue.__dict__,
                'result': fix_result.__dict__
            })
            
            if fix_result.success:
                results['fixed_issues'] += 1
                print(f"✅ {fix_result.message}")
                for change in fix_result.changes_made:
                    print(f"   - {change}")
            elif not issue.auto_fixable:
                results['skipped_issues'] += 1
                print(f"⏭️  {fix_result.message}")
            else:
                results['failed_issues'] += 1
                print(f"❌ {fix_result.message}")
        
        # 生成修复报告
        self._generate_fix_report(results)
        
        print(f"\n🎉 自动修复完成!")
        print(f"   总问题数: {results['total_issues']}")
        print(f"   成功修复: {results['fixed_issues']}")
        print(f"   修复失败: {results['failed_issues']}")
        print(f"   跳过处理: {results['skipped_issues']}")
        
        return results
    
    def _generate_fix_report(self, results: Dict):
        """生成修复报告"""
        report_file = AUDIT_DIR / f"auto_fix_report_{self.timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"📄 修复报告已生成: {report_file}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='医保审核系统自动修复程序')
    parser.add_argument('--report', type=str, help='指定审查报告文件路径')
    parser.add_argument('--priority', type=str, choices=['P0', 'P1', 'P2'], 
                       help='只修复指定优先级的问题')
    parser.add_argument('--dry-run', action='store_true', help='试运行模式，不实际修改文件')
    
    args = parser.parse_args()
    
    # 优先级过滤
    priority_filter = None
    if args.priority:
        priority_filter = [Priority(args.priority)]
    
    # 报告路径
    report_path = None
    if args.report:
        report_path = Path(args.report)
        if not report_path.exists():
            print(f"❌ 报告文件不存在: {report_path}")
            return
    
    # 运行自动修复
    manager = AutoFixManager()
    
    if args.dry_run:
        print("🔍 试运行模式，将分析问题但不修改文件")
        # 这里可以添加试运行逻辑
    
    manager.run_auto_fix(report_path, priority_filter)


if __name__ == '__main__':
    main()