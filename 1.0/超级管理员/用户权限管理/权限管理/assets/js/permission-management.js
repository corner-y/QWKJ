// 权限管理页面脚本
console.log('permission-management.js loaded');

// 全局变量
let roles = [
    {
        id: '超级管理员',
        name: '超级管理员',
        code: '超级管理员',
        type: 'system',
        description: '系统最高权限用户，拥有所有功能权限',
        status: 'active',
        userCount: 1,
        permissions: ['*'],
        createTime: '2024-01-01',
        createdBy: '系统创建'
    },
    {
        id: 'audit-manager',
        name: '审核主管',
        code: 'audit_manager',
        type: 'system',
        description: '负责审核业务的主管，拥有审核相关权限',
        status: 'active',
        userCount: 8,
        permissions: ['audit.*', 'user.view', 'rule.view'],
        createTime: '2024-01-15',
        createdBy: '超级管理员'
    },
    {
        id: 'audit-specialist',
        name: '审核专员',
        code: 'audit_specialist',
        type: 'custom',
        description: '执行具体审核工作的专员',
        status: 'active',
        userCount: 25,
        permissions: ['audit.pre', 'audit.during', 'audit.post'],
        createTime: '2024-01-20',
        createdBy: '审核主管'
    },
    {
        id: 'rule-admin',
        name: '规则管理员',
        code: 'rule_admin',
        type: 'system',
        description: '负责规则配置和管理',
        status: 'active',
        userCount: 5,
        permissions: ['rule.*', 'user.view'],
        createTime: '2024-02-01',
        createdBy: '超级管理员'
    },
    {
        id: 'tenant-admin',
        name: '租户管理员',
        code: 'tenant_admin',
        type: 'tenant',
        description: '负责租户管理和组织架构',
        status: 'active',
        userCount: 12,
        permissions: ['tenant.*', 'department.*', 'user.manage'],
        createTime: '2024-02-10',
        createdBy: '超级管理员'
    },
    {
        id: 'readonly-user',
        name: '只读用户',
        code: 'readonly_user',
        type: 'custom',
        description: '只能查看数据，无修改权限',
        status: 'active',
        userCount: 45,
        permissions: ['*.view'],
        createTime: '2024-02-15',
        createdBy: '系统创建'
    },
    {
        id: 'guest',
        name: '访客',
        code: 'guest',
        type: 'custom',
        description: '临时访问用户，权限最低',
        status: 'inactive',
        userCount: 0,
        permissions: ['dashboard.view'],
        createTime: '2024-03-01',
        createdBy: '系统创建'
    },
    {
        id: 'system-monitor',
        name: '系统监控员',
        code: 'system_monitor',
        type: 'system',
        description: '负责系统监控和维护',
        status: 'active',
        userCount: 3,
        permissions: ['system.*', 'monitor.*'],
        createTime: '2024-03-10',
        createdBy: '超级管理员'
    }
];

let selectedRoles = new Set();
let confirmCallback = null;

// 页面初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeTable();
    bindEvents();
    updateStatistics();
});

// 初始化表格
function initializeTable() {
    const tbody = document.getElementById('rolesTableBody') || document.querySelector('.role-table tbody');
    if (!tbody) return;
    tbody.innerHTML = roles.map(role => createRoleRow(role)).join('');
}

// 创建角色行HTML
function createRoleRow(role) {
    const statusClass = role.status === 'active' ? 'active' : 'inactive';
    const statusText = role.status === 'active' ? '启用' : '禁用';
    const typeMap = { system: '系统角色', custom: '自定义角色', tenant: '租户角色' };
    const typeClass = role.type || 'custom';
    const typeText = typeMap[typeClass] || '自定义角色';
    return `
        <tr data-role-id="${role.id}">
            <td><input type="checkbox" class="row-checkbox" value="${role.id}" onchange="updateBatchActions()"></td>
            <td>
                <div class="role-info">
                    <div class="role-name">${role.name}</div>
                    <div class="role-code">${role.code}</div>
                </div>
            </td>
            <td><span class="type-badge ${typeClass}">${typeText}</span></td>
            <td><span class="status-badge ${statusClass}">${statusText}</span></td>
            <td>
                <div class="user-count">
                    <span class="count-number">${role.userCount}</span>
                    <span class="count-label">个用户</span>
                </div>
            </td>
            <td>
                <div class="permission-count">
                    <span class="count-number">${role.permissions.length}</span>
                    <span class="count-label">个权限</span>
                </div>
            </td>
            <td>
                <div class="date-info">
                    <div class="date-primary">${role.createTime}</div>
                    <div class="date-secondary">${role.createdBy}</div>
                </div>
            </td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-sm btn-primary" onclick="viewRoleDetail('${role.id}')">查看</button>
                    <div class="dropdown">
                        <button class="btn btn-sm btn-secondary dropdown-toggle">更多</button>
                        <div class="dropdown-menu">
                            <a href="#" onclick="editRole('${role.id}')">编辑</a>
                            <a href="#" onclick="managePermissions('${role.id}')">权限配置</a>
                            <a href="#" onclick="copyRole('${role.id}')">复制角色</a>
                            <a href="#" onclick="toggleRoleStatus('${role.id}')">${role.status === 'active' ? '禁用' : '启用'}</a>
                            <a href="#" onclick="deleteRole('${role.id}')" class="text-danger">删除</a>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
    `;
}

// 绑定事件
function bindEvents() {
    const roleNameInput = document.getElementById('roleName');
    if (roleNameInput) roleNameInput.addEventListener('input', filterRoles);

    const roleStatusSelect = document.getElementById('roleStatus');
    if (roleStatusSelect) roleStatusSelect.addEventListener('change', filterRoles);

    const selectAll = document.getElementById('selectAll');
    if (selectAll) selectAll.addEventListener('change', toggleSelectAll);

    document.addEventListener('change', function(e) {
        if (e.target.classList.contains('row-checkbox')) {
            updateSelectedRoles();
            updateBatchActions();
        }
    });

    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('dropdown-toggle')) {
            e.preventDefault();
            toggleDropdown(e.target);
        } else {
            closeAllDropdowns();
        }
    });
}

// 过滤角色
function filterRoles() {
    const nameFilter = (document.getElementById('roleName')?.value || '').toLowerCase();
    const statusFilter = document.getElementById('roleStatus')?.value || '';
    const tbody = document.getElementById('rolesTableBody') || document.querySelector('.role-table tbody');
    if (!tbody) return;

    const filteredRoles = roles.filter(role => {
        const nameMatch = !nameFilter || role.name.toLowerCase().includes(nameFilter) || role.code.toLowerCase().includes(nameFilter);
        const statusMatch = !statusFilter || role.status === statusFilter;
        return nameMatch && statusMatch;
    });

    tbody.innerHTML = filteredRoles.map(role => createRoleRow(role)).join('');
    updateStatistics();
}

// 更新统计信息
function updateStatistics() {
    const totalRoles = roles.length;
    const activeUsers = roles.reduce((sum, role) => sum + role.userCount, 0);
    const totalPermissions = new Set(roles.flatMap(role => role.permissions)).size;
    const newRolesThisMonth = roles.filter(role => {
        const createDate = new Date(role.createTime);
        const thisMonth = new Date();
        return createDate.getMonth() === thisMonth.getMonth() && 
               createDate.getFullYear() === thisMonth.getFullYear();
    }).length;
    
    document.querySelector('.stat-card.total .stat-value').textContent = totalRoles;
    document.querySelector('.stat-card.total .trend-value').textContent = `+${newRolesThisMonth}`;
    document.querySelector('.stat-card.active .stat-value').textContent = activeUsers;
    document.querySelector('.stat-card.revenue .stat-value').textContent = totalPermissions;
    document.querySelector('.stat-card.revenue .trend-value').textContent = `+${Math.floor(Math.random() * 10)}`;
}

// 角色操作函数
function addRole() {
    showRoleDrawer();
}

function viewRoleDetail(roleId) {
    const role = roles.find(r => r.id === roleId);
    if (!role) return;
    
    document.getElementById('detailRoleName').textContent = role.name;
    document.getElementById('detailRoleCode').textContent = role.code;
    document.getElementById('detailRoleDescription').textContent = role.description;
    document.getElementById('detailRoleStatus').textContent = role.status === 'active' ? '启用' : '禁用';
    document.getElementById('detailUserCount').textContent = `${role.userCount} 个用户`;
    document.getElementById('detailPermissionCount').textContent = `${role.permissions.length} 个权限`;
    document.getElementById('detailCreateTime').textContent = role.createTime;
    
    document.getElementById('roleDetailDrawer').style.display = 'flex';
}

function editRole(roleId) {
    const role = roles.find(r => r.id === roleId);
    if (!role) return;

    const drawer = document.getElementById('roleDrawer');
    if (drawer) {
        const nameInput = drawer.querySelector('#roleName');
        const codeInput = drawer.querySelector('#roleCode');
        const descInput = drawer.querySelector('#roleDescription');
        const statusSelect = drawer.querySelector('#roleStatus');
        if (nameInput) nameInput.value = role.name;
        if (codeInput) codeInput.value = role.code;
        if (descInput) descInput.value = role.description;
        if (statusSelect) statusSelect.value = role.status;
    }

    showRoleDrawer('编辑角色', roleId);
}

function managePermissions(roleId) {
    const role = roles.find(r => r.id === roleId);
    if (!role) return;
    
    document.getElementById('permissionDrawerTitle').textContent = `${role.name} - 权限配置`;
    // 这里应该加载权限树并设置当前角色的权限
    document.getElementById('permissionDrawer').style.display = 'flex';
}

function copyRole(roleId) {
    const role = roles.find(r => r.id === roleId);
    if (!role) return;
    
    const newRole = {
        ...role,
        id: `${role.id}_copy_${Date.now()}`,
        name: `${role.name}_副本`,
        code: `${role.code}_copy`,
        userCount: 0,
        createTime: new Date().toISOString().split('T')[0],
        createdBy: '超级管理员'
    };
    
    roles.push(newRole);
    initializeTable();
    updateStatistics();
    showSuccessMessage('角色复制成功');
}

function toggleRoleStatus(roleId) {
    const role = roles.find(r => r.id === roleId);
    if (!role) return;
    
    const action = role.status === 'active' ? '禁用' : '启用';
    showConfirmModal(
        `确认${action}角色`,
        `确定要${action}角色"${role.name}"吗？`,
        () => {
            role.status = role.status === 'active' ? 'inactive' : 'active';
            initializeTable();
            showSuccessMessage(`角色${action}成功`);
        }
    );
}

function deleteRole(roleId) {
    const role = roles.find(r => r.id === roleId);
    if (!role) return;
    
    if (role.userCount > 0) {
        showErrorMessage('该角色下还有用户，无法删除');
        return;
    }
    
    showConfirmModal(
        '确认删除角色',
        `确定要删除角色"${role.name}"吗？删除后无法恢复。`,
        () => {
            roles = roles.filter(r => r.id !== roleId);
            initializeTable();
            updateStatistics();
            showSuccessMessage('角色删除成功');
        }
    );
}

// 抽屉/模态框操作
function showRoleDrawer(title = '新增角色', roleId = null) {
    document.querySelector('#roleDrawer .drawer-header h3').textContent = title;
    const drawer = document.getElementById('roleDrawer');
    drawer.style.display = 'flex';
    const nameInput = drawer.querySelector('#roleName');
    const codeInput = drawer.querySelector('#roleCode');
    const descInput = drawer.querySelector('#roleDescription');
    const statusSelect = drawer.querySelector('#roleStatus');

    if (!roleId) {
        if (nameInput) nameInput.value = '';
        if (codeInput) codeInput.value = '';
        if (descInput) descInput.value = '';
        if (statusSelect) statusSelect.value = 'active';
    }
}

function closeRoleDrawer() {
    document.getElementById('roleDrawer').style.display = 'none';
}

function closeRoleDetailDrawer() {
    document.getElementById('roleDetailDrawer').style.display = 'none';
}

function closePermissionDrawer() {
    document.getElementById('permissionDrawer').style.display = 'none';
}

function saveRole() {
    const drawer = document.getElementById('roleDrawer');
    const nameInput = drawer ? drawer.querySelector('#roleName') : document.getElementById('roleName');
    const codeInput = drawer ? drawer.querySelector('#roleCode') : document.getElementById('roleCode');
    const descInput = drawer ? drawer.querySelector('#roleDescription') : document.getElementById('roleDescription');
    const statusSelect = drawer ? drawer.querySelector('#roleStatus') : document.getElementById('roleStatus');

    const name = (nameInput?.value || '').trim();
    const code = (codeInput?.value || '').trim();

    if (!name) {
        showFieldError('roleNameError', '请输入角色名称');
        return;
    }
    if (!code) {
        showFieldError('roleCodeError', '请输入角色代码');
        return;
    }
    if (roles.some(r => r.code === code)) {
        showFieldError('roleCodeError', '角色代码已存在');
        return;
    }

    const newRole = {
        id: `role_${Date.now()}`,
        name: name,
        code: code,
        description: (descInput?.value || '').trim(),
        status: statusSelect?.value || 'active',
        userCount: 0,
        permissions: [],
        createTime: new Date().toISOString().split('T')[0],
        createdBy: '超级管理员'
    };

    roles.push(newRole);
    initializeTable();
    updateStatistics();
    closeRoleDrawer();
    showSuccessMessage('角色创建成功');
}

// 批量操作
function updateSelectedRoles() {
    selectedRoles.clear();
    document.querySelectorAll('.row-checkbox:checked').forEach(cb => {
        selectedRoles.add(cb.value);
    });
}

function updateBatchActions() {
    const count = selectedRoles.size;
    const batchActions = document.querySelector('.batch-actions');
    if (batchActions) {
        batchActions.style.display = count > 0 ? 'flex' : 'none';
        if (count > 0) {
            batchActions.querySelector('.selected-count').textContent = `已选择 ${count} 项`;
        }
    }
}

function toggleSelectAll(e) {
    const checked = e ? e.target.checked : (document.getElementById('selectAll')?.checked || false);
    const checkboxes = document.querySelectorAll('.row-checkbox');
    checkboxes.forEach(cb => cb.checked = checked);
    updateSelectedRoles();
    updateBatchActions();
}

// 工具函数
function toggleDropdown(button) {
    const dropdown = button.nextElementSibling;
    const isVisible = dropdown.style.display === 'block';
    
    closeAllDropdowns();
    
    if (!isVisible) {
        dropdown.style.display = 'block';
    }
}

function closeAllDropdowns() {
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        menu.style.display = 'none';
    });
}

function showConfirmModal(title, message, callback) {
    document.getElementById('confirmTitle').textContent = title;
    document.getElementById('confirmMessage').textContent = message;
    confirmCallback = callback;
    document.getElementById('confirmModal').style.display = 'flex';
}

function closeConfirmModal() {
    document.getElementById('confirmModal').style.display = 'none';
    confirmCallback = null;
}

function confirmAction() {
    if (confirmCallback) {
        confirmCallback();
    }
    closeConfirmModal();
}

function showFieldError(fieldId, message) {
    const errorElement = document.getElementById(fieldId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        setTimeout(() => {
            errorElement.style.display = 'none';
        }, 3000);
    }
}

function showSuccessMessage(message) {
    // 简单的成功提示，可以扩展为更美观的通知组件
    alert(message);
}

function showErrorMessage(message) {
    // 简单的错误提示，可以扩展为更美观的通知组件
    alert(message);
}

// 退出登录
function logout() {
    showConfirmModal(
        '确认退出',
        '确定要退出系统吗？',
        () => {
            window.location.href = '../../登录.html';
        }
    );
}

// 供“搜索”按钮调用
function searchRoles() {
    // 供“搜索”按钮调用
    filterRoles();
}