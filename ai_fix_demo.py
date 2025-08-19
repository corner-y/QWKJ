#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI智能修复演示脚本

展示新的AI修复流程：
1. 审查 → 2. 出报告 → 3. 根据报告内容逐条调用AI能力进行修复

作者: AI Assistant
创建时间: 2025-01-16
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ai_audit_fix_controller import AIAuditFixController
from ai_intelligent_fix_engine import AIIntelligentFixEngine
from unified_audit_system import UnifiedAuditSystem

class AIFixDemo:
    """AI修复演示类"""
    
    def __init__(self, project_root=None):
        if project_root is None:
            project_root = str(Path(__file__).parent)
        self.project_root = project_root
        self.audit_system = UnifiedAuditSystem(project_root)
        self.fix_engine = AIIntelligentFixEngine(project_root)
        self.controller = AIAuditFixController(project_root)
        
    def run_demo(self, target_pages=None):
        """运行AI修复演示
        
        Args:
            target_pages: 目标页面列表，如果为None则使用默认演示页面
        """
        print("\n" + "="*80)
        print("🤖 AI智能修复系统演示")
        print("="*80)
        
        # 如果没有指定页面，使用一些有代表性的页面进行演示
        if target_pages is None:
            target_pages = [
                "pages/workbench/_dashboard.html",
                "pages/rule-management/_rule-list.html",
                "pages/system-management/_system-monitor.html"
            ]
        
        print(f"\n📋 演示页面: {', '.join(target_pages)}")
        
        # 步骤1: 执行审查
        print("\n🔍 步骤1: 执行页面审查...")
        audit_results = self._run_audit(target_pages)
        
        if not audit_results:
            print("❌ 审查失败，演示终止")
            return
            
        # 步骤2: 分析审查报告
        print("\n📊 步骤2: 分析审查报告...")
        issues = self._analyze_audit_results(audit_results)
        
        if not issues:
            print("✅ 未发现需要修复的问题")
            return
            
        # 步骤3: AI智能修复
        print("\n🛠️ 步骤3: AI智能修复...")
        fix_results = self._run_ai_fixes(issues)
        
        # 步骤4: 验证修复效果
        print("\n✅ 步骤4: 验证修复效果...")
        self._verify_fixes(target_pages, fix_results)
        
        # 生成演示报告
        self._generate_demo_report(target_pages, audit_results, issues, fix_results)
        
        print("\n🎉 AI修复演示完成！")
        
    def _run_audit(self, target_pages):
        """执行审查"""
        audit_results = {}
        
        for page in target_pages:
            print(f"  📄 审查页面: {page}")
            try:
                # 使用统一审查系统进行审查
                page_path = Path(self.project_root) / page
                result = self.audit_system.audit_single_page(page_path)
                audit_results[page] = result
                
                # 显示审查结果摘要
                if result and hasattr(result, 'issues'):
                    issue_count = len(result.issues)
                    score = result.overall_score
                    print(f"    发现 {issue_count} 个问题，评分: {score}/100")
                else:
                    print("    审查完成，无问题发现")
                    
            except Exception as e:
                print(f"    ❌ 审查失败: {str(e)}")
                audit_results[page] = None
                
        return audit_results
        
    def _analyze_audit_results(self, audit_results):
        """分析审查结果，提取需要修复的问题"""
        all_issues = []
        
        for page, result in audit_results.items():
            if not result or not hasattr(result, 'issues'):
                continue
                
            for issue in result.issues:
                # 只处理P0和P1级别的问题进行演示
                if issue.priority in ['P0', 'P1']:
                    # 将AuditIssue对象转换为字典
                    issue_dict = {
                        'id': issue.id,
                        'title': issue.title,
                        'description': issue.description,
                        'priority': issue.priority,
                        'dimension': issue.dimension,
                        'page_path': page,
                        'fix_strategy': issue.fix_strategy,
                        'status': issue.status
                    }
                    all_issues.append(issue_dict)
                    
        # 按优先级排序
        priority_order = {'P0': 0, 'P1': 1, 'P2': 2}
        all_issues.sort(key=lambda x: priority_order.get(x.get('priority', 'P2'), 2))
        
        print(f"  📋 发现 {len(all_issues)} 个需要修复的问题")
        for issue in all_issues:
            priority = issue.get('priority', 'P2')
            description = issue.get('description', '未知问题')
            page = issue.get('page_path', '未知页面')
            print(f"    [{priority}] {description} - {page}")
            
        return all_issues
        
    def _run_ai_fixes(self, issues):
        """运行AI智能修复"""
        fix_results = []
        
        for i, issue in enumerate(issues, 1):
            print(f"\n  🔧 修复 {i}/{len(issues)}: {issue.get('description', '未知问题')}")
            
            try:
                # 使用AI修复引擎进行修复
                fix_result = self.fix_engine.fix_issue(
                    issue=issue,
                    page_path=issue.get('page_path')
                )
                
                if fix_result and fix_result.get('success'):
                    print(f"    ✅ 修复成功: {fix_result.get('description', '已修复')}")
                    fix_results.append({
                        'issue': issue,
                        'result': fix_result,
                        'status': 'success'
                    })
                else:
                    error_msg = fix_result.get('error', '未知错误') if fix_result else '修复失败'
                    print(f"    ❌ 修复失败: {error_msg}")
                    fix_results.append({
                        'issue': issue,
                        'result': fix_result,
                        'status': 'failed'
                    })
                    
            except Exception as e:
                print(f"    ❌ 修复异常: {str(e)}")
                fix_results.append({
                    'issue': issue,
                    'result': None,
                    'status': 'error',
                    'error': str(e)
                })
                
        return fix_results
        
    def _verify_fixes(self, target_pages, fix_results):
        """验证修复效果"""
        print("\n  🔍 重新审查页面以验证修复效果...")
        
        # 重新审查修复过的页面
        verification_results = self._run_audit(target_pages)
        
        # 统计修复效果
        successful_fixes = sum(1 for result in fix_results if result['status'] == 'success')
        failed_fixes = sum(1 for result in fix_results if result['status'] in ['failed', 'error'])
        
        print(f"\n  📊 修复统计:")
        print(f"    ✅ 成功修复: {successful_fixes} 个问题")
        print(f"    ❌ 修复失败: {failed_fixes} 个问题")
        
        # 显示修复前后的评分对比
        for page in target_pages:
            if page in verification_results and verification_results[page]:
                new_score = verification_results[page].overall_score
                print(f"    📄 {page}: 修复后评分 {new_score}/100")
                
    def _generate_demo_report(self, target_pages, audit_results, issues, fix_results):
        """生成演示报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        report_path = f"audit_reports/AI修复演示报告_{timestamp}.md"
        
        # 确保报告目录存在
        os.makedirs("audit_reports", exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# AI智能修复演示报告\n\n")
            f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"## 演示概览\n\n")
            f.write(f"- **演示页面**: {len(target_pages)} 个\n")
            f.write(f"- **发现问题**: {len(issues)} 个\n")
            f.write(f"- **修复尝试**: {len(fix_results)} 个\n")
            
            successful_fixes = sum(1 for result in fix_results if result['status'] == 'success')
            f.write(f"- **修复成功**: {successful_fixes} 个\n")
            f.write(f"- **修复成功率**: {successful_fixes/len(fix_results)*100:.1f}%\n\n")
            
            f.write(f"## 修复详情\n\n")
            for i, result in enumerate(fix_results, 1):
                issue = result['issue']
                status = result['status']
                
                f.write(f"### {i}. {issue.get('description', '未知问题')}\n\n")
                f.write(f"- **页面**: {issue.get('page_path', '未知页面')}\n")
                f.write(f"- **优先级**: {issue.get('priority', 'P2')}\n")
                f.write(f"- **修复状态**: {'✅ 成功' if status == 'success' else '❌ 失败'}\n")
                
                if result.get('result'):
                    fix_desc = result['result'].get('description', '无描述')
                    f.write(f"- **修复描述**: {fix_desc}\n")
                    
                if result.get('error'):
                    f.write(f"- **错误信息**: {result['error']}\n")
                    
                f.write(f"\n")
                
        print(f"\n📋 演示报告已保存: {report_path}")

def main():
    """主函数"""
    demo = AIFixDemo()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        # 如果提供了页面参数，使用指定页面
        target_pages = sys.argv[1:]
        demo.run_demo(target_pages)
    else:
        # 否则使用默认演示
        demo.run_demo()

if __name__ == "__main__":
    main()