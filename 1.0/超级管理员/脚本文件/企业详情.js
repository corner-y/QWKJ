// 企业详情页面JavaScript

// 全局变量
let currentTenant = null;

// 页面初始化
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
    bindEvents();
    loadTenantData();
});

// 初始化页面
function initializePage() {
    console.log('企业详情页面初始化');
    
    // 页面加载时滚动到顶部
    window.scrollTo(0, 0);
    
    // 从URL参数获取企业ID
    const urlParams = new URLSearchParams(window.location.search);
    const tenantId = urlParams.get('id');
    
    if (tenantId) {
        console.log('企业ID:', tenantId);
    } else {
        console.warn('未找到企业ID参数');
    }
}

// 绑定事件
function bindEvents() {
    // Tab切换事件
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabName = this.dataset.tab;
            switchTab(tabName);
        });
    });
    
    // 抽屉关闭事件
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('drawer-overlay')) {
            closeAllDrawers();
        }
    });
    
    // ESC键关闭抽屉
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeAllDrawers();
        }
    });
}

// 加载企业数据
function loadTenantData() {
    // 模拟从API加载数据
    const urlParams = new URLSearchParams(window.location.search);
    const tenantId = urlParams.get('id') || '1';
    
    // 模拟API调用
    setTimeout(() => {
        currentTenant = {
            id: tenantId,
            companyName: '示例医疗集团有限公司',
            companyType: '医疗机构',
            contactName: '张三',
            contactPhone: '13800138000',
            region: '北京市朝阳区',
            createTime: '2024-01-15 10:30:00',
            status: 'active',
            package: {
                type: '标准版',
                price: 2999,
                startDate: '2024-01-15',
                duration: '12个月',
                features: {
                    '智能审核': true,
                    '数据分析': true,
                    '报表生成': true,
                    '高级分析': false
                }
            },
            staff: [
                {
                    id: 1,
                    name: '张三',
                    phone: '13800138000',
                    email: 'zhangsan@example.com',
                    role: 'admin',
                    department: '信息科',
                    status: 'active'
                }
            ],
            contact: {
                primaryContact: {
                    name: '张三',
                    position: '信息科主任',
                    phone: '13800138000',
                    email: 'zhangsan@example.com'
                },
                address: {
                    region: '北京市朝阳区',
                    detail: '朝阳路123号医疗大厦15层',
                    postcode: '100020'
                }
            }
        };
        
        updatePageData();
    }, 500);
}

// 更新页面数据
function updatePageData() {
    if (!currentTenant) return;
    
    // 更新基本信息
    document.getElementById('companyName').textContent = currentTenant.companyName;
    document.getElementById('companyType').textContent = currentTenant.companyType;
    document.getElementById('contactName').textContent = currentTenant.contactName;
    document.getElementById('contactPhone').textContent = currentTenant.contactPhone;
    document.getElementById('region').textContent = currentTenant.region;
    document.getElementById('createTime').textContent = currentTenant.createTime;
    
    // 更新状态标签
    const statusBadge = document.querySelector('.status-badge');
    if (statusBadge) {
        statusBadge.className = `status-badge status-${currentTenant.status}`;
        statusBadge.textContent = currentTenant.status === 'active' ? '正常' : '停用';
    }
    
    // 更新人员列表
    updateStaffTable();
}

// Tab切换
function switchTab(tabName) {
    // 移除所有active类
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // 添加active类到当前tab
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

// 编辑基本信息
function editBasicInfo() {
    if (!currentTenant) return;
    
    // 填充表单数据
    document.getElementById('editCompanyName').value = currentTenant.companyName;
    document.getElementById('editCompanyType').value = currentTenant.companyType;
    document.getElementById('editContactName').value = currentTenant.contactName;
    document.getElementById('editContactPhone').value = currentTenant.contactPhone;
    document.getElementById('editRegion').value = currentTenant.region;
    
    // 显示抽屉
    showDrawer('basicInfoDrawer');
}

// 保存基本信息
function saveBasicInfo() {
    const form = document.getElementById('basicInfoForm');
    const formData = new FormData(form);
    
    // 验证表单
    if (!validateForm(form)) {
        return;
    }
    
    // 显示加载状态
    const saveBtn = document.querySelector('#basicInfoDrawer .btn-primary');
    const originalText = saveBtn.textContent;
    saveBtn.textContent = '保存中...';
    saveBtn.disabled = true;
    
    // 模拟API调用
    setTimeout(() => {
        // 更新数据
        currentTenant.companyName = formData.get('companyName');
        currentTenant.companyType = formData.get('companyType');
        currentTenant.contactName = formData.get('contactName');
        currentTenant.contactPhone = formData.get('contactPhone');
        currentTenant.region = formData.get('region');
        
        // 更新页面显示
        updatePageData();
        
        // 关闭抽屉
        closeDrawer('basicInfoDrawer');
        
        // 显示成功消息
        showNotification('基本信息更新成功', 'success');
        
        // 恢复按钮状态
        saveBtn.textContent = originalText;
        saveBtn.disabled = false;
    }, 1000);
}

// 变更套餐
function changePlan() {
    console.log('变更套餐');
    
    showCustomDrawer('变更套餐', `
        <div class="package-selection">
            <div class="current-package">
                <h5>当前套餐</h5>
                <div class="package-info">
                    <span class="package-name">${currentTenant.package.type}</span>
                    <span class="package-price">¥${currentTenant.package.price}/年</span>
                </div>
            </div>
            
            <div class="package-options">
                <h5>选择新套餐</h5>
                <div class="package-option" data-package="basic">
                    <input type="radio" name="newPackage" value="basic" id="basic" ${currentTenant.package.type === '基础版' ? 'checked' : ''}>
                    <label for="basic">
                        <div class="package-header">
                            <span class="package-title">基础版</span>
                            <span class="package-price">¥1,999/年</span>
                        </div>
                        <div class="package-features">
                            <p>• 基础审核功能</p>
                            <p>• 数据存储 10GB</p>
                            <p>• 用户数量 50人</p>
                            <p>• 基础报表</p>
                        </div>
                    </label>
                </div>
                
                <div class="package-option" data-package="standard">
                    <input type="radio" name="newPackage" value="standard" id="standard" ${currentTenant.package.type === '标准版' ? 'checked' : ''}>
                    <label for="standard">
                        <div class="package-header">
                            <span class="package-title">标准版</span>
                            <span class="package-price">¥2,999/年</span>
                        </div>
                        <div class="package-features">
                            <p>• 智能审核功能</p>
                            <p>• 数据分析</p>
                            <p>• 报表生成</p>
                            <p>• 用户数量 200人</p>
                        </div>
                    </label>
                </div>
                
                <div class="package-option" data-package="enterprise">
                    <input type="radio" name="newPackage" value="enterprise" id="enterprise" ${currentTenant.package.type === '企业版' ? 'checked' : ''}>
                    <label for="enterprise">
                        <div class="package-header">
                            <span class="package-title">企业版</span>
                            <span class="package-price">¥4,999/年</span>
                        </div>
                        <div class="package-features">
                            <p>• 全部标准版功能</p>
                            <p>• 高级分析</p>
                            <p>• API接口</p>
                            <p>• 定制开发</p>
                            <p>• 无限用户账号</p>
                        </div>
                    </label>
                </div>
            </div>
            
            <div class="form-group">
                <label for="effectiveDate">生效日期</label>
                <input type="date" id="effectiveDate" name="effectiveDate" required>
            </div>
            
            <div class="form-group">
                <label for="contractPeriod">合同期限</label>
                <select id="contractPeriod" name="contractPeriod" required>
                    <option value="">请选择合同期限</option>
                    <option value="3">3个月</option>
                    <option value="6">6个月</option>
                    <option value="12">12个月</option>
                    <option value="24">24个月</option>
                    <option value="36">36个月</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="remark">备注</label>
                <textarea id="remark" name="remark" rows="3" placeholder="请输入变更原因或备注信息"></textarea>
            </div>
        </div>
    `, () => {
        console.log('取消变更套餐');
    }, () => {
        const selectedPackage = document.querySelector('input[name="newPackage"]:checked');
        const effectiveDate = document.getElementById('effectiveDate').value;
        const contractPeriod = document.getElementById('contractPeriod').value;
        
        if (!selectedPackage) {
            showNotification('请选择新套餐', 'error');
            return false;
        }
        
        if (!effectiveDate) {
            showNotification('请选择生效日期', 'error');
            return false;
        }
        
        if (!contractPeriod) {
            showNotification('请选择合同期限', 'error');
            return false;
        }
        
        // 模拟API调用
        return new Promise((resolve) => {
            setTimeout(() => {
                const packageNames = {
                    'basic': '基础版',
                    'standard': '标准版',
                    'enterprise': '企业版'
                };
                const packagePrices = {
                    'basic': 1999,
                    'standard': 2999,
                    'enterprise': 4999
                };
                
                currentTenant.package.type = packageNames[selectedPackage.value];
                currentTenant.package.price = packagePrices[selectedPackage.value];
                updatePageData();
                showNotification('套餐变更成功', 'success');
                console.log('确认变更套餐:', selectedPackage.value);
                resolve();
            }, 1500);
        });
    });
    
    // 设置默认日期为明天
    setTimeout(() => {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        const effectiveDateInput = document.getElementById('effectiveDate');
        if (effectiveDateInput) {
            effectiveDateInput.value = tomorrow.toISOString().split('T')[0];
        }
    }, 100);
}

// 添加人员
function addStaff() {
    console.log('添加人员');
    
    showCustomDrawer(
        '添加人员',
        `
        <div class="drawer-form">
            <div class="form-group">
                <label for="staffName">姓名 <span class="required">*</span></label>
                <input type="text" id="staffName" name="name" required>
                <div class="field-error" id="staffNameError"></div>
            </div>
            <div class="form-group">
                <label for="staffPhone">手机号 <span class="required">*</span></label>
                <input type="tel" id="staffPhone" name="phone" required>
                <div class="field-error" id="staffPhoneError"></div>
            </div>
            <div class="form-group">
                <label for="staffEmail">邮箱 <span class="required">*</span></label>
                <input type="email" id="staffEmail" name="email" required>
                <div class="field-error" id="staffEmailError"></div>
            </div>
            <div class="form-group">
                <label for="staffRole">角色 <span class="required">*</span></label>
                <select id="staffRole" name="role" required>
                    <option value="">请选择角色</option>
                    <option value="admin">管理员</option>
                    <option value="operator">操作员</option>
                    <option value="auditor">审核员</option>
                    <option value="viewer">查看员</option>
                </select>
                <div class="field-error" id="staffRoleError"></div>
            </div>
            <div class="form-group">
                <label for="staffDepartment">部门 <span class="required">*</span></label>
                <input type="text" id="staffDepartment" name="department" required>
                <div class="field-error" id="staffDepartmentError"></div>
            </div>
            <div class="form-group">
                <label for="staffStatus">状态 <span class="required">*</span></label>
                <select id="staffStatus" name="status" required>
                    <option value="active">正常</option>
                    <option value="inactive">停用</option>
                </select>
            </div>
            <div class="form-group">
                <label for="staffRemark">备注</label>
                <textarea id="staffRemark" name="remark" rows="3" placeholder="请输入备注信息"></textarea>
            </div>
        </div>
        `,
        () => {
            console.log('取消添加人员');
        },
        () => {
            const form = document.querySelector('.drawer-form');
            if (validateStaffForm(form)) {
                const formData = new FormData(form);
                
                // 模拟API调用
                setTimeout(() => {
                    const newStaff = {
                        id: Date.now(),
                        name: formData.get('name'),
                        phone: formData.get('phone'),
                        email: formData.get('email'),
                        role: formData.get('role'),
                        department: formData.get('department'),
                        status: formData.get('status'),
                        remark: formData.get('remark')
                    };
                    
                    currentTenant.staff.push(newStaff);
                    updateStaffTable();
                    showNotification('人员添加成功', 'success');
                    console.log('添加人员成功:', newStaff);
                }, 1000);
                
                return true;
            }
            return false;
        }
    );
}

// 编辑人员
function editStaff(staffId) {
    const staff = currentTenant.staff.find(s => s.id == staffId);
    if (!staff) {
        showNotification('未找到人员信息', 'error');
        return;
    }
    
    console.log('编辑人员:', staff);
    
    showCustomDrawer(
        '编辑人员',
        `
        <div class="drawer-form">
            <div class="form-group">
                <label for="editStaffName">姓名 <span class="required">*</span></label>
                <input type="text" id="editStaffName" name="name" value="${staff.name}" required>
                <div class="field-error" id="editStaffNameError"></div>
            </div>
            <div class="form-group">
                <label for="editStaffPhone">手机号 <span class="required">*</span></label>
                <input type="tel" id="editStaffPhone" name="phone" value="${staff.phone}" required>
                <div class="field-error" id="editStaffPhoneError"></div>
            </div>
            <div class="form-group">
                <label for="editStaffEmail">邮箱 <span class="required">*</span></label>
                <input type="email" id="editStaffEmail" name="email" value="${staff.email}" required>
                <div class="field-error" id="editStaffEmailError"></div>
            </div>
            <div class="form-group">
                <label for="editStaffRole">角色 <span class="required">*</span></label>
                <select id="editStaffRole" name="role" required>
                    <option value="admin" ${staff.role === 'admin' ? 'selected' : ''}>管理员</option>
                    <option value="operator" ${staff.role === 'operator' ? 'selected' : ''}>操作员</option>
                    <option value="auditor" ${staff.role === 'auditor' ? 'selected' : ''}>审核员</option>
                    <option value="viewer" ${staff.role === 'viewer' ? 'selected' : ''}>查看员</option>
                </select>
                <div class="field-error" id="editStaffRoleError"></div>
            </div>
            <div class="form-group">
                <label for="editStaffDepartment">部门 <span class="required">*</span></label>
                <input type="text" id="editStaffDepartment" name="department" value="${staff.department}" required>
                <div class="field-error" id="editStaffDepartmentError"></div>
            </div>
            <div class="form-group">
                <label for="editStaffStatus">状态 <span class="required">*</span></label>
                <select id="editStaffStatus" name="status" required>
                    <option value="active" ${staff.status === 'active' ? 'selected' : ''}>正常</option>
                    <option value="inactive" ${staff.status === 'inactive' ? 'selected' : ''}>停用</option>
                </select>
            </div>
            <div class="form-group">
                <label for="editStaffRemark">备注</label>
                <textarea id="editStaffRemark" name="remark" rows="3" placeholder="请输入备注信息">${staff.remark || ''}</textarea>
            </div>
        </div>
        `,
        () => {
            console.log('取消编辑人员');
        },
        () => {
            const form = document.querySelector('.drawer-form');
            if (validateStaffForm(form)) {
                const formData = new FormData(form);
                
                // 模拟API调用
                setTimeout(() => {
                    staff.name = formData.get('name');
                    staff.phone = formData.get('phone');
                    staff.email = formData.get('email');
                    staff.role = formData.get('role');
                    staff.department = formData.get('department');
                    staff.status = formData.get('status');
                    staff.remark = formData.get('remark');
                    
                    updateStaffTable();
                    showNotification('人员信息更新成功', 'success');
                    console.log('编辑人员成功:', staff);
                }, 1000);
                
                return true;
            }
            return false;
        }
    );
}

// 删除人员
function deleteStaff(staffId) {
    if (confirm('确定要删除这个人员吗？')) {
        showNotification(`删除人员 ${staffId} 功能开发中`, 'info');
    }
}

// 更新人员表格
function updateStaffTable() {
    if (!currentTenant || !currentTenant.staff) return;
    
    const tbody = document.getElementById('staffTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    currentTenant.staff.forEach(staff => {
        const row = document.createElement('tr');
        const roleText = {
            'admin': '管理员',
            'operator': '操作员', 
            'auditor': '审核员',
            'viewer': '查看员'
        }[staff.role] || staff.role;
        
        row.innerHTML = `
            <td>${staff.name}</td>
            <td>${staff.phone}</td>
            <td>${staff.email}</td>
            <td><span class="role-badge ${staff.role}">${roleText}</span></td>
            <td>${staff.department}</td>
            <td><span class="status-badge status-${staff.status}">${staff.status === 'active' ? '正常' : '停用'}</span></td>
            <td>
                <button class="btn-link" onclick="editStaff(${staff.id})">编辑</button>
                <button class="btn-link text-danger" onclick="deleteStaff(${staff.id})">删除</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// 编辑联系信息
function editContactInfo() {
    console.log('编辑联系信息');
    
    showCustomDrawer(
        '编辑联系信息',
        `
        <div class="drawer-form">
            <div class="form-section">
                <h4>主要联系人</h4>
                <div class="form-grid">
                    <div class="form-group">
                        <label for="contactName">姓名 <span class="required">*</span></label>
                        <input type="text" id="contactName" name="contactName" value="${currentTenant.contact.primaryContact.name}" required>
                        <div class="field-error" id="contactNameError"></div>
                    </div>
                    <div class="form-group">
                        <label for="contactPosition">职位 <span class="required">*</span></label>
                        <input type="text" id="contactPosition" name="contactPosition" value="${currentTenant.contact.primaryContact.position}" required>
                        <div class="field-error" id="contactPositionError"></div>
                    </div>
                    <div class="form-group">
                        <label for="contactPhone">手机号 <span class="required">*</span></label>
                        <input type="tel" id="contactPhone" name="contactPhone" value="${currentTenant.contact.primaryContact.phone}" required>
                        <div class="field-error" id="contactPhoneError"></div>
                    </div>
                    <div class="form-group">
                        <label for="contactEmail">邮箱 <span class="required">*</span></label>
                        <input type="email" id="contactEmail" name="contactEmail" value="${currentTenant.contact.primaryContact.email}" required>
                        <div class="field-error" id="contactEmailError"></div>
                    </div>
                </div>
            </div>
            <div class="form-section">
                <h4>企业地址</h4>
                <div class="form-grid">
                    <div class="form-group">
                        <label for="addressRegion">地区 <span class="required">*</span></label>
                        <input type="text" id="addressRegion" name="addressRegion" value="${currentTenant.contact.address.region}" required>
                        <div class="field-error" id="addressRegionError"></div>
                    </div>
                    <div class="form-group">
                        <label for="addressDetail">详细地址 <span class="required">*</span></label>
                        <input type="text" id="addressDetail" name="addressDetail" value="${currentTenant.contact.address.detail}" required>
                        <div class="field-error" id="addressDetailError"></div>
                    </div>
                    <div class="form-group">
                        <label for="addressPostcode">邮政编码</label>
                        <input type="text" id="addressPostcode" name="addressPostcode" value="${currentTenant.contact.address.postcode}">
                        <div class="field-error" id="addressPostcodeError"></div>
                    </div>
                </div>
            </div>
        </div>
        `,
        () => {
            console.log('取消编辑联系信息');
        },
        () => {
            const form = document.querySelector('.drawer-form');
            if (validateContactForm(form)) {
                const formData = new FormData(form);
                
                // 模拟API调用
                setTimeout(() => {
                    currentTenant.contact.primaryContact.name = formData.get('contactName');
                    currentTenant.contact.primaryContact.position = formData.get('contactPosition');
                    currentTenant.contact.primaryContact.phone = formData.get('contactPhone');
                    currentTenant.contact.primaryContact.email = formData.get('contactEmail');
                    
                    currentTenant.contact.address.region = formData.get('addressRegion');
                    currentTenant.contact.address.detail = formData.get('addressDetail');
                    currentTenant.contact.address.postcode = formData.get('addressPostcode');
                    
                    updatePageData();
                    showNotification('联系信息更新成功', 'success');
                    console.log('联系信息更新成功');
                }, 1000);
                
                return true;
            }
            return false;
        }
    );
}

// 修改状态
function changeStatus() {
    console.log('修改企业状态');
    
    const currentStatus = currentTenant.status;
    const newStatus = currentStatus === 'active' ? 'inactive' : 'active';
    const statusText = newStatus === 'active' ? '启用' : '停用';
    
    // 显示自定义确认弹窗
    showStatusConfirmModal(
        '确认操作',
        `确定要${statusText}该企业吗？`,
        () => {
            console.log('取消修改状态');
        },
        () => {
            // 显示加载状态
            const statusBtn = document.querySelector('.status-btn');
            const originalText = statusBtn.textContent;
            statusBtn.textContent = '处理中...';
            statusBtn.disabled = true;
            
            // 模拟API调用
            setTimeout(() => {
                currentTenant.status = newStatus;
                
                // 更新页面显示
                updatePageData();
                
                // 恢复按钮状态
                statusBtn.textContent = originalText;
                statusBtn.disabled = false;
                
                // 显示成功消息
                showNotification(`企业${statusText}成功`, 'success');
                console.log(`企业状态修改为: ${newStatus}`);
            }, 1500);
        }
    );
}

// 显示状态确认弹窗
function showStatusConfirmModal(title, message, onCancel, onConfirm) {
    const modal = document.getElementById('statusConfirmModal');
    const titleElement = modal.querySelector('.modal-title');
    const messageElement = modal.querySelector('.modal-message');
    const cancelBtn = modal.querySelector('.btn-cancel');
    const confirmBtn = modal.querySelector('.btn-confirm');
    
    titleElement.textContent = title;
    messageElement.textContent = message;
    
    // 绑定事件
    cancelBtn.onclick = () => {
        closeStatusConfirmModal();
        if (onCancel) onCancel();
    };
    
    confirmBtn.onclick = () => {
        closeStatusConfirmModal();
        if (onConfirm) onConfirm();
    };
    
    // 显示弹窗
    modal.style.display = 'flex';
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
}

// 关闭状态确认弹窗
function closeStatusConfirmModal() {
    const modal = document.getElementById('statusConfirmModal');
    modal.classList.remove('show');
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
}

// 删除企业
function deleteTenant() {
    if (confirm('确定要删除这个企业吗？删除后无法恢复！')) {
        if (confirm('请再次确认删除操作，此操作不可逆！')) {
            // 模拟API调用
            setTimeout(() => {
                showNotification('企业删除成功', 'success');
                // 跳转回列表页
                setTimeout(() => {
                    window.location.href = 'tenant-list.html';
                }, 1500);
            }, 1000);
        }
    }
}

// 显示抽屉
function showDrawer(drawerId) {
    const drawer = document.getElementById(drawerId);
    if (drawer) {
        drawer.style.display = 'flex';
        setTimeout(() => {
            drawer.classList.add('show');
        }, 10);
    }
}

// 关闭抽屉
function closeDrawer(drawerId) {
    const drawer = document.getElementById(drawerId);
    if (drawer) {
        drawer.classList.remove('show');
        setTimeout(() => {
            drawer.style.display = 'none';
        }, 300);
    }
}

// 关闭所有抽屉
function closeAllDrawers() {
    const drawers = document.querySelectorAll('.drawer-overlay');
    drawers.forEach(drawer => {
        drawer.classList.remove('show');
    });
    document.body.style.overflow = '';
}

// 表单验证
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, '此字段为必填项');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    return isValid;
}

// 显示字段错误
function showFieldError(field, message) {
    clearFieldError(field);
    
    field.style.borderColor = '#dc3545';
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.style.color = '#dc3545';
    errorDiv.style.fontSize = '12px';
    errorDiv.style.marginTop = '4px';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

// 清除字段错误
function clearFieldError(field) {
    field.style.borderColor = '';
    
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// 显示通知
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 6px;
        color: white;
        font-weight: 500;
        z-index: 9999;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    // 设置背景色
    switch (type) {
        case 'success':
            notification.style.backgroundColor = '#28a745';
            break;
        case 'error':
            notification.style.backgroundColor = '#dc3545';
            break;
        case 'warning':
            notification.style.backgroundColor = '#ffc107';
            notification.style.color = '#212529';
            break;
        default:
            notification.style.backgroundColor = '#007bff';
    }
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // 显示动画
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // 自动隐藏
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// 工具函数：格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// 工具函数：格式化金额
function formatCurrency(amount) {
    return new Intl.NumberFormat('zh-CN', {
        style: 'currency',
        currency: 'CNY'
    }).format(amount);
}

// 显示自定义抽屉
function showCustomDrawer(title, content, onCancel, onConfirm) {
    const drawerId = 'customDrawer';
    let drawer = document.getElementById(drawerId);
    
    if (!drawer) {
        drawer = document.createElement('div');
        drawer.id = drawerId;
        drawer.className = 'drawer-overlay';
        document.body.appendChild(drawer);
    }
    
    drawer.innerHTML = `
        <div class="drawer-container">
            <div class="drawer-header">
                <h3>${title}</h3>
                <button class="drawer-close" onclick="closeDrawer('${drawerId}')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="drawer-content">
                ${content}
            </div>
            <div class="drawer-footer">
                <button type="button" class="btn btn-secondary" id="drawerCancelBtn">取消</button>
                <button type="button" class="btn btn-primary" id="drawerConfirmBtn">确认</button>
            </div>
        </div>
    `;
    
    // 绑定事件
    const cancelBtn = drawer.querySelector('#drawerCancelBtn');
    const confirmBtn = drawer.querySelector('#drawerConfirmBtn');
    
    cancelBtn.addEventListener('click', () => {
        closeDrawer(drawerId);
        if (onCancel) onCancel();
    });
    
    confirmBtn.addEventListener('click', () => {
        if (onConfirm) {
            const originalText = confirmBtn.textContent;
            confirmBtn.textContent = '处理中...';
            confirmBtn.disabled = true;
            
            const result = onConfirm();
            
            // 如果返回Promise，等待完成
            if (result && typeof result.then === 'function') {
                result.then(() => {
                    closeDrawer(drawerId);
                }).catch(() => {
                    confirmBtn.textContent = originalText;
                    confirmBtn.disabled = false;
                });
            } else {
                // 延迟关闭抽屉，让用户看到处理状态
                setTimeout(() => {
                    closeDrawer(drawerId);
                }, 1500);
            }
        }
    });
    
    drawer.classList.add('show');
    document.body.style.overflow = 'hidden';
}

// 验证人员表单
function validateStaffForm(form) {
    const requiredFields = ['name', 'phone', 'email', 'role', 'department'];
    let isValid = true;
    
    // 清除之前的错误
    form.querySelectorAll('.field-error').forEach(error => {
        error.textContent = '';
    });
    
    requiredFields.forEach(fieldName => {
        const field = form.querySelector(`[name="${fieldName}"]`);
        const errorElement = form.querySelector(`#${field.id}Error`) || form.querySelector(`#edit${field.id.charAt(0).toUpperCase() + field.id.slice(1)}Error`);
        
        if (!field || !field.value.trim()) {
            if (errorElement) {
                errorElement.textContent = '此字段为必填项';
                errorElement.style.color = '#dc3545';
                errorElement.style.fontSize = '12px';
                errorElement.style.marginTop = '4px';
            }
            field.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            if (errorElement) {
                errorElement.textContent = '';
            }
            field.style.borderColor = '';
        }
    });
    
    // 验证手机号格式
    const phoneField = form.querySelector('[name="phone"]');
    if (phoneField && phoneField.value.trim()) {
        const phoneRegex = /^1[3-9]\d{9}$/;
        if (!phoneRegex.test(phoneField.value.trim())) {
            const errorElement = form.querySelector(`#${phoneField.id}Error`);
            if (errorElement) {
                errorElement.textContent = '请输入正确的手机号格式';
                errorElement.style.color = '#dc3545';
            }
            phoneField.style.borderColor = '#dc3545';
            isValid = false;
        }
    }
    
    // 验证邮箱格式
    const emailField = form.querySelector('[name="email"]');
    if (emailField && emailField.value.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailField.value.trim())) {
            const errorElement = form.querySelector(`#${emailField.id}Error`);
            if (errorElement) {
                errorElement.textContent = '请输入正确的邮箱格式';
                errorElement.style.color = '#dc3545';
            }
            emailField.style.borderColor = '#dc3545';
            isValid = false;
        }
    }
    
    return isValid;
}

// 验证联系信息表单
function validateContactForm(form) {
    const requiredFields = ['contactName', 'contactPosition', 'contactPhone', 'contactEmail', 'addressRegion', 'addressDetail'];
    let isValid = true;
    
    // 清除之前的错误
    form.querySelectorAll('.field-error').forEach(error => {
        error.textContent = '';
    });
    
    requiredFields.forEach(fieldName => {
        const field = form.querySelector(`[name="${fieldName}"]`);
        const errorElement = form.querySelector(`#${fieldName}Error`);
        
        if (!field || !field.value.trim()) {
            if (errorElement) {
                errorElement.textContent = '此字段为必填项';
                errorElement.style.color = '#dc3545';
                errorElement.style.fontSize = '12px';
                errorElement.style.marginTop = '4px';
            }
            field.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            if (errorElement) {
                errorElement.textContent = '';
            }
            field.style.borderColor = '';
        }
    });
    
    // 验证手机号格式
    const phoneField = form.querySelector('[name="contactPhone"]');
    if (phoneField && phoneField.value.trim()) {
        const phoneRegex = /^1[3-9]\d{9}$/;
        if (!phoneRegex.test(phoneField.value.trim())) {
            const errorElement = form.querySelector('#contactPhoneError');
            if (errorElement) {
                errorElement.textContent = '请输入正确的手机号格式';
                errorElement.style.color = '#dc3545';
            }
            phoneField.style.borderColor = '#dc3545';
            isValid = false;
        }
    }
    
    // 验证邮箱格式
    const emailField = form.querySelector('[name="contactEmail"]');
    if (emailField && emailField.value.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailField.value.trim())) {
            const errorElement = form.querySelector('#contactEmailError');
            if (errorElement) {
                errorElement.textContent = '请输入正确的邮箱格式';
                errorElement.style.color = '#dc3545';
            }
            emailField.style.borderColor = '#dc3545';
            isValid = false;
        }
    }
    
    return isValid;
}