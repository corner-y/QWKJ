#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI审查修复控制器
整合审查、AI智能修复和验证的完整流程控制器
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# 导入现有模块
from unified_audit_system import UnifiedAuditSystem
from ai_intelligent_fix_engine import AIIntelligentFixEngine

class AIAuditFixController:
    """AI审查修复控制器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.audit_system = UnifiedAuditSystem(project_root)
        self.fix_engine = AIIntelligentFixEngine(project_root)
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def run_complete_audit_fix_cycle(self, 
                                   target_modules: Optional[List[str]] = None,
                                   priority_filter: Optional[List[str]] = None,
                                   max_fixes_per_cycle: int = 10) -> Dict[str, Any]:
        """
        运行完整的审查-修复-验证循环
        
        Args:
            target_modules: 目标模块列表，None表示全部模块
            priority_filter: 优先级过滤器，如['P0', 'P1']
            max_fixes_per_cycle: 每个循环最大修复数量
            
        Returns:
            完整的循环结果
        """
        cycle_result = {
            'session_id': self.session_id,
            'start_time': datetime.now().isoformat(),
            'cycles': [],
            'final_summary': {},
            'total_fixes_applied': 0,
            'overall_improvement': {}
        }
        
        print(f"🚀 开始AI审查修复循环 (会话ID: {self.session_id})")
        
        cycle_count = 0
        max_cycles = 5  # 最大循环次数，防止无限循环
        
        while cycle_count < max_cycles:
            cycle_count += 1
            print(f"\n📊 第 {cycle_count} 轮循环开始")
            
            # 1. 执行审查
            print("1️⃣ 执行系统审查...")
            audit_result = self._run_audit(target_modules)
            
            # 2. 分析问题并筛选
            print("2️⃣ 分析问题并筛选...")
            problems_to_fix = self._filter_problems(audit_result, priority_filter, max_fixes_per_cycle)
            
            if not problems_to_fix:
                print("✅ 没有需要修复的问题，循环结束")
                break
            
            print(f"📝 发现 {len(problems_to_fix)} 个需要修复的问题")
            
            # 3. AI智能修复
            print("3️⃣ 执行AI智能修复...")
            fix_results = self._run_ai_fixes(problems_to_fix)
            
            # 4. 验证修复效果
            print("4️⃣ 验证修复效果...")
            validation_results = self._validate_fixes(fix_results)
            
            # 5. 记录本轮结果
            cycle_data = {
                'cycle_number': cycle_count,
                'audit_summary': self._summarize_audit(audit_result),
                'problems_identified': len(problems_to_fix),
                'fixes_attempted': len(fix_results),
                'fixes_successful': len([f for f in validation_results if f.get('validation', {}).get('is_fixed', False)]),
                'fixes_failed': len([f for f in validation_results if not f.get('validation', {}).get('is_fixed', False)]),
                'cycle_improvement': self._calculate_improvement(audit_result, validation_results)
            }
            
            cycle_result['cycles'].append(cycle_data)
            cycle_result['total_fixes_applied'] += cycle_data['fixes_successful']
            
            print(f"📈 本轮修复成功: {cycle_data['fixes_successful']}/{cycle_data['fixes_attempted']}")
            
            # 6. 检查是否需要继续
            if cycle_data['fixes_successful'] == 0:
                print("⚠️ 本轮无成功修复，停止循环")
                break
        
        # 最终审查
        print("\n🏁 执行最终审查...")
        final_audit = self._run_audit(target_modules)
        cycle_result['final_audit'] = self._summarize_audit(final_audit)
        cycle_result['end_time'] = datetime.now().isoformat()
        
        # 生成最终报告
        report_content = self._generate_cycle_report(cycle_result)
        report_path = self.project_root / 'audit_reports' / f'AI修复循环报告_{self.session_id}.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\n📋 完整报告已保存: {report_path}")
        
        return cycle_result
    
    def _run_audit(self, target_modules: Optional[List[str]] = None) -> Dict[str, Any]:
        """执行审查"""
        if target_modules:
            # 模块审查
            results = {}
            for module in target_modules:
                results[module] = self.audit_system.audit_module(module)
            return results
        else:
            # 全量审查
            return self.audit_system.run_comprehensive_audit()
    
    def _filter_problems(self, 
                        audit_result: Dict[str, Any], 
                        priority_filter: Optional[List[str]] = None,
                        max_fixes: int = 10) -> List[Dict[str, Any]]:
        """筛选需要修复的问题"""
        all_problems = []
        
        # 从审查结果中提取问题
        if isinstance(audit_result, dict):
            for module_name, module_result in audit_result.items():
                if isinstance(module_result, dict) and 'pages' in module_result:
                    for page_name, page_result in module_result['pages'].items():
                        if 'issues' in page_result:
                            for issue in page_result['issues']:
                                problem = {
                                    'module': module_name,
                                    'page': page_name,
                                    'file_path': page_result.get('file_path', ''),
                                    'type': issue.get('type', ''),
                                    'description': issue.get('description', ''),
                                    'severity': issue.get('severity', 'P2'),
                                    'status': issue.get('status', '待修复')
                                }
                                all_problems.append(problem)
        
        # 应用优先级过滤
        if priority_filter:
            all_problems = [p for p in all_problems if p['severity'] in priority_filter]
        
        # 按优先级排序
        priority_order = {'P0': 0, 'P1': 1, 'P2': 2}
        all_problems.sort(key=lambda x: priority_order.get(x['severity'], 3))
        
        # 限制数量
        return all_problems[:max_fixes]
    
    def _run_ai_fixes(self, problems: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """执行AI修复"""
        fix_results = []
        
        for i, problem in enumerate(problems, 1):
            print(f"  🔧 修复 {i}/{len(problems)}: {problem['type']} - {problem['file_path']}")
            
            try:
                # 1. 分析问题
                analysis = self.fix_engine.analyze_problem(problem)
                
                # 2. 收集上下文
                context = self.fix_engine.gather_context(problem['file_path'], analysis['context_needed'])
                
                # 3. 生成修复提示
                fix_prompt = self.fix_engine.generate_fix_prompt(analysis, context)
                
                # 4. 这里应该调用AI API进行修复
                # 由于没有实际的AI API，我们使用模拟的修复逻辑
                fixed_content = self._simulate_ai_fix(problem, context, fix_prompt)
                
                if fixed_content:
                    # 5. 应用修复
                    success = self.fix_engine.apply_ai_fix(problem['file_path'], fixed_content)
                    
                    fix_result = {
                        'problem': problem,
                        'analysis': analysis,
                        'fix_prompt': fix_prompt,
                        'status': 'success' if success else 'failed',
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    fix_result = {
                        'problem': problem,
                        'analysis': analysis,
                        'status': 'failed',
                        'error': 'AI修复生成失败',
                        'timestamp': datetime.now().isoformat()
                    }
                
                fix_results.append(fix_result)
                
            except Exception as e:
                print(f"    ❌ 修复失败: {e}")
                fix_results.append({
                    'problem': problem,
                    'status': 'failed',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        return fix_results
    
    def _simulate_ai_fix(self, problem: Dict[str, Any], context: Dict[str, Any], prompt: str) -> Optional[str]:
        """模拟AI修复（实际应用中应该调用真实的AI API）"""
        file_content = context.get('file_content', '')
        
        if not file_content:
            return None
        
        # 根据问题类型进行简单的模拟修复
        if '面包屑导航' in problem['description']:
            return self._add_breadcrumb_simulation(file_content, problem)
        elif '页面标题' in problem['description']:
            return self._add_title_simulation(file_content, problem)
        elif '响应式设计' in problem['description']:
            return self._add_responsive_simulation(file_content, problem)
        elif '无障碍访问' in problem['description']:
            return self._add_accessibility_simulation(file_content, problem)
        
        return None
    
    def _add_breadcrumb_simulation(self, content: str, problem: Dict[str, Any]) -> str:
        """模拟添加面包屑导航"""
        page_name = problem.get('page', '页面')
        module_name = problem.get('module', '模块')
        
        breadcrumb_html = f'''
<!-- AI生成的面包屑导航 -->
<nav aria-label="breadcrumb" class="breadcrumb-nav">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">首页</a></li>
        <li class="breadcrumb-item"><a href="/{module_name.lower()}">{module_name}</a></li>
        <li class="breadcrumb-item active" aria-current="page">{page_name}</li>
    </ol>
</nav>
'''
        
        # 如果是HTML片段（组件），直接在开头添加
        if not content.strip().startswith('<html'):
            return breadcrumb_html + content
        
        # 如果是完整HTML，在body开头添加
        body_match = re.search(r'<body[^>]*>', content, re.IGNORECASE)
        if body_match:
            insert_pos = body_match.end()
            return content[:insert_pos] + breadcrumb_html + content[insert_pos:]
        
        return content
    
    def _add_title_simulation(self, content: str, problem: Dict[str, Any]) -> str:
        """模拟添加页面标题"""
        page_name = problem.get('page', '页面')
        
        title_html = f'<h1 class="page-title">{page_name}</h1>\n'
        
        # 如果是HTML片段，直接在开头添加
        if not content.strip().startswith('<html'):
            return title_html + content
        
        # 如果是完整HTML，在主内容区域添加
        main_match = re.search(r'<main[^>]*>|<div[^>]*class=["\'][^"\']*(main|content)[^"\']* ["\']', content, re.IGNORECASE)
        if main_match:
            insert_pos = main_match.end()
            return content[:insert_pos] + title_html + content[insert_pos:]
        
        return content
    
    def _add_responsive_simulation(self, content: str, problem: Dict[str, Any]) -> str:
        """模拟添加响应式设计"""
        # 如果是HTML片段，跳过viewport添加
        if content.strip().startswith('<html'):
            # 检查是否已有viewport
            if not re.search(r'<meta[^>]*name=["\']viewport["\']', content, re.IGNORECASE):
                viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
                if head_match:
                    insert_pos = head_match.end()
                    content = content[:insert_pos] + viewport_meta + content[insert_pos:]
        
        # 添加响应式类
        if 'class=' in content:
            content = re.sub(r'class="([^"]*)"', r'class="\1 responsive"', content, count=1)
        
        return content
    
    def _add_accessibility_simulation(self, content: str, problem: Dict[str, Any]) -> str:
        """模拟添加无障碍访问特性"""
        # 为按钮添加aria-label
        content = re.sub(r'<button([^>]*)>', r'<button\1 aria-label="操作按钮">', content)
        
        # 为输入框添加aria-describedby
        content = re.sub(r'<input([^>]*)>', r'<input\1 aria-describedby="input-help">', content)
        
        # 为图片添加alt属性
        content = re.sub(r'<img([^>]*?)(?<!alt=["\'][^"\']*)>', r'<img\1 alt="图片描述">', content)
        
        return content
    
    def _validate_fixes(self, fix_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """验证修复效果"""
        validated_results = []
        
        for fix_result in fix_results:
            if fix_result.get('status') == 'success':
                problem = fix_result['problem']
                validation = self.fix_engine.validate_fix(problem['file_path'], problem)
                fix_result['validation'] = validation
            
            validated_results.append(fix_result)
        
        return validated_results
    
    def _summarize_audit(self, audit_result: Dict[str, Any]) -> Dict[str, Any]:
        """总结审查结果"""
        summary = {
            'total_pages': 0,
            'total_issues': 0,
            'issues_by_severity': {'P0': 0, 'P1': 0, 'P2': 0},
            'average_score': 0.0
        }
        
        if isinstance(audit_result, dict):
            scores = []
            for module_result in audit_result.values():
                if isinstance(module_result, dict) and 'pages' in module_result:
                    for page_result in module_result['pages'].values():
                        summary['total_pages'] += 1
                        if 'score' in page_result:
                            scores.append(page_result['score'])
                        if 'issues' in page_result:
                            for issue in page_result['issues']:
                                summary['total_issues'] += 1
                                severity = issue.get('severity', 'P2')
                                if severity in summary['issues_by_severity']:
                                    summary['issues_by_severity'][severity] += 1
            
            if scores:
                summary['average_score'] = sum(scores) / len(scores)
        
        return summary
    
    def _calculate_improvement(self, audit_result: Dict[str, Any], fix_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """计算改进情况"""
        return {
            'fixes_attempted': len(fix_results),
            'fixes_successful': len([f for f in fix_results if f.get('validation', {}).get('is_fixed', False)]),
            'success_rate': len([f for f in fix_results if f.get('validation', {}).get('is_fixed', False)]) / len(fix_results) if fix_results else 0
        }
    
    def _generate_cycle_report(self, cycle_result: Dict[str, Any]) -> str:
        """生成循环报告"""
        report = f"""
# AI审查修复循环报告

**会话ID**: {cycle_result['session_id']}
**开始时间**: {cycle_result['start_time']}
**结束时间**: {cycle_result['end_time']}
**总修复数**: {cycle_result['total_fixes_applied']}

## 循环概览

"""
        
        for cycle in cycle_result['cycles']:
            report += f"""
### 第 {cycle['cycle_number']} 轮循环

- **发现问题**: {cycle['problems_identified']} 个
- **尝试修复**: {cycle['fixes_attempted']} 个
- **修复成功**: {cycle['fixes_successful']} 个
- **修复失败**: {cycle['fixes_failed']} 个
- **成功率**: {cycle['fixes_successful'] / cycle['fixes_attempted'] * 100 if cycle['fixes_attempted'] > 0 else 0:.1f}%

"""
        
        final_audit = cycle_result.get('final_audit', {})
        report += f"""
## 最终审查结果

- **总页面数**: {final_audit.get('total_pages', 0)}
- **剩余问题**: {final_audit.get('total_issues', 0)} 个
- **平均评分**: {final_audit.get('average_score', 0):.1f}/100

### 问题分布

| 严重级别 | 数量 |
|----------|------|
| P0 | {final_audit.get('issues_by_severity', {}).get('P0', 0)} |
| P1 | {final_audit.get('issues_by_severity', {}).get('P1', 0)} |
| P2 | {final_audit.get('issues_by_severity', {}).get('P2', 0)} |

## 总结

本次AI修复循环共执行 {len(cycle_result['cycles'])} 轮，成功修复 {cycle_result['total_fixes_applied']} 个问题。

---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return report

def main():
    """主函数 - 演示AI审查修复控制器"""
    print("🤖 AI审查修复控制器")
    print("整合审查、AI智能修复和验证的完整流程")
    print("\n使用示例:")
    print("controller = AIAuditFixController('/path/to/project')")
    print("result = controller.run_complete_audit_fix_cycle(priority_filter=['P0', 'P1'])")
    
if __name__ == "__main__":
    main()