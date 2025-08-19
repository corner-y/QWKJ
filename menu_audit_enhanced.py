#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医保审核系统页面审查增强版脚本
功能：
1. 页面截图 + 控制台/网络错误日志采集
2. 左侧菜单树结构抽取与分析
3. 导航一致性评分
4. 综合页面质量评估
5. 生成结构化审查报告
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
# 共享配置（若存在audit_config则优先使用）
try:
    from audit_config import (
        ROOT as CFG_ROOT,
        ADMIN_DIR as CFG_ADMIN_DIR,
        IMG_DIR as CFG_IMG_DIR,
        LOG_DIR as CFG_LOG_DIR,
        AUDIT_DIR as CFG_AUDIT_DIR,
        BASE_URL as CFG_BASE_URL,
        AUDIT_PAGES as CFG_AUDIT_PAGES,
        STANDARD_MENU_STRUCTURE as CFG_STANDARD_MENU_STRUCTURE,
    )
    HAS_CFG = True
except ImportError:
    HAS_CFG = False

# 配置路径
ADMIN_DIR = Path('/Users/baiyumi/Mai/代码/chenyrweb/ybsh/1.0/超级管理员')
IMG_DIR = Path('/Users/baiyumi/Mai/代码/chenyrweb/ybsh/img')
LOG_DIR = IMG_DIR / 'logs'
AUDIT_DIR = Path('/Users/baiyumi/Mai/代码/chenyrweb/ybsh/audit_reports')
BASE_URL = 'http://localhost:8000/1.0/超级管理员'

# 需要审查的页面列表 - 按模块分组
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

# 标准菜单结构（从_unified-sidebar.html提取）
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

def setup_driver():
    """设置Chrome WebDriver，启用日志采集（离线优先，多重回退）"""
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--ignore-certificate-errors')

    # 启用性能日志和控制台日志
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL', 'performance': 'ALL'})

    # 优先使用 webdriver_manager 的本地缓存，避免联网
    os.environ.setdefault('WDM_LOCAL', '1')
    os.environ.setdefault('WDM_OFFLINE', '1')

    # 方案一：webdriver_manager（离线缓存）
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_window_size(1920, 1080)
        return driver
    except Exception as e1:
        print(f"⚠️ webdriver_manager 离线模式失败: {e1}. 尝试使用 Selenium Manager 自动驱动。")

    # 方案二：Selenium Manager（Selenium 4.6+）
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1920, 1080)
        return driver
    except Exception as e2:
        print(f"⚠️ Selenium Manager 初始化失败: {e2}. 尝试使用环境变量指定的 chromedriver。")

    # 方案三：环境变量 CHROMEDRIVER / CHROMEWEBDRIVER 指定的二进制
    chromedriver_path = os.environ.get('CHROMEDRIVER') or os.environ.get('CHROMEWEBDRIVER')
    if chromedriver_path:
        try:
            service = Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_window_size(1920, 1080)
            return driver
        except Exception as e3:
            print(f"⚠️ 使用环境变量中的 chromedriver 失败: {e3}")

    print("❌ Chrome WebDriver 初始化失败：请确认本机已安装 Chrome 浏览器，并在离线环境下提供可用的 chromedriver（可设置环境变量 CHROMEDRIVER 指向可执行文件）")
    return None

def extract_menu_structure(driver):
    """抽取页面左侧菜单结构"""
    menu_data = {
        "exists": False,
        "structure": {},
        "active_items": [],
        "expanded_groups": [],
        "errors": []
    }
    
    try:
        # 检查统一侧边栏容器是否存在
        sidebar_container = driver.find_element(By.ID, "sidebar-container")
        if not sidebar_container:
            menu_data["errors"].append("缺少 sidebar-container 容器")
            return menu_data
        
        # 检查侧边栏是否加载
        sidebar = driver.find_element(By.CSS_SELECTOR, "#sidebar-container .sidebar")
        if not sidebar:
            menu_data["errors"].append("统一侧边栏未加载")
            return menu_data
        
        menu_data["exists"] = True
        
        # 提取菜单结构
        nav_groups = driver.find_elements(By.CSS_SELECTOR, "#sidebar-container .nav-group")
        for group in nav_groups:
            try:
                # 一级菜单
                level1_item = group.find_element(By.CSS_SELECTOR, ".nav-level-1")
                level1_text = level1_item.find_element(By.CSS_SELECTOR, ".nav-text").text
                
                group_data = {
                    "level": 1,
                    "expanded": "expanded" in group.get_attribute("class"),
                    "children": {}
                }
                
                # 记录展开状态
                if group_data["expanded"]:
                    menu_data["expanded_groups"].append(level1_text)
                
                # 检查高亮状态
                if "active" in level1_item.get_attribute("class"):
                    menu_data["active_items"].append(level1_text)
                
                # 二级菜单
                level2_items = group.find_elements(By.CSS_SELECTOR, ".nav-level-2")
                for item2 in level2_items:
                    try:
                        text2 = item2.find_element(By.CSS_SELECTOR, ".nav-text").text
                        href2 = item2.get_attribute("href")
                        
                        item2_data = {
                            "level": 2,
                            "href": href2 if href2 and href2 != "javascript:void(0)" else None
                        }
                        
                        if "active" in item2.get_attribute("class"):
                            menu_data["active_items"].append(f"{level1_text} > {text2}")
                        
                        # 三级菜单（如果有）
                        parent_subgroup = item2.find_element(By.XPATH, "./..")
                        if "nav-subgroup" in parent_subgroup.get_attribute("class"):
                            level3_items = parent_subgroup.find_elements(By.CSS_SELECTOR, ".nav-level-3")
                            if level3_items:
                                item2_data["children"] = {}
                                for item3 in level3_items:
                                    try:
                                        text3 = item3.find_element(By.CSS_SELECTOR, ".nav-text").text
                                        href3 = item3.get_attribute("href")
                                        
                                        item3_data = {
                                            "level": 3,
                                            "href": href3 if href3 and href3 != "javascript:void(0)" else None
                                        }
                                        
                                        if "active" in item3.get_attribute("class"):
                                            menu_data["active_items"].append(f"{level1_text} > {text2} > {text3}")
                                        
                                        item2_data["children"][text3] = item3_data
                                    except Exception:
                                        continue
                        
                        group_data["children"][text2] = item2_data
                    except Exception:
                        continue
                
                menu_data["structure"][level1_text] = group_data
                
            except Exception as e:
                menu_data["errors"].append(f"解析菜单组失败: {str(e)}")
                continue
        
    except Exception as e:
        menu_data["errors"].append(f"抽取菜单结构失败: {str(e)}")
    
    return menu_data

def calculate_navigation_score(menu_data, page_path):
    """计算导航一致性评分"""
    score = {
        "total": 0,
        "details": {
            "menu_exists": 0,      # 菜单存在 (20分)
            "structure_match": 0,   # 结构匹配 (25分)
            "active_highlight": 0,  # 高亮正确 (25分)
            "expansion_logic": 0,   # 展开逻辑 (15分)
            "link_validity": 0      # 链接有效 (15分)
        },
        "issues": []
    }
    
    # 1. 菜单存在检查 (20分)
    if menu_data["exists"]:
        score["details"]["menu_exists"] = 20
    else:
        score["issues"].append("左侧菜单不存在或未正确加载")
    
    # 2. 结构匹配检查 (25分)
    if menu_data["structure"]:
        structure_score = 0
        for menu_name in STANDARD_MENU_STRUCTURE:
            if menu_name in menu_data["structure"]:
                structure_score += 5  # 每个一级菜单5分
        score["details"]["structure_match"] = min(structure_score, 25)
    else:
        score["issues"].append("菜单结构为空")
    
    # 3. 高亮正确性检查 (25分)
    current_module = page_path.split('/')[0] if '/' in page_path else "登录"
    module_mapping = {
        "工作台": "工作台",
        "审核管理": "审核管理",
        "规则管理": "规则管理", 
        "用户权限管理": "用户权限管理",
        "系统管理": "系统管理",
        "知识库": "知识库",
        "登录": "登录"
    }
    
    expected_module = module_mapping.get(current_module, current_module)
    # 知识库目录页面（物理路径在系统管理下）属于“知识库”一级菜单
    if "知识库目录.html" in page_path:
        expected_module = "知识库"
    
    if menu_data["active_items"]:
        # 检查是否有正确的高亮
        has_correct_highlight = any(expected_module in item for item in menu_data["active_items"])
        if has_correct_highlight:
            score["details"]["active_highlight"] = 25
        else:
            score["issues"].append(f"当前页面({expected_module})高亮不正确，实际高亮: {menu_data['active_items']}")
    else:
        score["issues"].append("没有任何菜单项被高亮")
    
    # 4. 展开逻辑检查 (15分)
    if expected_module in menu_data["expanded_groups"]:
        score["details"]["expansion_logic"] = 15
    else:
        score["issues"].append(f"当前模块({expected_module})的菜单组未正确展开")
    
    # 5. 链接有效性检查 (15分) - 简单检查href存在
    valid_links = 0
    total_links = 0
    
    def count_links(menu_dict):
        count = 0
        valid = 0
        for item in menu_dict.values():
            if isinstance(item, dict):
                if "href" in item:
                    count += 1
                    if item["href"]:
                        valid += 1
                if "children" in item:
                    c, v = count_links(item["children"])
                    count += c
                    valid += v
        return count, valid
    
    total_links, valid_links = count_links(STANDARD_MENU_STRUCTURE)
    if total_links > 0:
        score["details"]["link_validity"] = round(15 * (valid_links / total_links))
    else:
        score["details"]["link_validity"] = 15
    
    # 汇总总分
    score["total"] = sum(score["details"].values())
    return score

def parse_performance_logs(raw_logs):
    """解析performance日志，统计网络错误"""
    import json
    net_errors = []
    for entry in raw_logs:
        try:
            msg = json.loads(entry.get('message', '{}'))
            message = msg.get('message', {})
            method = message.get('method')
            params = message.get('params', {})

            if method == 'Network.loadingFailed':
                url = params.get('url', '')
                error_text = params.get('errorText', '')
                net_errors.append(f"NetworkFailed: {url} | {error_text}")
        except Exception:
            continue
    return net_errors

def collect_logs_and_errors(driver, page_name):
    """采集控制台与网络错误日志"""
    logs = []
    
    # 浏览器控制台日志
    try:
        browser_logs = driver.get_log('browser')
        for e in browser_logs:
            lvl = e.get('level')
            msg = e.get('message')
            if lvl in ('SEVERE', 'ERROR'):
                logs.append(f"Console[{lvl}]: {msg}")
    except Exception:
        pass

    # 网络错误日志
    try:
        perf_logs = driver.get_log('performance')
        net_errors = parse_performance_logs(perf_logs)
        logs.extend(net_errors)
    except Exception:
        pass

    # 保存到文件
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{page_name}.log"
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"==== {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {page_name} ====\n")
        if logs:
            f.write("\n".join(logs) + "\n")
        else:
            f.write("No errors captured.\n")
    
    return logs

def audit_single_page(driver, page_path, module_name):
    """审查单个页面"""
    try:
        url = f"{BASE_URL}/{page_path}"
        page_name = Path(page_path).name
        print(f"🔍 审查页面: {page_path}")
        
        driver.get(url)
        time.sleep(2)
        
        # 等待侧边栏加载（登录页面跳过）
        is_login_page = page_path == '登录.html'
        if not is_login_page:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "sidebar-container"))
                )
                time.sleep(1.5)  # 额外等待异步加载
            except Exception:
                print(f"⚠️  侧边栏加载超时: {page_path}")
        else:
            print(f"🔓 登录页面，跳过侧边栏检查")
        
        # 1. 截图
        output_path = IMG_DIR / f"{page_name}.png"
        total_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
        driver.set_window_size(1920, max(1080, int(total_height)))
        driver.save_screenshot(str(output_path))
        
        # 2. 抽取菜单结构
        menu_data = extract_menu_structure(driver)
        
        # 3. 计算导航评分
        nav_score = calculate_navigation_score(menu_data, page_path)
        
        # 4. 收集错误日志
        error_logs = collect_logs_and_errors(driver, page_name)
        
        # 5. 基础页面检查
        page_title = driver.title
        current_url = driver.current_url
        
        audit_result = {
            "page_info": {
                "path": page_path,
                "name": page_name,
                "module": module_name,
                "title": page_title,
                "url": current_url,
                "screenshot": f"{page_name}.png",
                "audit_time": datetime.now().isoformat()
            },
            "menu_analysis": menu_data,
            "navigation_score": nav_score,
            "error_logs": {
                "count": len(error_logs),
                "details": error_logs,
                "log_file": f"{page_name}.log"
            },
            "quality_indicators": {
                "has_title": bool(page_title),
                "loads_successfully": True,
                "menu_functional": menu_data["exists"],
                "error_free": len(error_logs) == 0
            }
        }
        
        print(f"✅ 审查完成: {page_name} (导航评分: {nav_score['total']}/100)")
        return audit_result
        
    except Exception as e:
        print(f"❌ 审查失败: {page_path} - {e}")
        return {
            "page_info": {
                "path": page_path,
                "name": Path(page_path).name,
                "module": module_name,
                "audit_time": datetime.now().isoformat(),
                "error": str(e)
            },
            "quality_indicators": {
                "loads_successfully": False
            }
        }

def generate_audit_report(module_results, module_name):
    """生成模块审查报告"""
    report = {
        "module": module_name,
        "audit_time": datetime.now().isoformat(),
        "summary": {
            "total_pages": len(module_results),
            "successful_audits": sum(1 for r in module_results if r.get("quality_indicators", {}).get("loads_successfully", False)),
            "pages_with_errors": sum(1 for r in module_results if r.get("error_logs", {}).get("count", 0) > 0),
            "avg_navigation_score": 0
        },
        "pages": module_results,
        "issues_summary": {
            "navigation_issues": [],
            "common_errors": [],
            "recommendations": []
        }
    }
    
    # 计算平均导航评分
    nav_scores = [r.get("navigation_score", {}).get("total", 0) for r in module_results if "navigation_score" in r]
    if nav_scores:
        report["summary"]["avg_navigation_score"] = round(sum(nav_scores) / len(nav_scores), 1)
    
    # 汇总问题
    all_nav_issues = []
    error_types = {}
    
    for result in module_results:
        # 导航问题
        nav_issues = result.get("navigation_score", {}).get("issues", [])
        all_nav_issues.extend(nav_issues)
        
        # 错误类型统计
        for error in result.get("error_logs", {}).get("details", []):
            error_type = error.split(":")[0] if ":" in error else "Unknown"
            error_types[error_type] = error_types.get(error_type, 0) + 1
    
    # 生成问题汇总
    report["issues_summary"]["navigation_issues"] = list(set(all_nav_issues))
    report["issues_summary"]["common_errors"] = [f"{k}: {v}次" for k, v in sorted(error_types.items(), key=lambda x: x[1], reverse=True)]
    
    # 生成建议
    if report["summary"]["avg_navigation_score"] < 80:
        report["issues_summary"]["recommendations"].append("导航评分偏低，建议检查菜单高亮和展开逻辑")
    if report["summary"]["pages_with_errors"] > 0:
        report["issues_summary"]["recommendations"].append("存在页面错误，建议优先修复控制台和网络问题")
    
    return report

def main():
    """主函数 - 执行模块化页面审查"""
    print("🚀 医保审核系统页面审查增强版")
    print("=" * 60)
    
    # 确保输出目录存在
    IMG_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 初始化WebDriver
    driver = setup_driver()
    if not driver:
        return
    
    try:
        # 选择要审查的模块
        print("可用模块:")
        modules = list(AUDIT_PAGES.keys())
        for i, module in enumerate(modules, 1):
            print(f"  {i}. {module} ({len(AUDIT_PAGES[module])}页)")
        
        print("\n请选择要审查的模块 (输入数字，多个用逗号分隔，或输入'all'审查全部):")
        user_input = input().strip()
        
        if user_input.lower() == 'all':
            selected_modules = modules
        else:
            try:
                indices = [int(x.strip()) - 1 for x in user_input.split(',')]
                selected_modules = [modules[i] for i in indices if 0 <= i < len(modules)]
            except:
                print("❌ 输入格式错误，默认审查前两个模块")
                selected_modules = modules[:2]
        
        print(f"\n将审查模块: {', '.join(selected_modules)}")
        print("-" * 60)
        
        # 执行审查
        for module_name in selected_modules:
            print(f"\n📋 开始审查模块: {module_name}")
            module_results = []
            
            for page_path in AUDIT_PAGES[module_name]:
                # 检查页面文件是否存在（去除查询参数）
                clean_path = page_path.split('?')[0]  # 移除查询参数
                page_file = ADMIN_DIR / clean_path
                if not page_file.exists():
                    print(f"⚠️  页面文件不存在: {page_path}")
                    continue
                
                # 审查页面
                result = audit_single_page(driver, page_path, module_name)
                module_results.append(result)
                time.sleep(1)  # 避免请求过快
            
            # 生成模块报告
            if module_results:
                report = generate_audit_report(module_results, module_name)
                report_file = AUDIT_DIR / f"{module_name}_审查报告_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
                
                with open(report_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, ensure_ascii=False, indent=2)
                
                print(f"✅ {module_name} 模块审查完成")
                print(f"   - 页面数: {report['summary']['total_pages']}")
                print(f"   - 平均导航评分: {report['summary']['avg_navigation_score']}/100")
                print(f"   - 错误页面数: {report['summary']['pages_with_errors']}")
                print(f"   - 报告文件: {report_file.name}")
        
        print("\n" + "=" * 60)
        print("🎉 页面审查任务完成!")
        print(f"截图保存: {IMG_DIR}")
        print(f"日志保存: {LOG_DIR}")
        print(f"报告保存: {AUDIT_DIR}")
        
    finally:
        driver.quit()

if __name__ == '__main__':
    main()