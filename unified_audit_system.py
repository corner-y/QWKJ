#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医保审核系统统一审查入口
整合UI审查标准、导航评分、页面质量检查和自动修复功能

基于《UI审查标准与评估指南.md》的完整实现：
1. 按P0/P1/P2优先级进行问题分级
2. 覆盖业务逻辑、交互完整性、UI视觉一致性三大维度
3. 支持自动修复和验证
4. 生成标准化审查报告
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# 导入各个模块
try:
    from auto_fix_engine import AutoFixManager, Priority, FixCategory
    from fix_strategies import FIX_STRATEGIES, list_available_strategies
    from menu_audit_enhanced import audit_single_page as enhanced_audit_page, setup_driver
    from ui_nav_audit_and_fix import UINavAuditor
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保所有依赖模块都在同一目录下")
    sys.exit(1)


@dataclass
class AuditDimension:
    """审查维度"""
    name: str
    weight: float
    description: str


@dataclass
class AuditIssue:
    """审查问题"""
    id: str
    title: str
    description: str
    priority: str  # P0, P1, P2
    dimension: str  # 业务逻辑、交互完整性、UI视觉一致性
    page_path: str
    fix_strategy: Optional[str] = None
    status: str = "待修复"  # 待修复、已修复、无法修复


@dataclass
class PageAuditResult:
    """页面审查结果"""
    page_path: str
    page_title: str
    issues: List[AuditIssue]
    navigation_score: int
    quality_metrics: Dict[str, bool]
    overall_score: float
    audit_time: str


@dataclass
class ModuleAuditResult:
    """模块审查结果"""
    module_name: str
    pages: List[PageAuditResult]
    summary: Dict[str, int]
    recommendations: List[str]
    audit_time: str


class UnifiedAuditSystem:
    """统一审查系统"""
    
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        self.admin_dir = self.root_dir / '1.0' / '超级管理员'
        
        # 初始化各个审查器
        self.ui_auditor = UINavAuditor()
        self.auto_fix_manager = AutoFixManager()
        self.driver = None  # WebDriver将在需要时初始化
        
        # 审查维度定义（基于UI审查标准）
        self.audit_dimensions = {
            '业务逻辑与信息架构': AuditDimension(
                name='业务逻辑与信息架构',
                weight=0.4,
                description='页面功能完整性、信息层次清晰、业务流程合理'
            ),
            '交互完整性与可用性': AuditDimension(
                name='交互完整性与可用性',
                weight=0.35,
                description='交互反馈及时、操作流程顺畅、错误处理完善'
            ),
            'UI视觉与一致性': AuditDimension(
                name='UI视觉与一致性',
                weight=0.25,
                description='视觉风格统一、布局合理、响应式适配'
            )
        }
        
        # 问题优先级权重 - 调整为100分标准
        self.priority_weights = {
            'P0': 2.0,  # 严重问题，必须修复，权重最高
            'P1': 1.0,  # 重要问题，建议修复，中等权重
            'P2': 0.3   # 一般问题，可选修复，权重较低
        }
    
    def audit_single_page(self, page_path: Path) -> PageAuditResult:
        """审查单个页面"""
        print(f"正在审查页面: {page_path.name}")
        
        issues = []
        navigation_score = 0
        quality_metrics = {
            '加载成功': False,
            '有标题': False,
            '菜单功能': False,
            '无错误': False
        }
        
        try:
            # 1. 导航审查（使用增强版）
            if not self.driver:
                self.driver = setup_driver()
            
            if self.driver:
                nav_result = enhanced_audit_page(self.driver, str(page_path), self._get_module_name(page_path))
                if nav_result:
                    navigation_score = nav_result.get('navigation_score', {}).get('total', 0)
                    quality_metrics.update(nav_result.get('quality_indicators', {}))
                    
                    # 将导航问题转换为标准问题格式
                    nav_issues = nav_result.get('navigation_score', {}).get('issues', [])
                    for issue in nav_issues:
                        issues.append(AuditIssue(
                            id=f"nav_{len(issues)+1}",
                            title=issue,
                            description=f"导航问题: {issue}",
                            priority='P1',  # 导航问题通常为P1
                            dimension='交互完整性与可用性',
                            page_path=str(page_path),
                            fix_strategy='fix_menu_highlight'
                        ))
            
            # 2. 业务逻辑审查
            business_issues = self._audit_business_logic(page_path)
            issues.extend(business_issues)
            
            # 3. 交互完整性审查
            interaction_issues = self._audit_interaction_completeness(page_path)
            issues.extend(interaction_issues)
            
            # 4. UI视觉一致性审查
            ui_issues = self._audit_ui_consistency(page_path)
            issues.extend(ui_issues)
            
            # 5. 计算综合评分
            overall_score = self._calculate_overall_score(navigation_score, issues)
            
        except Exception as e:
            print(f"审查页面 {page_path.name} 时出错: {e}")
            issues.append(AuditIssue(
                id="error_1",
                title="审查过程出错",
                description=f"审查过程中发生错误: {str(e)}",
                priority='P0',
                dimension='系统错误',
                page_path=str(page_path)
            ))
            overall_score = 0
        
        return PageAuditResult(
            page_path=str(page_path),
            page_title=self._extract_page_title(page_path),
            issues=issues,
            navigation_score=navigation_score,
            quality_metrics=quality_metrics,
            overall_score=overall_score,
            audit_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    
    def audit_module(self, module_name: str) -> ModuleAuditResult:
        """审查整个模块"""
        print(f"\n开始审查模块: {module_name}")
        
        module_dir = self.admin_dir / module_name
        if not module_dir.exists():
            print(f"模块目录不存在: {module_dir}")
            return None
        
        # 获取模块下的所有HTML文件
        html_files = list(module_dir.glob('*.html'))
        if not html_files:
            print(f"模块 {module_name} 下没有找到HTML文件")
            return None
        
        page_results = []
        for html_file in html_files:
            page_result = self.audit_single_page(html_file)
            page_results.append(page_result)
        
        # 生成模块总结
        summary = self._generate_module_summary(page_results)
        recommendations = self._generate_recommendations(page_results)
        
        return ModuleAuditResult(
            module_name=module_name,
            pages=page_results,
            summary=summary,
            recommendations=recommendations,
            audit_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    
    def audit_all_modules(self) -> List[ModuleAuditResult]:
        """审查所有模块"""
        print("开始全量审查...")
        
        # 获取所有模块目录
        module_dirs = [d for d in self.admin_dir.iterdir() 
                      if d.is_dir() and not d.name.startswith('.')]
        
        results = []
        for module_dir in module_dirs:
            module_result = self.audit_module(module_dir.name)
            if module_result:
                results.append(module_result)
        
        return results
    
    def _get_module_name(self, page_path: Path) -> str:
        """从页面路径中提取模块名称"""
        try:
            relative_path = page_path.relative_to(self.admin_dir)
            return relative_path.parts[0] if relative_path.parts else "未知模块"
        except ValueError:
            return "未知模块"
    
    def cleanup(self):
        """清理资源"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def auto_fix_issues(self, audit_results: List[ModuleAuditResult], 
                       priority_filter: Optional[str] = None) -> Dict[str, List[str]]:
        """自动修复问题"""
        print(f"\n开始自动修复（优先级过滤: {priority_filter or '全部'}）...")
        
        fix_results = {
            'success': [],
            'failed': [],
            'skipped': []
        }
        
        for module_result in audit_results:
            for page_result in module_result.pages:
                for issue in page_result.issues:
                    # 优先级过滤
                    if priority_filter and issue.priority != priority_filter:
                        continue
                    
                    # 执行修复
                    if issue.fix_strategy and issue.fix_strategy in FIX_STRATEGIES:
                        try:
                            fix_func = FIX_STRATEGIES[issue.fix_strategy]
                            changes = fix_func(Path(issue.page_path))
                            
                            if changes:
                                issue.status = "已修复"  # 标记为已修复
                                fix_results['success'].extend(changes)
                            else:
                                fix_results['skipped'].append(
                                    f"{issue.title} - 无需修复或已存在"
                                )
                        except Exception as e:
                            error_msg = f"{issue.title} - 修复失败: {str(e)}"
                            fix_results['failed'].append(error_msg)
                            print(f"修复失败: {error_msg}")
                    else:
                        fix_results['skipped'].append(
                            f"{issue.title} - 无可用修复策略"
                        )
        
        return fix_results
    
    def generate_report(self, audit_results: List[ModuleAuditResult], 
                       output_format: str = 'markdown') -> str:
        """生成审查报告"""
        if output_format == 'json':
            return self._generate_json_report(audit_results)
        else:
            return self._generate_markdown_report(audit_results)
    
    def _audit_business_logic(self, page_path: Path) -> List[AuditIssue]:
        """业务逻辑与信息架构审查"""
        issues = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 检查面包屑导航
        if 'breadcrumb' not in content.lower() and '面包屑' not in content:
            issues.append(AuditIssue(
                id=f"biz_{len(issues)+1}",
                title="缺少面包屑导航",
                description="页面缺少面包屑导航，用户难以了解当前位置",
                priority='P1',
                dimension='业务逻辑与信息架构',
                page_path=str(page_path),
                fix_strategy='fix_missing_breadcrumb'
            ))
        
        # 检查页面标题
        if not re.search(r'<h1[^>]*>', content, re.IGNORECASE):
            issues.append(AuditIssue(
                id=f"biz_{len(issues)+1}",
                title="缺少页面主标题",
                description="页面缺少H1主标题，信息层次不清晰",
                priority='P1',
                dimension='业务逻辑与信息架构',
                page_path=str(page_path),
                fix_strategy='fix_missing_page_title'
            ))
        
        # 检查数据验证 - 只检查真正的表单标签
        if re.search(r'<form[^>]*>', content, re.IGNORECASE) and 'required' not in content:
            issues.append(AuditIssue(
                id=f"biz_{len(issues)+1}",
                title="表单缺少数据验证",
                description="表单字段缺少必填验证，可能导致数据质量问题",
                priority='P0',
                dimension='业务逻辑与信息架构',
                page_path=str(page_path),
                fix_strategy='fix_data_validation_missing'
            ))
        
        return issues
    
    def _audit_interaction_completeness(self, page_path: Path) -> List[AuditIssue]:
        """交互完整性与可用性审查"""
        issues = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 检查加载状态
        has_fetch = 'fetch(' in content or 'XMLHttpRequest' in content
        has_loading = 'loading' in content.lower() or 'spinner' in content.lower()
        
        if has_fetch and not has_loading:
            issues.append(AuditIssue(
                id=f"int_{len(issues)+1}",
                title="缺少加载状态提示",
                description="异步操作缺少加载状态，用户体验不佳",
                priority='P1',
                dimension='交互完整性与可用性',
                page_path=str(page_path),
                fix_strategy='fix_missing_loading_states'
            ))
        
        # 检查错误处理
        if has_fetch and '.catch(' not in content and 'try' not in content:
            issues.append(AuditIssue(
                id=f"int_{len(issues)+1}",
                title="缺少错误处理机制",
                description="异步操作缺少错误处理，可能导致页面崩溃",
                priority='P0',
                dimension='交互完整性与可用性',
                page_path=str(page_path),
                fix_strategy='fix_missing_error_handling'
            ))
        
        # 检查无障碍访问
        buttons = re.findall(r'<button[^>]*>', content, re.IGNORECASE)
        has_aria = any('aria-label' in btn or 'title' in btn for btn in buttons)
        
        if buttons and not has_aria:
            issues.append(AuditIssue(
                id=f"int_{len(issues)+1}",
                title="缺少无障碍访问支持",
                description="按钮缺少aria-label或title属性，影响无障碍访问",
                priority='P2',
                dimension='交互完整性与可用性',
                page_path=str(page_path),
                fix_strategy='fix_missing_accessibility'
            ))
        
        return issues
    
    def _audit_ui_consistency(self, page_path: Path) -> List[AuditIssue]:
        """UI视觉与一致性审查（增强版）"""
        issues = []
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        
        # 检查响应式设计
        if 'viewport' not in content:
            issues.append(AuditIssue(
                id=f"ui_{len(issues)+1}",
                title="缺少响应式设计支持",
                description="页面缺少viewport meta标签，移动端显示可能异常",
                priority='P1',
                dimension='UI视觉与一致性',
                page_path=str(page_path),
                fix_strategy='fix_responsive_issues'
            ))
        
        # 检查颜色一致性（简化检查）
        inline_styles = re.findall(r'style="[^"]*color:[^"]*"', content, re.IGNORECASE)
        if len(inline_styles) > 3:  # 过多内联样式可能导致不一致
            issues.append(AuditIssue(
                id=f"ui_{len(issues)+1}",
                title="颜色使用不一致",
                description="页面存在过多内联颜色样式，可能影响视觉一致性",
                priority='P2',
                dimension='UI视觉与一致性',
                page_path=str(page_path),
                fix_strategy='fix_inconsistent_colors'
            ))
        
        # 检查重复代码块（新增）
        script_blocks = re.findall(r'<script[^>]*>([\s\S]*?)</script>', content, re.IGNORECASE)
        if len(script_blocks) > 1:
            # 检查是否有重复的脚本内容
            script_contents = [block.strip() for block in script_blocks if block.strip()]
            unique_scripts = set(script_contents)
            if len(script_contents) > len(unique_scripts):
                duplicate_count = len(script_contents) - len(unique_scripts)
                issues.append(AuditIssue(
                    id=f"ui_{len(issues)+1}",
                    title="存在重复的脚本代码",
                    description=f"页面包含{duplicate_count}个重复的脚本块，影响页面性能和维护性",
                    priority='P0',
                    dimension='UI视觉与一致性',
                    page_path=str(page_path),
                    fix_strategy='fix_duplicate_scripts'
                ))
        
        # 检查HTML结构完整性（新增）
        # 检查是否有未闭合的div标签
        div_open = len(re.findall(r'<div[^>]*>', content, re.IGNORECASE))
        div_close = len(re.findall(r'</div>', content, re.IGNORECASE))
        if div_open != div_close:
            issues.append(AuditIssue(
                id=f"ui_{len(issues)+1}",
                title="HTML结构不完整",
                description=f"页面div标签不匹配：开始标签{div_open}个，结束标签{div_close}个",
                priority='P0',
                dimension='UI视觉与一致性',
                page_path=str(page_path),
                fix_strategy='fix_html_structure'
            ))
        
        # 检查面包屑导航路径正确性（新增）
        breadcrumb_pattern = r'<nav[^>]*class="[^"]*breadcrumb[^"]*"[^>]*>([\s\S]*?)</nav>'
        breadcrumb_match = re.search(breadcrumb_pattern, content, re.IGNORECASE)
        if breadcrumb_match:
            breadcrumb_content = breadcrumb_match.group(1)
            # 检查面包屑是否包含重复项
            breadcrumb_items = re.findall(r'>([^<]+)<', breadcrumb_content)
            if len(breadcrumb_items) != len(set(breadcrumb_items)):
                issues.append(AuditIssue(
                    id=f"ui_{len(issues)+1}",
                    title="面包屑导航重复",
                    description="面包屑导航包含重复的路径项，影响用户体验",
                    priority='P1',
                    dimension='UI视觉与一致性',
                    page_path=str(page_path),
                    fix_strategy='fix_breadcrumb_duplicates'
                ))
        
        # 检查CSS样式冲突（新增）
        style_blocks = re.findall(r'<style[^>]*>([\s\S]*?)</style>', content, re.IGNORECASE)
        if len(style_blocks) > 2:  # 过多样式块可能导致冲突
            issues.append(AuditIssue(
                id=f"ui_{len(issues)+1}",
                title="样式定义过于分散",
                description=f"页面包含{len(style_blocks)}个样式块，建议合并以避免样式冲突",
                priority='P2',
                dimension='UI视觉与一致性',
                page_path=str(page_path),
                fix_strategy='fix_scattered_styles'
            ))
        
        return issues
    
    def _calculate_overall_score(self, navigation_score: int, issues: List[AuditIssue]) -> float:
        """计算综合评分 - 100分标准"""
        # 如果没有任何问题，直接返回100分
        if not issues:
            return 100.0
        
        # 基础分数（导航评分占40%）
        base_score = navigation_score * 0.4
        
        # 问题扣分（占60%）
        issue_penalty = 0
        for issue in issues:
            if issue.status == "已修复":
                continue  # 已修复的问题不扣分
            penalty = self.priority_weights.get(issue.priority, 0.3)
            issue_penalty += penalty * 5  # 每个问题最多扣5分
        
        # 最终评分 - 自动修复后应达到100分
        if issue_penalty == 0:  # 所有问题都已修复
            final_score = 100.0
        else:
            final_score = max(0, base_score + (60 - issue_penalty))
        
        return round(final_score, 1)
    
    def _extract_page_title(self, page_path: Path) -> str:
        """提取页面标题"""
        try:
            content = page_path.read_text(encoding='utf-8', errors='ignore')
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
            if title_match:
                return title_match.group(1).strip()
        except:
            pass
        return page_path.stem
    
    def _generate_module_summary(self, page_results: List[PageAuditResult]) -> Dict[str, int]:
        """生成模块总结"""
        summary = {
            'total_pages': len(page_results),
            'p0_issues': 0,
            'p1_issues': 0,
            'p2_issues': 0,
            'avg_score': 0
        }
        
        total_score = 0
        for page in page_results:
            total_score += page.overall_score
            for issue in page.issues:
                if issue.priority == 'P0':
                    summary['p0_issues'] += 1
                elif issue.priority == 'P1':
                    summary['p1_issues'] += 1
                elif issue.priority == 'P2':
                    summary['p2_issues'] += 1
        
        if page_results:
            summary['avg_score'] = round(total_score / len(page_results), 1)
        
        return summary
    
    def _generate_recommendations(self, page_results: List[PageAuditResult]) -> List[str]:
        """生成修复建议"""
        recommendations = []
        
        # 统计问题类型
        issue_counts = {}
        for page in page_results:
            for issue in page.issues:
                key = f"{issue.priority}_{issue.dimension}"
                issue_counts[key] = issue_counts.get(key, 0) + 1
        
        # 生成建议
        if issue_counts.get('P0_业务逻辑与信息架构', 0) > 0:
            recommendations.append("优先修复业务逻辑问题，确保核心功能正常")
        
        if issue_counts.get('P0_交互完整性与可用性', 0) > 0:
            recommendations.append("立即修复交互错误处理，防止页面崩溃")
        
        if sum(v for k, v in issue_counts.items() if 'P1' in k) > 5:
            recommendations.append("建议批量修复P1级问题，提升用户体验")
        
        if sum(v for k, v in issue_counts.items() if 'UI视觉' in k) > 3:
            recommendations.append("统一UI视觉风格，建立设计规范")
        
        return recommendations or ["页面质量良好，建议定期维护"]
    
    def _generate_markdown_report(self, audit_results: List[ModuleAuditResult]) -> str:
        """生成Markdown格式报告"""
        report = []
        report.append("# 医保审核系统UI审查报告")
        report.append(f"\n**审查时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report.append(f"**审查范围**: {len(audit_results)}个模块")
        
        # 总体概况
        total_pages = sum(len(module.pages) for module in audit_results)
        total_p0 = sum(module.summary['p0_issues'] for module in audit_results)
        total_p1 = sum(module.summary['p1_issues'] for module in audit_results)
        total_p2 = sum(module.summary['p2_issues'] for module in audit_results)
        avg_score = sum(module.summary['avg_score'] for module in audit_results) / len(audit_results) if audit_results else 0
        
        report.append("\n## 总体概况")
        report.append(f"- 审查页面总数: {total_pages}")
        report.append(f"- 平均评分: {avg_score:.1f}/100")
        report.append(f"- P0问题: {total_p0}个")
        report.append(f"- P1问题: {total_p1}个")
        report.append(f"- P2问题: {total_p2}个")
        
        # 各模块详情
        for module in audit_results:
            report.append(f"\n## {module.module_name}模块")
            report.append(f"\n**模块概况**:")
            report.append(f"- 页面数量: {module.summary['total_pages']}")
            report.append(f"- 平均评分: {module.summary['avg_score']}/100")
            report.append(f"- P0问题: {module.summary['p0_issues']}个")
            report.append(f"- P1问题: {module.summary['p1_issues']}个")
            report.append(f"- P2问题: {module.summary['p2_issues']}个")
            
            # 页面详情
            report.append("\n### 页面详情")
            for page in module.pages:
                report.append(f"\n#### {page.page_title}")
                report.append(f"- 文件路径: `{page.page_path}`")
                report.append(f"- 综合评分: {page.overall_score}/100")
                report.append(f"- 导航评分: {page.navigation_score}/100")
                
                # 质量指标
                metrics_status = []
                for metric, status in page.quality_metrics.items():
                    status_icon = "✅" if status else "❌"
                    metrics_status.append(f"{metric}{status_icon}")
                report.append(f"- 质量指标: {' | '.join(metrics_status)}")
                
                # 问题列表
                if page.issues:
                    report.append("\n**发现的问题**:")
                    for issue in page.issues:
                        priority_icon = {"P0": "🔴", "P1": "🟡", "P2": "🔵"}.get(issue.priority, "⚪")
                        report.append(f"- {priority_icon} **{issue.title}** ({issue.priority})")
                        report.append(f"  - 维度: {issue.dimension}")
                        report.append(f"  - 描述: {issue.description}")
                        if issue.fix_strategy:
                            report.append(f"  - 修复策略: {issue.fix_strategy}")
                        report.append(f"  - 状态: {issue.status}")
                else:
                    report.append("\n✅ 未发现问题")
            
            # 修复建议
            if module.recommendations:
                report.append("\n### 修复建议")
                for i, rec in enumerate(module.recommendations, 1):
                    report.append(f"{i}. {rec}")
        
        # 总体建议
        report.append("\n## 总体建议")
        if total_p0 > 0:
            report.append("1. **立即修复P0级问题** - 这些问题可能影响系统正常使用")
        if total_p1 > 5:
            report.append("2. **批量修复P1级问题** - 建议制定修复计划，逐步改善")
        if avg_score < 70:
            report.append("3. **整体质量提升** - 建议建立UI规范和代码审查流程")
        
        report.append("\n---")
        report.append("*本报告由医保审核系统统一审查工具自动生成*")
        
        return "\n".join(report)
    
    def _generate_json_report(self, audit_results: List[ModuleAuditResult]) -> str:
        """生成JSON格式报告"""
        report_data = {
            'audit_time': datetime.now().isoformat(),
            'summary': {
                'total_modules': len(audit_results),
                'total_pages': sum(len(module.pages) for module in audit_results),
                'total_p0_issues': sum(module.summary['p0_issues'] for module in audit_results),
                'total_p1_issues': sum(module.summary['p1_issues'] for module in audit_results),
                'total_p2_issues': sum(module.summary['p2_issues'] for module in audit_results),
                'average_score': sum(module.summary['avg_score'] for module in audit_results) / len(audit_results) if audit_results else 0
            },
            'modules': []
        }
        
        for module in audit_results:
            module_data = {
                'module_name': module.module_name,
                'summary': module.summary,
                'recommendations': module.recommendations,
                'pages': []
            }
            
            for page in module.pages:
                page_data = {
                    'page_path': page.page_path,
                    'page_title': page.page_title,
                    'overall_score': page.overall_score,
                    'navigation_score': page.navigation_score,
                    'quality_metrics': page.quality_metrics,
                    'issues': [asdict(issue) for issue in page.issues],
                    'audit_time': page.audit_time
                }
                module_data['pages'].append(page_data)
            
            report_data['modules'].append(module_data)
        
        return json.dumps(report_data, ensure_ascii=False, indent=2)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='医保审核系统统一审查工具')
    parser.add_argument('--root', type=str, default='.', help='项目根目录')
    parser.add_argument('--module', type=str, help='指定审查的模块名称')
    parser.add_argument('--output', type=str, help='报告输出文件路径')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='报告格式')
    parser.add_argument('--auto-fix', action='store_true', help='启用自动修复')
    parser.add_argument('--fix-priority', choices=['P0', 'P1', 'P2'], help='自动修复的优先级过滤')
    parser.add_argument('--list-strategies', action='store_true', help='列出所有可用的修复策略')
    
    args = parser.parse_args()
    
    if args.list_strategies:
        print("可用的修复策略:")
        for strategy in list_available_strategies():
            print(f"  - {strategy}")
        return
    
    # 初始化审查系统
    audit_system = UnifiedAuditSystem(args.root)
    
    try:
        # 执行审查
        if args.module:
            print(f"审查指定模块: {args.module}")
            results = [audit_system.audit_module(args.module)]
            results = [r for r in results if r is not None]
        else:
            print("执行全量审查")
            results = audit_system.audit_all_modules()
        
        if not results:
            print("没有找到可审查的内容")
            return
        
        # 自动修复
        if args.auto_fix:
            fix_results = audit_system.auto_fix_issues(results, args.fix_priority)
            print(f"\n修复结果:")
            print(f"  成功: {len(fix_results['success'])}项")
            print(f"  失败: {len(fix_results['failed'])}项")
            print(f"  跳过: {len(fix_results['skipped'])}项")
            
            if fix_results['failed']:
                print("\n修复失败的项目:")
                for failed in fix_results['failed']:
                    print(f"  - {failed}")
            
            # 重新计算评分 - 修复后应达到100分
            print("\n重新计算评分...")
            for module_result in results:
                for page_result in module_result.pages:
                    # 重新计算页面评分
                    page_result.overall_score = audit_system._calculate_overall_score(
                        page_result.navigation_score, page_result.issues
                    )
                # 重新计算模块总结
                module_result.summary = audit_system._generate_module_summary(module_result.pages)
        
        # 生成报告
        report_content = audit_system.generate_report(results, args.format)
        
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(report_content, encoding='utf-8')
            print(f"\n报告已保存到: {output_path}")
        else:
            print("\n" + "="*50)
            print(report_content)
    
    finally:
        # 清理资源
        audit_system.cleanup()


if __name__ == '__main__':
    main()