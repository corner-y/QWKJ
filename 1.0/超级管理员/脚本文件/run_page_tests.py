#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import urllib.parse
import time
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 以测试页所在目录为基准，确保相对路径一致
BASE_URL = 'http://localhost:8000/1.0/%E8%B6%85%E7%BA%A7%E7%AE%A1%E7%90%86%E5%91%98/%E8%84%9A%E6%9C%AC%E6%96%87%E4%BB%B6/'

page_configs = {
    'dashboard': [
        { 'title': '工作台', 'path': '../工作台/工作台.html', 'menu': 'dashboard' },
        { 'title': '平台运营看板', 'path': '../工作台/平台运营看板.html', 'menu': 'dashboard-overview' },
        { 'title': '报告规则分析', 'path': '../工作台/报告规则分析.html', 'menu': 'dashboard-analysis' },
    ],
    'rules': [
        { 'title': '规则管理主页', 'path': '../规则管理/规则列表/规则管理主页.html', 'menu': 'rules-main' },
        { 'title': '门诊规则管理', 'path': '../规则管理/规则列表/门诊规则管理.html', 'menu': 'rules-outpatient' },
        { 'title': '医保规则管理系统', 'path': '../规则管理/规则列表/医保规则管理系统v2.html', 'menu': 'rules-medical' },
        { 'title': '规则详情', 'path': '../规则管理/规则详情/规则详情.html', 'menu': 'rules-detail-general' },
        { 'title': '临床规则详情', 'path': '../规则管理/规则详情/临床规则详情.html', 'menu': 'rules-detail-clinical' },
        { 'title': '慢病规则详情', 'path': '../规则管理/规则详情/慢病规则详情.html', 'menu': 'rules-detail-chronic' },
        { 'title': '政策规则详情', 'path': '../规则管理/规则详情/政策规则详情.html', 'menu': 'rules-detail-policy' },
        { 'title': '门诊规则详情', 'path': '../规则管理/规则详情/门诊规则详情.html', 'menu': 'rules-detail-outpatient' },
        { 'title': '创建规则', 'path': '../规则管理/规则操作/创建规则.html', 'menu': 'rules-create' },
        { 'title': '编辑规则', 'path': '../规则管理/规则操作/编辑规则.html', 'menu': 'rules-edit' },
        { 'title': '规则参数配置', 'path': '../规则管理/规则操作/规则参数配置.html', 'menu': 'rules-config' },
        { 'title': '规则管理完整版', 'path': '../规则管理/规则操作/规则管理完整版.html', 'menu': 'rules-full' },
    ],
    'audit': [
        { 'title': '事前审核记录', 'path': '../审核管理/审核流程/事前审核记录.html', 'menu': 'audit-pre' },
        { 'title': '事中审核检查', 'path': '../审核管理/审核流程/事中审核检查.html', 'menu': 'audit-during' },
        { 'title': '事后审核任务列表', 'path': '../审核管理/审核流程/事后审核任务列表.html', 'menu': 'audit-post' },
        { 'title': '审核结果', 'path': '../审核管理/审核结果/审核结果.html', 'menu': 'audit-results' },
    ],
    'user': [
        { 'title': '用户列表', 'path': '../用户权限管理/用户管理/用户列表.html', 'menu': 'user-list' },
        { 'title': '权限管理', 'path': '../用户权限管理/权限管理/权限管理.html', 'menu': 'permission' },
        { 'title': '科室管理', 'path': '../用户权限管理/组织管理/科室管理.html', 'menu': 'department' },
        { 'title': '租户管理', 'path': '../用户权限管理/组织管理/租户管理.html', 'menu': 'tenant' },
        { 'title': '租户表单', 'path': '../用户权限管理/组织管理/租户表单.html', 'menu': 'tenant-form' },
        { 'title': '企业详情', 'path': '../用户权限管理/组织管理/企业详情.html', 'menu': 'enterprise' },
    ],
    'system': [
        { 'title': '全局设置', 'path': '../系统管理/全局设置.html', 'menu': 'global-settings' },
        { 'title': '系统监控', 'path': '../系统管理/系统监控.html', 'menu': 'system-monitor' },
        { 'title': '知识库目录', 'path': '../系统管理/知识库目录.html', 'menu': 'knowledge-base' },
    ],
}

def make_url(rel_path: str) -> str:
    # 将相对路径与基址合并，并对路径做URL编码，追加时间戳参数避免缓存
    joined = urllib.parse.urljoin(BASE_URL, rel_path)
    parts = urllib.parse.urlsplit(joined)
    # 先反解码避免双重编码，再编码
    decoded_path = urllib.parse.unquote(parts.path)
    quoted_path = urllib.parse.quote(decoded_path)
    # 追加或合并查询参数
    qs = urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
    qs.append(('t', str(int(time.time()))))
    new_query = urllib.parse.urlencode(qs)
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, quoted_path, new_query, parts.fragment))


def http_head(url: str, timeout: int = 10):
    req = urllib.request.Request(url, method='HEAD')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        # 若不支持HEAD或返回错误，尝试GET以获取状态码
        if e.code in (405, 501):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, method='GET'), timeout=timeout) as resp:
                    return resp.status
            except Exception:
                return e.code
        return e.code
    except Exception:
        # 兜底再尝试一次GET
        try:
            with urllib.request.urlopen(urllib.request.Request(url, method='GET'), timeout=timeout) as resp:
                return resp.status
        except Exception:
            return None


def http_get_text(url: str, timeout: int = 15):
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or 'utf-8'
            return resp.read().decode(charset, errors='ignore')
    except Exception:
        return None


def test_page(rel_path: str):
    url = make_url(rel_path)
    status = http_head(url)
    result = {
        'url': url,
        'status': status,
        'issues': [],
        'ok': False,
    }
    if status in (200, 304):
        html = http_get_text(url)
        if html is None:
            result['issues'].append('无法获取页面内容')
        else:
            if 'sidebar-container' not in html:
                result['issues'].append('缺少统一菜单容器')
            if 'unified-sidebar.css' not in html:
                result['issues'].append('缺少统一菜单样式')
            if '_unified-sidebar.html' not in html:
                result['issues'].append('缺少菜单加载脚本')
        result['ok'] = len(result['issues']) == 0
    else:
        result['issues'].append('页面无法访问')
    return result


def main():
    all_pages = []
    for category, pages in page_configs.items():
        for p in pages:
            all_pages.append((category, p))

    detailed = []
    counts = {'success': 0, 'warning': 0, 'error': 0}

    for category, page in all_pages:
        r = test_page(page['path'])
        status = 'success' if r['ok'] else ('error' if r['status'] not in (200, 304) else 'warning')
        counts[status] += 1
        detailed.append({
            'category': category,
            'title': page['title'],
            'menu': page['menu'],
            'path': page['path'],
            'final_status': status,
            'http_status': r['status'],
            'issues': r['issues'],
            'url': r['url'],
        })
        print(f"[{status.upper()}] {page['title']} ({page['path']}) -> {r['status']} | issues: {', '.join(r['issues']) if r['issues'] else 'none'}")
        time.sleep(0.2)  # 轻微节流，避免请求过快

    # 生成Markdown报告
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    report_path = os.path.abspath(os.path.join(BASE_DIR, '..', '..', '..', '测试明细报告.md'))
    timestamped_report_path = os.path.abspath(os.path.join(BASE_DIR, '..', '..', '..', f'测试明细报告_{timestamp}.md'))
    lines = []
    lines.append('# 页面全面测试明细报告')
    lines.append('')
    lines.append(f"- 测试时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append('## 汇总')
    lines.append(f"- 成功：{counts['success']} | 警告：{counts['warning']} | 失败：{counts['error']}\n")
    lines.append('## 明细')
    for item in detailed:
        lines.append(f"- [{item['final_status'].upper()}] {item['title']} | 路径：{item['path']} | HTTP：{item['http_status']} | 问题：{('、'.join(item['issues']) if item['issues'] else '无')} ")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    # 写入时间戳版报告
    with open(timestamped_report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    # 同时输出JSON，方便机器读取
    json_path = os.path.abspath(os.path.join(BASE_DIR, 'page_test_results.json'))
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({'summary': counts, 'details': detailed}, f, ensure_ascii=False, indent=2)

    print('\n报告已生成:')
    print(report_path)
    print(json_path)

if __name__ == '__main__':
    main()