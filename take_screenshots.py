#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量截取超级管理员目录下所有页面的截图
使用Selenium WebDriver自动化截图
增强：采集控制台/网络错误日志
"""

import os
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

# 配置路径
ADMIN_DIR = Path('/Users/baiyumi/Mai/代码/chenyrweb/ybsh/1.0/超级管理员')
IMG_DIR = Path('/Users/baiyumi/Mai/代码/chenyrweb/ybsh/img')
LOG_DIR = IMG_DIR / 'logs'
BASE_URL = 'http://localhost:8000/1.0/超级管理员'

# 需要截图的页面列表（根据之前的修复列表）
TARGET_PAGES = [
    # 工作台模块
    '工作台/工作台.html',
    '工作台/平台运营看板.html', 
    '工作台/报告规则分析.html',
    
    # 用户权限管理模块
    '用户权限管理/用户管理/用户列表.html',
    '用户权限管理/权限管理/权限管理.html',
    '用户权限管理/组织管理/科室管理.html',
    '用户权限管理/组织管理/企业详情.html',
    '用户权限管理/组织管理/租户管理.html',
    '用户权限管理/组织管理/租户表单.html',
    
    # 审核管理模块
    '审核管理/审核流程/事中审核检查.html',
    '审核管理/审核流程/事前审核记录.html',
    '审核管理/审核流程/事后审核任务列表.html',
    '审核管理/审核结果/审核结果.html',
    
    # 规则管理模块
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
    
    # 系统管理模块
    '系统管理/知识库目录.html',
    '系统管理/全局设置.html',
    '系统管理/系统监控.html',
    
    # 登录页
    '登录.html'
]

def setup_driver():
    """设置Chrome WebDriver，启用日志采集"""
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')  # 新版 headless 更稳定
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--ignore-certificate-errors')

    # 启用性能日志（含网络）和控制台日志（Selenium 4语法）
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL', 'performance': 'ALL'})

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_window_size(1920, 1080)
        return driver
    except Exception as e:
        print(f"❌ Chrome WebDriver 初始化失败: {e}")
        print("请确保已安装 Chrome 浏览器，或手动安装匹配版本的 ChromeDriver")
        return None


def parse_performance_logs(raw_logs):
    """解析performance日志，统计网络错误与JS异常"""
    import json
    net_errors = []
    for entry in raw_logs:
        try:
            msg = json.loads(entry.get('message', '{}'))
            message = msg.get('message', {})
            method = message.get('method')
            params = message.get('params', {})

            # 请求失败
            if method == 'Network.loadingFailed':
                url = params.get('url', '')
                error_text = params.get('errorText', '')
                net_errors.append(f"NetworkFailed: {url} | {error_text}")
        except Exception:
            continue
    return net_errors


def collect_logs(driver, page_name):
    """采集控制台与网络错误日志，写入文件"""
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

    # performance 日志（网络失败）
    try:
        perf_logs = driver.get_log('performance')
        net_errors = parse_performance_logs(perf_logs)
        logs.extend(net_errors)
    except Exception:
        pass

    # 输出到文件
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{page_name}.log"
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"\n==== {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ====: {page_name} ===\n")
        if logs:
            f.write("\n".join(logs) + "\n")
        else:
            f.write("No errors captured.\n")
    return logs


def take_screenshot(driver, page_path, output_name):
    """截取指定页面的截图并记录日志"""
    try:
        url = f"{BASE_URL}/{page_path}"
        print(f"📸 正在截图: {page_path}")
        driver.get(url)
        
        # 初步等待页面主要结构加载
        time.sleep(2)
        
        # 等待统一侧边栏加载完成（尽量保证视觉完整）
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "sidebar-container"))
            )
        except Exception:
            print(f"⚠️  侧边栏未完全加载: {page_path}")
        
        # 额外等待可能的异步内容
        time.sleep(1.5)
        
        # 调整窗口高度以覆盖页面整体高度
        total_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight, document.documentElement.offsetHeight)")
        driver.set_window_size(1920, max(1080, int(total_height)))
        
        # 截图
        output_path = IMG_DIR / f"{output_name}.png"
        driver.save_screenshot(str(output_path))

        # 采集日志
        logs = collect_logs(driver, output_name)
        err_count = len(logs)
        if err_count:
            print(f"⚠️  捕获到 {err_count} 条错误日志: {output_name}.log")
        else:
            print("✅ 未发现错误日志")

        print(f"✅ 截图成功: {output_path.name}")
        return True
    except Exception as e:
        print(f"❌ 截图失败: {page_path} - {e}")
        return False


def main():
    """主函数"""
    print("开始批量截取页面截图并收集日志...")
    print("=" * 60)
    
    # 确保输出目录存在
    IMG_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # 初始化WebDriver
    driver = setup_driver()
    if not driver:
        return
    
    try:
        success_count = 0
        total_count = len(TARGET_PAGES)
        pages_with_errors = []
        
        for page_path in TARGET_PAGES:
            output_name = Path(page_path).name  # 如 用户列表.html
            
            # 检查页面文件是否存在
            page_file = ADMIN_DIR / page_path
            if not page_file.exists():
                print(f"⚠️  页面文件不存在: {page_path}")
                continue
                
            # 截图 + 日志
            ok = take_screenshot(driver, page_path, output_name)
            if ok:
                success_count += 1
                # 粗略统计本页错误
                log_file = LOG_DIR / f"{output_name}.log"
                try:
                    if log_file.exists() and log_file.stat().st_size > 0:
                        with open(log_file, 'r', encoding='utf-8') as lf:
                            content = lf.read()
                            # 粗略判断是否包含Console/Network错误
                            if 'Console[' in content or 'NetworkFailed:' in content:
                                pages_with_errors.append(output_name)
                except Exception:
                    pass
            
            # 短暂延迟避免请求过快
            time.sleep(1)
        
        print("\n" + "=" * 60)
        print("截图与日志任务完成!")
        print(f"成功截图: {success_count}/{total_count} 个页面")
        if pages_with_errors:
            print(f"存在错误日志的页面 ({len(pages_with_errors)}):")
            for p in pages_with_errors:
                print(f" - {p}")
        else:
            print("所有页面均未捕获到错误日志 ✅")
        print(f"截图保存位置: {IMG_DIR}")
        print(f"日志保存位置: {LOG_DIR}")
        
    finally:
        driver.quit()


if __name__ == '__main__':
    main()