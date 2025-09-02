// 生成部分菜单SQL插入语句的脚本
// 生成几个关键菜单的SQL语句以便通过MCP工具直接执行

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

// 生成部分关键菜单的SQL插入语句
function generatePartialInsertSQL() {
    const currentTime = getCurrentTime();
    const sqlStatements = [
        '-- 插入部分关键菜单数据',
        
        // 审核管理菜单
        `INSERT INTO sys_menu (scale_menu_id, menu_path, menu_name, menu_iconcls, menu_type, menu_status, menu_parentid, menu_order, create_time, update_time) VALUES ('M000009', '/1.0/超级管理员/审核管理/', '审核管理', 'nav-icon-audit', '1', '1', '', '3', '${currentTime}', '${currentTime}') ON DUPLICATE KEY UPDATE menu_path = VALUES(menu_path), menu_name = VALUES(menu_name), menu_iconcls = VALUES(menu_iconcls), menu_type = VALUES(menu_type), menu_status = VALUES(menu_status), menu_parentid = VALUES(menu_parentid), menu_order = VALUES(menu_order), update_time = VALUES(update_time);`,
        
        // 审核流程菜单（二级菜单）
        `INSERT INTO sys_menu (scale_menu_id, menu_path, menu_name, menu_iconcls, menu_type, menu_status, menu_parentid, menu_order, create_time, update_time) VALUES ('M000025', '/1.0/超级管理员/审核管理/审核流程.html', '审核流程', 'nav-icon-process', '2', '1', 'M000009', '1', '${currentTime}', '${currentTime}') ON DUPLICATE KEY UPDATE menu_path = VALUES(menu_path), menu_name = VALUES(menu_name), menu_iconcls = VALUES(menu_iconcls), menu_type = VALUES(menu_type), menu_status = VALUES(menu_status), menu_parentid = VALUES(menu_parentid), menu_order = VALUES(menu_order), update_time = VALUES(update_time);`,
        
        // 事前审核记录（三级菜单）
        `INSERT INTO sys_menu (scale_menu_id, menu_path, menu_name, menu_iconcls, menu_type, menu_status, menu_parentid, menu_order, create_time, update_time) VALUES ('M000026', '/1.0/超级管理员/审核管理/事前审核记录.html', '事前审核记录', 'nav-icon-search', '2', '1', 'M000025', '1', '${currentTime}', '${currentTime}') ON DUPLICATE KEY UPDATE menu_path = VALUES(menu_path), menu_name = VALUES(menu_name), menu_iconcls = VALUES(menu_iconcls), menu_type = VALUES(menu_type), menu_status = VALUES(menu_status), menu_parentid = VALUES(menu_parentid), menu_order = VALUES(menu_order), update_time = VALUES(update_time);`,
        
        // 事中审核检查（三级菜单）
        `INSERT INTO sys_menu (scale_menu_id, menu_path, menu_name, menu_iconcls, menu_type, menu_status, menu_parentid, menu_order, create_time, update_time) VALUES ('M000027', '/1.0/超级管理员/审核管理/事中审核检查.html', '事中审核检查', 'nav-icon-check', '2', '1', 'M000025', '2', '${currentTime}', '${currentTime}') ON DUPLICATE KEY UPDATE menu_path = VALUES(menu_path), menu_name = VALUES(menu_name), menu_iconcls = VALUES(menu_iconcls), menu_type = VALUES(menu_type), menu_status = VALUES(menu_status), menu_parentid = VALUES(menu_parentid), menu_order = VALUES(menu_order), update_time = VALUES(update_time);`,
        
        // 事后审核任务（三级菜单）
        `INSERT INTO sys_menu (scale_menu_id, menu_path, menu_name, menu_iconcls, menu_type, menu_status, menu_parentid, menu_order, create_time, update_time) VALUES ('M000028', '/1.0/超级管理员/审核管理/事后审核任务.html', '事后审核任务', 'nav-icon-task', '2', '1', 'M000025', '3', '${currentTime}', '${currentTime}') ON DUPLICATE KEY UPDATE menu_path = VALUES(menu_path), menu_name = VALUES(menu_name), menu_iconcls = VALUES(menu_iconcls), menu_type = VALUES(menu_type), menu_status = VALUES(menu_status), menu_parentid = VALUES(menu_parentid), menu_order = VALUES(menu_order), update_time = VALUES(update_time);`,
        
        // 审核结果（二级菜单）
        `INSERT INTO sys_menu (scale_menu_id, menu_path, menu_name, menu_iconcls, menu_type, menu_status, menu_parentid, menu_order, create_time, update_time) VALUES ('M000029', '/1.0/超级管理员/审核管理/审核结果.html', '审核结果', 'nav-icon-results', '2', '1', 'M000009', '2', '${currentTime}', '${currentTime}') ON DUPLICATE KEY UPDATE menu_path = VALUES(menu_path), menu_name = VALUES(menu_name), menu_iconcls = VALUES(menu_iconcls), menu_type = VALUES(menu_type), menu_status = VALUES(menu_status), menu_parentid = VALUES(menu_parentid), menu_order = VALUES(menu_order), update_time = VALUES(update_time);`
    ];
    
    return sqlStatements.join('\n');
}

// 输出SQL语句
const sqlOutput = generatePartialInsertSQL();
console.log(sqlOutput);

// 如果在Node.js环境中运行，可以将SQL保存到文件
if (typeof require !== 'undefined') {
    const fs = require('fs');
    fs.writeFileSync('partial_menu_insert_sql.txt', sqlOutput, 'utf8');
    console.log('SQL语句已保存到 partial_menu_insert_sql.txt 文件');
}