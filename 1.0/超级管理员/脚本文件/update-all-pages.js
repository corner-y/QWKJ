// 批量更新所有页面使用统一菜单的脚本

// 页面配置映射
const pageConfigs = {
    // 工作台模块
    '工作台/工作台.html': { menu: 'dashboard', level: 1 },
    '工作台/平台运营看板.html': { menu: 'dashboard-overview', level: 2 },
    '工作台/报告规则分析.html': { menu: 'dashboard-analysis', level: 2 },
    
    // 规则管理模块
    '规则管理/规则列表/规则管理主页.html': { menu: 'rules-main', level: 3 },
    '规则管理/规则列表/门诊规则管理.html': { menu: 'rules-outpatient', level: 3 },
    '规则管理/规则列表/医保规则管理系统v2.html': { menu: 'rules-medical', level: 3 },
    '规则管理/规则详情/规则详情.html': { menu: 'rules-detail-general', level: 3 },
    '规则管理/规则详情/临床规则详情.html': { menu: 'rules-detail-clinical', level: 3 },
    '规则管理/规则详情/慢病规则详情.html': { menu: 'rules-detail-chronic', level: 3 },
    '规则管理/规则详情/政策规则详情.html': { menu: 'rules-detail-policy', level: 3 },
    '规则管理/规则详情/门诊规则详情.html': { menu: 'rules-detail-outpatient', level: 3 },
    '规则管理/规则操作/创建规则.html': { menu: 'rules-create', level: 3 },
    '规则管理/规则操作/编辑规则.html': { menu: 'rules-edit', level: 3 },
    '规则管理/规则操作/规则参数配置.html': { menu: 'rules-config', level: 3 },
    '规则管理/规则操作/规则管理完整版.html': { menu: 'rules-full', level: 3 },
    
    // 审核管理模块
    '审核管理/审核流程/事前审核记录.html': { menu: 'audit-pre', level: 3 },
    '审核管理/审核流程/事中审核检查.html': { menu: 'audit-during', level: 3 },
    '审核管理/审核流程/事后审核任务列表.html': { menu: 'audit-post', level: 3 },
    '审核管理/审核结果/审核结果.html': { menu: 'audit-results', level: 2 },
    
    // 用户权限管理模块
    '用户权限管理/用户管理/用户列表.html': { menu: 'user-list', level: 2 },
    '用户权限管理/权限管理/权限管理.html': { menu: 'permission', level: 2 },
    '用户权限管理/组织管理/科室管理.html': { menu: 'department', level: 3 },
    '用户权限管理/组织管理/租户管理.html': { menu: 'tenant', level: 3 },
    '用户权限管理/组织管理/租户表单.html': { menu: 'tenant-form', level: 3 },
    '用户权限管理/组织管理/企业详情.html': { menu: 'enterprise', level: 3 },
    
    // 系统管理模块
    '系统管理/全局设置.html': { menu: 'global-settings', level: 2 },
    '系统管理/系统监控.html': { menu: 'system-monitor', level: 2 },
    '系统管理/知识库目录.html': { menu: 'knowledge-base', level: 2 }
};

// 生成菜单加载脚本
function generateMenuScript(pageConfig) {
    const { menu, level } = pageConfig;
    const relativePath = level === 1 ? '../组件/_unified-sidebar.html' : 
                        level === 2 ? '../../组件/_unified-sidebar.html' : 
                        '../../../组件/_unified-sidebar.html';
    
    return `
    <!-- 加载统一菜单 -->
    <script>
        // 加载统一菜单组件
        fetch('${relativePath}')
            .then(response => response.text())
            .then(html => {
                document.getElementById('sidebar-container').innerHTML = html;
                // 设置当前页面菜单高亮
                const currentMenuItem = document.querySelector('[data-menu="${menu}"]');
                if (currentMenuItem) {
                    currentMenuItem.classList.add('active');
                    // 展开父级菜单组
                    let parent = currentMenuItem.closest('.nav-group, .nav-subgroup');
                    while (parent) {
                        parent.classList.add('expanded');
                        const submenu = parent.querySelector('.nav-submenu');
                        if (submenu) {
                            submenu.style.display = 'block';
                        }
                        parent = parent.parentElement.closest('.nav-group, .nav-subgroup');
                    }
                }
            })
            .catch(error => console.error('Error loading sidebar:', error));
    </script>`;
}

// 生成样式引用
function generateStyleLinks(level) {
    const prefix = level === 1 ? '../' : level === 2 ? '../../' : '../../../';
    return `
    <link rel="stylesheet" href="${prefix}样式文件/通用样式.css">
    <link rel="stylesheet" href="${prefix}样式文件/unified-sidebar.css">`;
}

// 生成统一的菜单容器
function generateSidebarContainer() {
    return `
    <div class="dashboard-container">
        <!-- 统一左侧菜单 -->
        <div id="sidebar-container"></div>
        
        <!-- 主内容区域 -->
        <div class="main-content">`;
}

// 输出配置信息供手动更新使用
console.log('页面配置信息：');
for (const [path, config] of Object.entries(pageConfigs)) {
    console.log(`${path}: ${config.menu} (Level ${config.level})`);
}

// 新增：批量注入统一菜单到指定页面（供自动化修复复用）
function applyUnifiedMenuToDocument({ menu, level }) {
    const prefix = level === 1 ? '../' : level === 2 ? '../../' : '../../../';

    // 1) 注入样式（若不存在）
    if (!document.querySelector(`link[href$="unified-sidebar.css"]`)) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = `${prefix}样式文件/unified-sidebar.css`;
        document.head.appendChild(link);
    }

    // 2) 注入容器（若不存在）
    if (!document.getElementById('sidebar-container')) {
        const dashboard = document.querySelector('.dashboard-container');
        if (dashboard) {
            const container = document.createElement('div');
            container.id = 'sidebar-container';
            dashboard.insertBefore(container, dashboard.firstChild);
        } else {
            // 如果没有标准布局，则创建一个
            const main = document.body;
            const wrapper = document.createElement('div');
            wrapper.className = 'dashboard-container';
            const container = document.createElement('div');
            container.id = 'sidebar-container';
            const mainContent = document.createElement('div');
            mainContent.className = 'main-content';
            // 将现有内容迁移至主内容区
            while (main.firstChild) {
                mainContent.appendChild(main.firstChild);
            }
            wrapper.appendChild(container);
            wrapper.appendChild(mainContent);
            main.appendChild(wrapper);
        }
    }

    // 3) 注入菜单加载脚本（若未加载过）
    if (!document.body.dataset.sidebarLoaded) {
        fetch(`${prefix}组件/_unified-sidebar.html`).then(r => r.text()).then(html => {
            const mount = document.getElementById('sidebar-container');
            if (mount) {
                mount.innerHTML = html;
                if (typeof window.initSidebar === 'function') {
                    window.initSidebar();
                }
                // 高亮当前菜单
                const currentMenuItem = document.querySelector(`[data-menu="${menu}"]`);
                if (currentMenuItem) {
                    currentMenuItem.classList.add('active');
                    let parent = currentMenuItem.closest('.nav-group, .nav-subgroup');
                    while (parent) {
                        parent.classList.add('expanded');
                        const submenu = parent.querySelector('.nav-submenu');
                        if (submenu) submenu.style.display = 'block';
                        parent = parent.parentElement && parent.parentElement.closest ? parent.parentElement.closest('.nav-group, .nav-subgroup') : null;
                    }
                }
                document.body.dataset.sidebarLoaded = '1';
            }
        }).catch(err => console.error('Error loading sidebar:', err));
    }
}

// 提供一个统一的入口，供外部调用
function applyUnifiedMenuByPath(path) {
    const cfg = pageConfigs[path];
    if (!cfg) return false;
    applyUnifiedMenuToDocument(cfg);
    return true;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports.applyUnifiedMenuToDocument = applyUnifiedMenuToDocument;
    module.exports.applyUnifiedMenuByPath = applyUnifiedMenuByPath;
}

if (typeof window !== 'undefined') {
    window.applyUnifiedMenuToDocument = applyUnifiedMenuToDocument;
    window.applyUnifiedMenuByPath = applyUnifiedMenuByPath;
}

// 输出配置和函数
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        pageConfigs,
        generateMenuScript,
        generateStyleLinks,
        generateSidebarContainer
    };
}

// 浏览器环境下的全局变量
if (typeof window !== 'undefined') {
    window.PageUpdateUtils = {
        pageConfigs,
        generateMenuScript,
        generateStyleLinks,
        generateSidebarContainer
    };
}