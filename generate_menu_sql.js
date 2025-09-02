// 生成菜单SQL插入语句的脚本
// 从HTML文件中解析菜单数据并生成SQL语句

// 模拟的menuData对象（从HTML中提取）
const menuData = {
    '1': {
        name: '工作台',
        icon: 'nav-icon-dashboard',
        path: '/1.0/超级管理员/工作台/',
        parent: '0',
        sort: '1',
        status: 'enabled'
    },
    '2': {
        name: '平台运营看板',
        icon: 'nav-icon-chart',
        path: '/1.0/超级管理员/工作台/平台运营看板.html',
        parent: '1',
        sort: '1',
        status: 'enabled'
    },
    '3': {
        name: '报告规则分析',
        icon: 'nav-icon-analysis',
        path: '/1.0/超级管理员/工作台/报告规则分析.html',
        parent: '1',
        sort: '2',
        status: 'enabled'
    },
    '4': {
        name: '规则管理',
        icon: 'nav-icon-rules',
        path: '/1.0/超级管理员/规则管理/',
        parent: '0',
        sort: '2',
        status: 'enabled'
    },
    '5': {
        name: '药品规则库',
        icon: 'nav-icon-drug',
        path: '/1.0/超级管理员/规则管理/药品规则库.html',
        parent: '4',
        sort: '1',
        status: 'enabled'
    },
    '6': {
        name: '慢病规则库',
        icon: 'nav-icon-chronic',
        path: '/1.0/超级管理员/规则管理/慢病规则库.html',
        parent: '4',
        sort: '2',
        status: 'enabled'
    },
    '7': {
        name: '诊疗规则库',
        icon: 'nav-icon-clinical',
        path: '/1.0/超级管理员/规则管理/诊疗规则库.html',
        parent: '4',
        sort: '3',
        status: 'enabled'
    },
    '8': {
        name: '政策规则库',
        icon: 'nav-icon-policy',
        path: '/1.0/超级管理员/规则管理/政策规则库.html',
        parent: '4',
        sort: '4',
        status: 'enabled'
    },
    // 审核管理
    '9': {
        name: '审核管理',
        icon: 'nav-icon-audit',
        path: '/1.0/超级管理员/审核管理/',
        parent: '0',
        sort: '3',
        status: 'enabled'
    },
    '25': {
        name: '审核流程',
        icon: 'nav-icon-process',
        path: '/1.0/超级管理员/审核管理/审核流程.html',
        parent: '9',
        sort: '1',
        status: 'enabled'
    },
    '26': {
        name: '事前审核记录',
        icon: 'nav-icon-search',
        path: '/1.0/超级管理员/审核管理/事前审核记录.html',
        parent: '25',
        sort: '1',
        status: 'enabled'
    },
    '27': {
        name: '事中审核检查',
        icon: 'nav-icon-check',
        path: '/1.0/超级管理员/审核管理/事中审核检查.html',
        parent: '25',
        sort: '2',
        status: 'enabled'
    },
    '28': {
        name: '事后审核任务',
        icon: 'nav-icon-task',
        path: '/1.0/超级管理员/审核管理/事后审核任务.html',
        parent: '25',
        sort: '3',
        status: 'enabled'
    },
    '29': {
        name: '审核结果',
        icon: 'nav-icon-results',
        path: '/1.0/超级管理员/审核管理/审核结果.html',
        parent: '9',
        sort: '2',
        status: 'enabled'
    },
    // 事后审核管理
    '10': {
        name: '事后审核管理',
        icon: 'nav-icon-analytics',
        path: '/1.0/超级管理员/事后审核管理/',
        parent: '0',
        sort: '4',
        status: 'enabled'
    },
    '30': {
        name: '审核进度监控台',
        icon: 'nav-icon-monitor',
        path: '/1.0/超级管理员/事后审核管理/审核进度监控台.html',
        parent: '10',
        sort: '1',
        status: 'enabled'
    },
    '31': {
        name: '诊疗数据上传',
        icon: 'nav-icon-upload',
        path: '/1.0/超级管理员/事后审核管理/诊疗数据上传.html',
        parent: '10',
        sort: '2',
        status: 'enabled'
    },
    '32': {
        name: '人工审核工作台',
        icon: 'nav-icon-workbench',
        path: '/1.0/超级管理员/事后审核管理/人工审核工作台.html',
        parent: '10',
        sort: '3',
        status: 'enabled'
    },
    '33': {
        name: '稽核交互中心',
        icon: 'nav-icon-interaction',
        path: '/1.0/超级管理员/事后审核管理/稽核交互中心.html',
        parent: '10',
        sort: '4',
        status: 'enabled'
    },
    '34': {
        name: '审核结果管理',
        icon: 'nav-icon-results',
        path: '/1.0/超级管理员/事后审核管理/审核结果管理.html',
        parent: '10',
        sort: '5',
        status: 'enabled'
    },
    // 用户权限管理
    '11': {
        name: '用户权限管理',
        icon: 'nav-icon-users',
        path: '/1.0/超级管理员/用户权限管理/',
        parent: '0',
        sort: '5',
        status: 'enabled'
    },
    // 系统管理
    '12': {
        name: '系统管理',
        icon: 'nav-icon-system',
        path: '/1.0/超级管理员/系统管理/',
        parent: '0',
        sort: '6',
        status: 'enabled'
    },
    '13': {
        name: '全局设置',
        icon: 'nav-icon-settings',
        path: '/1.0/超级管理员/系统管理/全局设置.html',
        parent: '12',
        sort: '1',
        status: 'enabled'
    },
    '14': {
        name: '系统监控',
        icon: 'nav-icon-monitor',
        path: '/1.0/超级管理员/系统管理/系统监控.html',
        parent: '12',
        sort: '2',
        status: 'enabled'
    },
    '15': {
        name: '菜单管理',
        icon: 'nav-icon-settings',
        path: '/1.0/超级管理员/系统管理/菜单管理.html',
        parent: '12',
        sort: '3',
        status: 'enabled'
    },
    // 慢病管理
    '17': {
        name: '慢病管理',
        icon: 'nav-icon-chronic',
        path: '/1.0/超级管理员/慢病管理/',
        parent: '0',
        sort: '8',
        status: 'enabled'
    },
    '18': {
        name: '慢病资格申报',
        icon: 'nav-icon-apply',
        path: '/1.0/超级管理员/慢病管理/慢病资格申报.html',
        parent: '17',
        sort: '1',
        status: 'enabled'
    },
    '19': {
        name: '慢病资格评审',
        icon: 'nav-icon-review',
        path: '/1.0/超级管理员/慢病管理/慢病资格评审.html',
        parent: '17',
        sort: '2',
        status: 'enabled'
    },
    '20': {
        name: '评审结果管理',
        icon: 'nav-icon-result',
        path: '/1.0/超级管理员/慢病管理/评审结果管理.html',
        parent: '17',
        sort: '3',
        status: 'enabled'
    },
    '21': {
        name: '慢病数据看板',
        icon: 'nav-icon-dashboard',
        path: '/1.0/超级管理员/慢病管理/慢病数据看板.html',
        parent: '17',
        sort: '4',
        status: 'enabled'
    },
    // 知识库
    '22': {
        name: '知识库',
        icon: 'nav-icon-knowledge',
        path: '/1.0/超级管理员/知识库/',
        parent: '0',
        sort: '9',
        status: 'enabled'
    },
    '23': {
        name: '药品目录',
        icon: 'nav-icon-list',
        path: '/1.0/超级管理员/知识库/药品目录.html',
        parent: '22',
        sort: '1',
        status: 'enabled'
    },
    '24': {
        name: '诊疗目录',
        icon: 'nav-icon-list',
        path: '/1.0/超级管理员/知识库/诊疗目录.html',
        parent: '22',
        sort: '2',
        status: 'enabled'
    },
    '35': {
        name: '耗材目录',
        icon: 'nav-icon-list',
        path: '/1.0/超级管理员/知识库/耗材目录.html',
        parent: '22',
        sort: '3',
        status: 'enabled'
    }
};

// 生成当前时间戳
function getCurrentTime() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

// 生成SQL插入语句
function generateInsertSQL() {
    const currentTime = getCurrentTime();
    let sqlStatements = [];
    
    // 清空表（可选，根据需求决定是否执行）
    // sqlStatements.push('-- 清空现有菜单数据（可选）');
    // sqlStatements.push('DELETE FROM sys_menu;');
    // sqlStatements.push('');
    
    sqlStatements.push('-- 插入菜单数据');
    
    Object.entries(menuData).forEach(([menuId, menuInfo]) => {
        // 转换ID格式为M00000X
        const scaleMenuId = `M${parseInt(menuId).toString().padStart(6, '0')}`;
        
        // 确定菜单类型（1-一级菜单，2-二级菜单）
        const menuType = menuInfo.parent === '0' ? '1' : '2';
        
        // 转换父ID格式
        const menuParentId = menuInfo.parent === '0' ? '' : `M${parseInt(menuInfo.parent).toString().padStart(6, '0')}`;
        
        // 转换状态（1-启用，2-禁用）
        const menuStatus = menuInfo.status === 'enabled' ? '1' : '2';
        
        // 构建SQL插入语句
        const sql = `INSERT INTO sys_menu (scale_menu_id, menu_path, menu_name, menu_iconcls, menu_type, menu_status, menu_parentid, menu_order, create_time, update_time) VALUES ('${scaleMenuId}', '${menuInfo.path}', '${menuInfo.name}', '${menuInfo.icon}', '${menuType}', '${menuStatus}', '${menuParentId}', '${menuInfo.sort}', '${currentTime}', '${currentTime}') ON DUPLICATE KEY UPDATE menu_path = VALUES(menu_path), menu_name = VALUES(menu_name), menu_iconcls = VALUES(menu_iconcls), menu_type = VALUES(menu_type), menu_status = VALUES(menu_status), menu_parentid = VALUES(menu_parentid), menu_order = VALUES(menu_order), update_time = VALUES(update_time);`;
        
        sqlStatements.push(sql);
    });
    
    return sqlStatements.join('\n');
}

// 输出SQL语句
const sqlOutput = generateInsertSQL();
console.log(sqlOutput);

// 如果在Node.js环境中运行，可以将SQL保存到文件
if (typeof require !== 'undefined') {
    const fs = require('fs');
    fs.writeFileSync('menu_insert_sql.txt', sqlOutput, 'utf8');
    console.log('SQL语句已保存到 menu_insert_sql.txt 文件');
}