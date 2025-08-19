#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI智能修复引擎
基于AI能力的智能代码修复系统，根据审查报告逐条进行针对性修复
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class AIIntelligentFixEngine:
    """AI智能修复引擎"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.fix_history = []
        self.context_cache = {}
        
    def analyze_problem(self, problem_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析问题详情，提取关键信息
        
        Args:
            problem_info: 问题信息字典，包含类型、描述、文件路径等
            
        Returns:
            分析结果字典
        """
        analysis = {
            'problem_type': problem_info.get('type', ''),
            'description': problem_info.get('description', ''),
            'file_path': problem_info.get('file_path', ''),
            'severity': problem_info.get('severity', 'P2'),
            'context_needed': [],
            'fix_strategy': '',
            'estimated_complexity': 'medium'
        }
        
        # 根据问题类型确定所需上下文
        if '面包屑导航' in analysis['description']:
            analysis['context_needed'] = ['navigation_structure', 'page_hierarchy']
            analysis['fix_strategy'] = 'add_breadcrumb_navigation'
            analysis['estimated_complexity'] = 'low'
            
        elif '页面标题' in analysis['description']:
            analysis['context_needed'] = ['page_content', 'existing_titles']
            analysis['fix_strategy'] = 'add_page_title'
            analysis['estimated_complexity'] = 'low'
            
        elif '响应式设计' in analysis['description']:
            analysis['context_needed'] = ['css_structure', 'viewport_meta']
            analysis['fix_strategy'] = 'enhance_responsive_design'
            analysis['estimated_complexity'] = 'medium'
            
        elif '无障碍访问' in analysis['description']:
            analysis['context_needed'] = ['html_structure', 'form_elements', 'interactive_elements']
            analysis['fix_strategy'] = 'improve_accessibility'
            analysis['estimated_complexity'] = 'high'
            
        elif '表单验证' in analysis['description']:
            analysis['context_needed'] = ['form_structure', 'validation_logic']
            analysis['fix_strategy'] = 'add_form_validation'
            analysis['estimated_complexity'] = 'medium'
            
        elif '错误处理' in analysis['description']:
            analysis['context_needed'] = ['error_scenarios', 'user_feedback']
            analysis['fix_strategy'] = 'enhance_error_handling'
            analysis['estimated_complexity'] = 'high'
            
        return analysis
    
    def gather_context(self, file_path: str, context_types: List[str]) -> Dict[str, Any]:
        """
        收集修复所需的上下文信息
        
        Args:
            file_path: 目标文件路径
            context_types: 需要的上下文类型列表
            
        Returns:
            上下文信息字典
        """
        context = {
            'file_content': '',
            'file_type': '',
            'related_files': [],
            'dependencies': [],
            'current_structure': {}
        }
        
        # 读取文件内容
        full_path = self.project_root / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    context['file_content'] = f.read()
                context['file_type'] = full_path.suffix
            except Exception as e:
                print(f"读取文件失败: {e}")
                return context
        
        # 根据上下文类型收集特定信息
        for ctx_type in context_types:
            if ctx_type == 'navigation_structure':
                context['navigation_info'] = self._extract_navigation_info(context['file_content'])
                
            elif ctx_type == 'page_hierarchy':
                context['hierarchy_info'] = self._extract_page_hierarchy(file_path)
                
            elif ctx_type == 'css_structure':
                context['css_info'] = self._extract_css_info(context['file_content'])
                
            elif ctx_type == 'html_structure':
                context['html_structure'] = self._extract_html_structure(context['file_content'])
                
            elif ctx_type == 'form_structure':
                context['form_info'] = self._extract_form_structure(context['file_content'])
        
        return context
    
    def _extract_navigation_info(self, content: str) -> Dict[str, Any]:
        """提取导航信息"""
        nav_info = {
            'has_breadcrumb': False,
            'nav_elements': [],
            'menu_structure': []
        }
        
        # 检查是否已有面包屑
        breadcrumb_patterns = [
            r'class=["\'].*breadcrumb.*["\']',
            r'<nav[^>]*aria-label=["\']breadcrumb["\']',
            r'<ol[^>]*class=["\'].*breadcrumb.*["\']'
        ]
        
        for pattern in breadcrumb_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                nav_info['has_breadcrumb'] = True
                break
        
        # 提取现有导航元素
        nav_matches = re.findall(r'<nav[^>]*>(.*?)</nav>', content, re.DOTALL | re.IGNORECASE)
        nav_info['nav_elements'] = nav_matches
        
        return nav_info
    
    def _extract_page_hierarchy(self, file_path: str) -> Dict[str, Any]:
        """提取页面层级信息"""
        hierarchy = {
            'level': 0,
            'parent_pages': [],
            'page_name': '',
            'module': ''
        }
        
        # 从文件路径推断层级
        path_parts = Path(file_path).parts
        hierarchy['level'] = len(path_parts) - 1
        hierarchy['page_name'] = Path(file_path).stem
        
        # 推断模块
        if len(path_parts) > 1:
            hierarchy['module'] = path_parts[-2]
        
        # 构建父级页面路径
        for i in range(len(path_parts) - 1):
            parent_path = '/'.join(path_parts[:i+1])
            hierarchy['parent_pages'].append(parent_path)
        
        return hierarchy
    
    def _extract_css_info(self, content: str) -> Dict[str, Any]:
        """提取CSS信息"""
        css_info = {
            'has_viewport_meta': False,
            'responsive_classes': [],
            'media_queries': []
        }
        
        # 检查viewport meta标签
        if re.search(r'<meta[^>]*name=["\']viewport["\']', content, re.IGNORECASE):
            css_info['has_viewport_meta'] = True
        
        # 提取响应式类名
        responsive_patterns = [
            r'class=["\'][^"\']*(responsive|mobile|tablet|desktop)[^"\']* ["\']',
            r'class=["\'][^"\']*(col-|row-|grid-)[^"\']* ["\']'
        ]
        
        for pattern in responsive_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            css_info['responsive_classes'].extend(matches)
        
        return css_info
    
    def _extract_html_structure(self, content: str) -> Dict[str, Any]:
        """提取HTML结构信息"""
        structure = {
            'has_main_content': False,
            'headings': [],
            'interactive_elements': [],
            'accessibility_features': []
        }
        
        # 检查主内容区域
        if re.search(r'<main[^>]*>|<div[^>]*class=["\'][^"\']*(main|content)[^"\']* ["\']', content, re.IGNORECASE):
            structure['has_main_content'] = True
        
        # 提取标题
        heading_matches = re.findall(r'<(h[1-6])[^>]*>(.*?)</\1>', content, re.IGNORECASE)
        structure['headings'] = [(tag, text.strip()) for tag, text in heading_matches]
        
        # 提取交互元素
        interactive_patterns = [
            r'<button[^>]*>',
            r'<input[^>]*>',
            r'<select[^>]*>',
            r'<a[^>]*href'
        ]
        
        for pattern in interactive_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            structure['interactive_elements'].extend(matches)
        
        # 检查无障碍特性
        accessibility_patterns = [
            r'aria-label=["\'][^"\']* ["\']',
            r'aria-describedby=["\'][^"\']* ["\']',
            r'role=["\'][^"\']* ["\']',
            r'alt=["\'][^"\']* ["\']'
        ]
        
        for pattern in accessibility_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            structure['accessibility_features'].extend(matches)
        
        return structure
    
    def _extract_form_structure(self, content: str) -> Dict[str, Any]:
        """提取表单结构信息"""
        form_info = {
            'forms': [],
            'inputs': [],
            'validation_present': False
        }
        
        # 提取表单
        form_matches = re.findall(r'<form[^>]*>(.*?)</form>', content, re.DOTALL | re.IGNORECASE)
        form_info['forms'] = form_matches
        
        # 提取输入字段
        input_matches = re.findall(r'<input[^>]*>', content, re.IGNORECASE)
        form_info['inputs'] = input_matches
        
        # 检查验证
        validation_patterns = [
            r'required[\s>]',
            r'pattern=["\']',
            r'minlength=["\']',
            r'maxlength=["\']'
        ]
        
        for pattern in validation_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                form_info['validation_present'] = True
                break
        
        return form_info
    
    def generate_fix_prompt(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        生成AI修复提示词
        
        Args:
            analysis: 问题分析结果
            context: 上下文信息
            
        Returns:
            AI修复提示词
        """
        prompt = f"""
你是一个专业的前端代码修复专家。请根据以下信息修复代码问题：

## 问题描述
- 问题类型：{analysis['problem_type']}
- 具体描述：{analysis['description']}
- 严重级别：{analysis['severity']}
- 文件路径：{analysis['file_path']}

## 当前代码内容
```{context.get('file_type', 'html')}
{context['file_content']}
```

## 上下文信息
"""
        
        # 添加特定上下文信息
        if 'navigation_info' in context:
            nav_info = context['navigation_info']
            prompt += f"""
### 导航信息
- 已有面包屑：{nav_info['has_breadcrumb']}
- 导航元素数量：{len(nav_info['nav_elements'])}
"""
        
        if 'hierarchy_info' in context:
            hier_info = context['hierarchy_info']
            prompt += f"""
### 页面层级
- 页面层级：{hier_info['level']}
- 页面名称：{hier_info['page_name']}
- 所属模块：{hier_info['module']}
- 父级页面：{' > '.join(hier_info['parent_pages'])}
"""
        
        if 'html_structure' in context:
            html_info = context['html_structure']
            prompt += f"""
### HTML结构
- 主内容区域：{html_info['has_main_content']}
- 标题数量：{len(html_info['headings'])}
- 交互元素数量：{len(html_info['interactive_elements'])}
- 无障碍特性数量：{len(html_info['accessibility_features'])}
"""
        
        prompt += f"""

## 修复要求
1. 请提供完整的修复后代码
2. 确保修复符合Web标准和最佳实践
3. 保持代码风格与现有代码一致
4. 添加必要的注释说明修复内容
5. 确保修复不会破坏现有功能

## 修复策略
根据问题类型 "{analysis['fix_strategy']}"，请采用相应的修复方案。

请直接提供修复后的完整代码，不需要额外解释。
"""
        
        return prompt
    
    def apply_ai_fix(self, file_path: str, fixed_content: str) -> bool:
        """
        应用AI修复结果
        
        Args:
            file_path: 文件路径
            fixed_content: 修复后的内容
            
        Returns:
            是否修复成功
        """
        try:
            full_path = self.project_root / file_path
            
            # 备份原文件
            backup_path = full_path.with_suffix(f"{full_path.suffix}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            if full_path.exists():
                full_path.rename(backup_path)
            
            # 写入修复后的内容
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            # 记录修复历史
            self.fix_history.append({
                'file_path': file_path,
                'timestamp': datetime.now().isoformat(),
                'backup_path': str(backup_path),
                'status': 'success'
            })
            
            return True
            
        except Exception as e:
            print(f"应用修复失败: {e}")
            self.fix_history.append({
                'file_path': file_path,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'status': 'failed'
            })
            return False
    
    def fix_issue(self, issue: Dict[str, Any], page_path: str = None) -> Dict[str, Any]:
        """
        修复单个问题（兼容演示脚本的接口）
        
        Args:
            issue: 问题信息字典
            page_path: 页面路径（可选）
            
        Returns:
            修复结果字典
        """
        try:
            # 转换问题格式
            problem_info = {
                'type': issue.get('description', ''),
                'description': issue.get('description', ''),
                'file_path': page_path or issue.get('page_path', ''),
                'severity': issue.get('priority', 'P2'),
                'fix_strategy': issue.get('fix_strategy', '')
            }
            
            # 分析问题
            analysis = self.analyze_problem(problem_info)
            
            # 收集上下文
            context = self.gather_context(problem_info['file_path'], analysis['context_needed'])
            
            # 生成修复提示
            fix_prompt = self.generate_fix_prompt(analysis, context)
            
            # 模拟AI修复（实际应用中这里会调用AI API）
            fixed_content = self._simulate_fix_for_demo(problem_info, context)
            
            if fixed_content:
                # 应用修复
                success = self.apply_ai_fix(problem_info['file_path'], fixed_content)
                
                if success:
                    # 验证修复
                    validation = self.validate_fix(problem_info['file_path'], problem_info)
                    
                    return {
                        'success': True,
                        'description': f"已修复: {problem_info['description']}",
                        'changes_made': [f"更新文件: {problem_info['file_path']}"],
                        'validation': validation
                    }
                else:
                    return {
                        'success': False,
                        'error': '应用修复失败',
                        'description': problem_info['description']
                    }
            else:
                return {
                    'success': False,
                    'error': '无法生成修复内容',
                    'description': problem_info['description']
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'修复过程出错: {str(e)}',
                'description': issue.get('description', '未知问题')
            }
    
    def _simulate_fix_for_demo(self, problem_info: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        为演示目的模拟修复内容生成
        
        Args:
            problem_info: 问题信息
            context: 上下文信息
            
        Returns:
            模拟的修复后内容
        """
        try:
            file_path = self.project_root / problem_info['file_path']
            if not file_path.exists():
                return None
                
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # 根据问题类型进行简单的模拟修复
            description = problem_info.get('description', '')
            
            if '面包屑导航' in description:
                # 添加面包屑导航
                breadcrumb_html = '''<nav class="breadcrumb">
    <ol>
        <li><a href="/">首页</a></li>
        <li><a href="#">当前模块</a></li>
        <li class="active">当前页面</li>
    </ol>
</nav>\n'''
                
                # 在主内容区域开头插入面包屑
                if '<main' in original_content:
                    return original_content.replace('<main', breadcrumb_html + '<main')
                elif '<div class="content"' in original_content:
                    return original_content.replace('<div class="content"', breadcrumb_html + '<div class="content"')
                else:
                    return breadcrumb_html + original_content
                    
            elif '页面标题' in description:
                # 添加页面标题
                title = file_path.stem.replace('_', ' ').title()
                title_html = f'<h1>{title}</h1>\n'
                
                # 在主内容区域开头插入标题
                if '<main' in original_content:
                    return original_content.replace('<main', title_html + '<main')
                else:
                    return title_html + original_content
                    
            elif '响应式设计' in description:
                # 添加viewport meta标签
                viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                
                if '<head>' in original_content:
                    return original_content.replace('<head>', '<head>\n' + viewport_meta)
                else:
                    return viewport_meta + original_content
            
            # 如果没有特定的修复逻辑，返回原内容（表示无法修复）
            return None
            
        except Exception as e:
            print(f"模拟修复失败: {e}")
            return None

    def validate_fix(self, file_path: str, original_problem: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证修复效果
        
        Args:
            file_path: 文件路径
            original_problem: 原始问题信息
            
        Returns:
            验证结果
        """
        validation_result = {
            'is_fixed': False,
            'confidence': 0.0,
            'remaining_issues': [],
            'new_issues': [],
            'recommendations': []
        }
        
        try:
            # 重新读取修复后的文件
            full_path = self.project_root / file_path
            if not full_path.exists():
                validation_result['remaining_issues'].append('文件不存在')
                return validation_result
            
            with open(full_path, 'r', encoding='utf-8') as f:
                fixed_content = f.read()
            
            # 根据问题类型进行验证
            problem_type = original_problem.get('type', '')
            
            if '面包屑导航' in problem_type:
                validation_result = self._validate_breadcrumb_fix(fixed_content, validation_result)
                
            elif '页面标题' in problem_type:
                validation_result = self._validate_title_fix(fixed_content, validation_result)
                
            elif '响应式设计' in problem_type:
                validation_result = self._validate_responsive_fix(fixed_content, validation_result)
                
            elif '无障碍访问' in problem_type:
                validation_result = self._validate_accessibility_fix(fixed_content, validation_result)
            
            # 通用验证
            validation_result = self._validate_general_quality(fixed_content, validation_result)
            
        except Exception as e:
            validation_result['remaining_issues'].append(f'验证过程出错: {e}')
        
        return validation_result
    
    def _validate_breadcrumb_fix(self, content: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """验证面包屑导航修复"""
        breadcrumb_patterns = [
            r'class=["\'].*breadcrumb.*["\']',
            r'<nav[^>]*aria-label=["\']breadcrumb["\']',
            r'<ol[^>]*class=["\'].*breadcrumb.*["\']'
        ]
        
        has_breadcrumb = any(re.search(pattern, content, re.IGNORECASE) for pattern in breadcrumb_patterns)
        
        if has_breadcrumb:
            result['is_fixed'] = True
            result['confidence'] = 0.9
        else:
            result['remaining_issues'].append('未检测到面包屑导航')
        
        return result
    
    def _validate_title_fix(self, content: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """验证页面标题修复"""
        title_patterns = [
            r'<h1[^>]*>.*?</h1>',
            r'<title[^>]*>.*?</title>'
        ]
        
        has_title = any(re.search(pattern, content, re.IGNORECASE | re.DOTALL) for pattern in title_patterns)
        
        if has_title:
            result['is_fixed'] = True
            result['confidence'] = 0.9
        else:
            result['remaining_issues'].append('未检测到页面标题')
        
        return result
    
    def _validate_responsive_fix(self, content: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """验证响应式设计修复"""
        responsive_indicators = [
            r'<meta[^>]*name=["\']viewport["\']',
            r'class=["\'][^"\']*(responsive|mobile|col-)[^"\']* ["\']',
            r'@media[^{]*{'
        ]
        
        responsive_score = sum(1 for pattern in responsive_indicators 
                             if re.search(pattern, content, re.IGNORECASE))
        
        if responsive_score >= 1:
            result['is_fixed'] = True
            result['confidence'] = min(0.9, responsive_score * 0.3)
        else:
            result['remaining_issues'].append('未检测到响应式设计特性')
        
        return result
    
    def _validate_accessibility_fix(self, content: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """验证无障碍访问修复"""
        accessibility_patterns = [
            r'aria-label=["\'][^"\']* ["\']',
            r'aria-describedby=["\'][^"\']* ["\']',
            r'role=["\'][^"\']* ["\']',
            r'alt=["\'][^"\']* ["\']',
            r'tabindex=["\'][^"\']* ["\']'
        ]
        
        accessibility_score = sum(1 for pattern in accessibility_patterns 
                                if re.search(pattern, content, re.IGNORECASE))
        
        if accessibility_score >= 2:
            result['is_fixed'] = True
            result['confidence'] = min(0.9, accessibility_score * 0.2)
        else:
            result['remaining_issues'].append('无障碍访问特性不足')
        
        return result
    
    def _validate_general_quality(self, content: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """通用质量验证"""
        # 检查语法错误
        if content.count('<') != content.count('>'):
            result['new_issues'].append('HTML标签不匹配')
        
        # 检查基本结构
        if not re.search(r'<html[^>]*>', content, re.IGNORECASE) and len(content) > 100:
            result['recommendations'].append('考虑添加完整的HTML文档结构')
        
        return result
    
    def generate_fix_report(self, fixes: List[Dict[str, Any]]) -> str:
        """
        生成修复报告
        
        Args:
            fixes: 修复结果列表
            
        Returns:
            修复报告内容
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        
        report = f"""
# AI智能修复报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**修复引擎**: AI智能修复引擎 v1.0

## 修复概览

- **总修复项目**: {len(fixes)}
- **成功修复**: {len([f for f in fixes if f.get('status') == 'success'])}
- **修复失败**: {len([f for f in fixes if f.get('status') == 'failed'])}
- **验证通过**: {len([f for f in fixes if f.get('validation', {}).get('is_fixed', False)])}

## 详细修复记录

"""
        
        for i, fix in enumerate(fixes, 1):
            status_icon = "✅" if fix.get('status') == 'success' else "❌"
            validation = fix.get('validation', {})
            confidence = validation.get('confidence', 0) * 100
            
            report += f"""
### {i}. {fix.get('file_path', 'Unknown')}

{status_icon} **修复状态**: {fix.get('status', 'unknown')}
📊 **验证置信度**: {confidence:.1f}%
🎯 **问题类型**: {fix.get('problem_type', 'Unknown')}
📝 **问题描述**: {fix.get('description', 'No description')}

"""
            
            if validation.get('remaining_issues'):
                report += "**剩余问题**:\n"
                for issue in validation['remaining_issues']:
                    report += f"- {issue}\n"
                report += "\n"
            
            if validation.get('recommendations'):
                report += "**建议**:\n"
                for rec in validation['recommendations']:
                    report += f"- {rec}\n"
                report += "\n"
        
        report += f"""
## 修复统计

| 指标 | 数量 | 百分比 |
|------|------|--------|
| 总修复项目 | {len(fixes)} | 100% |
| 成功修复 | {len([f for f in fixes if f.get('status') == 'success'])} | {len([f for f in fixes if f.get('status') == 'success']) / len(fixes) * 100:.1f}% |
| 验证通过 | {len([f for f in fixes if f.get('validation', {}).get('is_fixed', False)])} | {len([f for f in fixes if f.get('validation', {}).get('is_fixed', False)]) / len(fixes) * 100:.1f}% |

## 建议后续行动

1. 对验证失败的项目进行人工检查
2. 运行完整的审查流程验证修复效果
3. 考虑对高频问题类型优化AI修复策略

---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return report

def main():
    """主函数 - 演示AI智能修复引擎"""
    print("AI智能修复引擎初始化完成")
    print("该引擎将根据审查报告逐条进行AI驱动的智能修复")
    print("\n核心特性:")
    print("1. 问题智能分析与上下文理解")
    print("2. AI驱动的代码生成与修复")
    print("3. 自动验证与质量评估")
    print("4. 详细的修复报告生成")
    
if __name__ == "__main__":
    main()