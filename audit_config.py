"""
医保审核系统UI+导航审查配置
用于统一管理页面列表、菜单结构和路径配置
"""

from pathlib import Path

# 基础路径配置
ROOT = Path(__file__).resolve().parent
ADMIN_DIR = ROOT / '1.0' / '超级管理员'
IMG_DIR = ROOT / 'img'
LOG_DIR = IMG_DIR / 'logs'
AUDIT_DIR = ROOT / 'audit_reports'
COMMON_CSS = ROOT / '1.0' / '样式文件' / '通用样式.css'
BASE_URL = 'http://localhost:8000/1.0/超级管理员'

# 审查页面配置
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

# 标准菜单结构配置
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

# 自动修复标记
SIDEBAR_SNIPPET_MARK = '/* unified-sidebar: injected */'
CHART_CSS_MARK = '/* ui_audit_and_fix: charts min-height */'
UI_FIX_MARK = '/* ui_nav_audit_and_fix: auto-applied */'