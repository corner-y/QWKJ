// 医保智能审核系统 - 租户表单JavaScript

// 全局变量
let currentStep = 1;
let totalSteps = 2;
let formData = {};

// 页面初始化
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
});

function initializePage() {
    console.log('=== TENANT FORM 页面初始化 ===');
    
    // 初始化表单
    initializeForm();
    
    // 初始化步骤指示器
    updateStepIndicator();
    
    // 初始化套餐选择
    initializePlanSelection();
    
    // 设置默认日期
    setDefaultDates();
    
    // 绑定表单提交事件
    bindFormEvents();
}

function initializeForm() {
    // 显示第一步
    showStep(1);
    
    // 初始化省市联动
    initializeCityData();
    
    // 初始化表单验证
    initializeValidation();
}

function bindFormEvents() {
    const form = document.getElementById('tenantForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmit();
        });
    }
}

// 步骤控制
function nextStep() {
    if (validateCurrentStep()) {
        if (currentStep < totalSteps) {
            currentStep++;
            showStep(currentStep);
            updateStepIndicator();
            
            // 如果是第二步，更新确认信息
            if (currentStep === 2) {
                updateConfirmationData();
            }
        }
    }
}

function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
        updateStepIndicator();
    }
}

function showStep(step) {
    // 隐藏所有步骤
    for (let i = 1; i <= totalSteps; i++) {
        const stepElement = document.getElementById(`step${i}`);
        if (stepElement) {
            stepElement.style.display = 'none';
        }
    }
    
    // 显示当前步骤
    const currentStepElement = document.getElementById(`step${step}`);
    if (currentStepElement) {
        currentStepElement.style.display = 'block';
    }
}

function updateStepIndicator() {
    const steps = document.querySelectorAll('.progress-step');
    steps.forEach((step, index) => {
        const stepNumber = index + 1;
        if (stepNumber < currentStep) {
            step.classList.add('completed');
            step.classList.remove('active');
        } else if (stepNumber === currentStep) {
            step.classList.add('active');
            step.classList.remove('completed');
        } else {
            step.classList.remove('active', 'completed');
        }
    });
}

// 表单验证
function validateCurrentStep() {
    console.log(`验证第 ${currentStep} 步`);
    
    let isValid = true;
    
    if (currentStep === 1) {
        // 验证基本信息
        const requiredFields = ['companyName', 'companyType', 'contactName', 'contactPhone', 'region'];
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (!validateField(field)) {
                isValid = false;
            }
        });
        
        // 验证手机号格式
        const phone = document.getElementById('contactPhone');
        if (phone && phone.value && !isValidPhone(phone.value)) {
            showFieldError(phone, '请输入正确的手机号格式');
            isValid = false;
        }
    }
    
    return isValid;
}

function validateField(field) {
    const value = field.value.trim();
    const fieldType = field.type;
    const fieldName = field.name || field.id;
    
    // 清除之前的错误状态
    field.classList.remove('error');
    
    if (field.hasAttribute('required') && !value) {
        field.classList.add('error');
        showFieldError(field, '此字段为必填项');
        return false;
    }
    
    // 特殊字段验证
    switch (fieldType) {
        case 'email':
            if (value && !isValidEmail(value)) {
                field.classList.add('error');
                showFieldError(field, '请输入有效的邮箱地址');
                return false;
            }
            break;
        case 'tel':
            if (value && !isValidPhone(value)) {
                field.classList.add('error');
                showFieldError(field, '请输入有效的手机号码');
                return false;
            }
            break;
    }
    
    // 统一社会信用代码验证
    if (fieldName === 'creditCode' && value) {
        if (!isValidCreditCode(value)) {
            field.classList.add('error');
            showFieldError(field, '请输入有效的18位统一社会信用代码');
            return false;
        }
    }
    
    return true;
}

function showFieldError(field, message) {
    // 移除之前的错误提示
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    
    // 添加新的错误提示
    const errorEl = document.createElement('div');
    errorEl.className = 'field-error';
    errorEl.textContent = message;
    field.parentNode.appendChild(errorEl);
    
    // 3秒后自动移除
    setTimeout(() => {
        if (errorEl.parentNode) {
            errorEl.remove();
        }
    }, 3000);
}

// 工具函数
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhone(phone) {
    const phoneRegex = /^1[3-9]\d{9}$/;
    return phoneRegex.test(phone);
}

function isValidCreditCode(code) {
    const creditCodeRegex = /^[0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}$/;
    return creditCodeRegex.test(code) && code.length === 18;
}

// 省市联动
function initializeCityData() {
    // 省市数据
    window.cityData = {
        'beijing': ['北京市'],
        'shanghai': ['上海市'],
        'guangdong': ['广州市', '深圳市', '珠海市', '佛山市', '东莞市', '中山市'],
        'zhejiang': ['杭州市', '宁波市', '温州市', '嘉兴市', '湖州市', '绍兴市'],
        'jiangsu': ['南京市', '苏州市', '无锡市', '常州市', '镇江市', '南通市'],
        'sichuan': ['成都市', '绵阳市', '德阳市', '南充市', '宜宾市', '自贡市']
    };
}

function updateCities() {
    const provinceSelect = document.getElementById('province');
    const citySelect = document.getElementById('city');
    const districtSelect = document.getElementById('district');
    
    if (!provinceSelect || !citySelect) return;
    
    const selectedProvince = provinceSelect.value;
    
    // 清空城市和区县选项
    citySelect.innerHTML = '<option value="">请选择城市</option>';
    districtSelect.innerHTML = '<option value="">请选择区县</option>';
    
    if (selectedProvince && window.cityData[selectedProvince]) {
        window.cityData[selectedProvince].forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });
    }
}

function updateTypeFields() {
    const typeSelect = document.getElementById('tenantType');
    const levelSelect = document.getElementById('hospitalLevel');
    
    if (!typeSelect || !levelSelect) return;
    
    const selectedType = typeSelect.value;
    
    // 根据机构类型显示/隐藏相关字段
    if (selectedType === 'insurance' || selectedType === 'clinic') {
        levelSelect.disabled = true;
        levelSelect.value = '';
    } else {
        levelSelect.disabled = false;
    }
}

// 管理员账号管理
function addAdminAccount() {
    adminAccountCount++;
    
    const adminAccountsContainer = document.querySelector('.admin-accounts');
    const newAccountHtml = `
        <div class="admin-account" id="adminAccount${adminAccountCount}">
            <div class="account-header">
                <h5>管理员账号 #${adminAccountCount}</h5>
                <button type="button" class="btn btn-sm btn-danger" onclick="removeAdminAccount(${adminAccountCount})">删除</button>
            </div>
            <div class="form-grid">
                <div class="form-group">
                    <label class="required">用户名</label>
                    <input type="text" class="form-input" name="adminUsername${adminAccountCount}" placeholder="请输入用户名" required>
                    <div class="form-help">用于登录系统的用户名</div>
                </div>
                <div class="form-group">
                    <label class="required">姓名</label>
                    <input type="text" class="form-input" name="adminName${adminAccountCount}" placeholder="请输入真实姓名" required>
                </div>
                <div class="form-group">
                    <label class="required">手机号</label>
                    <input type="tel" class="form-input" name="adminPhone${adminAccountCount}" placeholder="请输入手机号" required>
                </div>
                <div class="form-group">
                    <label class="required">邮箱</label>
                    <input type="email" class="form-input" name="adminEmail${adminAccountCount}" placeholder="请输入邮箱" required>
                </div>
                <div class="form-group">
                    <label class="required">角色</label>
                    <select class="form-select" name="adminRole${adminAccountCount}" required>
                        <option value="">请选择角色</option>
                        <option value="超级管理员">超级管理员</option>
                        <option value="admin">管理员</option>
                        <option value="operator">操作员</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>部门</label>
                    <input type="text" class="form-input" name="adminDepartment${adminAccountCount}" placeholder="请输入所属部门">
                </div>
            </div>
        </div>
    `;
    
    adminAccountsContainer.insertAdjacentHTML('beforeend', newAccountHtml);
    
    // 显示第一个账号的删除按钮
    const firstAccountDeleteBtn = document.querySelector('#adminAccount1 .btn-danger');
    if (firstAccountDeleteBtn) {
        firstAccountDeleteBtn.style.display = 'inline-block';
    }
}

function removeAdminAccount(accountId) {
    const accountElement = document.getElementById(`adminAccount${accountId}`);
    if (accountElement) {
        accountElement.remove();
        adminAccountCount--;
        
        // 如果只剩一个账号，隐藏删除按钮
        if (adminAccountCount === 1) {
            const firstAccountDeleteBtn = document.querySelector('#adminAccount1 .btn-danger');
            if (firstAccountDeleteBtn) {
                firstAccountDeleteBtn.style.display = 'none';
            }
        }
    }
}

// 套餐选择
function initializePlanSelection() {
    const planCards = document.querySelectorAll('.plan-card');
    const planRadios = document.querySelectorAll('input[name="planType"]');
    
    planCards.forEach(card => {
        card.addEventListener('click', function() {
            const planType = this.dataset.plan;
            const radio = document.getElementById(`plan${planType.charAt(0).toUpperCase() + planType.slice(1)}`);
            if (radio) {
                radio.checked = true;
                updatePlanSelection();
            }
        });
    });
    
    planRadios.forEach(radio => {
        radio.addEventListener('change', updatePlanSelection);
    });
}

function updatePlanSelection() {
    const selectedPlan = document.querySelector('input[name="planType"]:checked');
    const planCards = document.querySelectorAll('.plan-card');
    
    planCards.forEach(card => {
        card.classList.remove('selected');
    });
    
    if (selectedPlan) {
        const selectedCard = document.querySelector(`[data-plan="${selectedPlan.value}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }
    }
}

// 设置默认日期
function setDefaultDates() {
    const serviceStartDate = document.getElementById('serviceStartDate');
    if (serviceStartDate) {
        // 设置为明天
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        serviceStartDate.value = tomorrow.toISOString().split('T')[0];
    }
}

// 确认信息更新
function updateConfirmationData() {
    console.log('更新确认信息');
    
    // 基本信息
    updateConfirmField('companyName', 'confirmCompanyName');
    updateConfirmField('companyType', 'confirmCompanyType', getTypeText);
    updateConfirmField('contactName', 'confirmContactName');
    updateConfirmField('contactPhone', 'confirmContactPhone');
    updateConfirmField('region', 'confirmRegion', getOptionText);
}

function updateConfirmField(sourceId, targetId, textTransform = null) {
    const sourceEl = document.getElementById(sourceId);
    const targetEl = document.getElementById(targetId);
    
    if (sourceEl && targetEl) {
        let value = sourceEl.value;
        if (textTransform) {
            value = textTransform(sourceEl);
        }
        targetEl.textContent = value || '-';
    }
}

function getOptionText(selectElement) {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    return selectedOption ? selectedOption.textContent : '';
}

function getTypeText(selectElement) {
    const typeTexts = {
        'level3': '三甲医院',
        'level2': '二甲医院',
        'level1': '一甲医院',
        'specialist': '专科医院',
        'insurance': '医保机构',
        'clinic': '诊所',
        'other': '其他'
    };
    return typeTexts[selectElement.value] || '';
}

function getPeriodText(selectElement) {
    const periodTexts = {
        '3': '3个月',
        '6': '6个月',
        '12': '1年',
        '24': '2年',
        '36': '3年'
    };
    return periodTexts[selectElement.value] || '';
}

function updateAdminAccountsSummary() {
    const container = document.getElementById('confirmAdminAccounts');
    if (!container) return;
    
    let html = '';
    for (let i = 1; i <= adminAccountCount; i++) {
        const accountEl = document.getElementById(`adminAccount${i}`);
        if (!accountEl) continue;
        
        const username = accountEl.querySelector(`[name="adminUsername${i}"]`)?.value || '';
        const name = accountEl.querySelector(`[name="adminName${i}"]`)?.value || '';
        const role = accountEl.querySelector(`[name="adminRole${i}"]`)?.value || '';
        
        const roleTexts = {
            '超级管理员': '超级管理员',
            'admin': '管理员',
            'operator': '操作员'
        };
        
        if (username || name) {
            html += `
                <div class="admin-summary-item">
                    <strong>${name || username}</strong> (${username}) - ${roleTexts[role] || role}
                </div>
            `;
        }
    }
    
    container.innerHTML = html || '<div class="admin-summary-item">暂无管理员账号</div>';
}

function updateModulesSummary() {
    const container = document.getElementById('confirmModules');
    if (!container) return;
    
    const checkedModules = document.querySelectorAll('input[name="modules"]:checked');
    const moduleTexts = {
        'pre_audit': '事前审核',
        'in_process_audit': '事中审核',
        'post_audit': '事后审核',
        'user_management': '用户管理',
        'rule_management': '规则管理',
        'knowledge_base': '知识库管理',
        'basic_reports': '基础报表',
        'advanced_analytics': '高级分析',
        'custom_reports': '自定义报表'
    };
    
    let html = '';
    checkedModules.forEach(module => {
        html += `<span class="module-tag">${moduleTexts[module.value] || module.value}</span>`;
    });
    
    container.innerHTML = html || '<span class="module-tag">暂无选择模块</span>';
}

// 创建企业函数
function createTenant() {
    console.log('创建企业');
    
    // 收集表单数据
    const data = collectFormData();
    
    // 显示加载状态
    showNotification('正在创建企业...', 'info');
    
    // 模拟API调用
    setTimeout(() => {
        console.log('提交的数据:', data);
        showNotification('企业创建成功！', 'success');
        
        // 3秒后跳转到租户列表
        setTimeout(() => {
            window.location.href = 'tenant-list.html';
        }, 3000);
    }, 2000);
}

// 表单提交
function handleFormSubmit() {
    console.log('处理表单提交');
    createTenant();
}

function collectFormData() {
    const data = {
        // 基本信息
        companyName: document.getElementById('companyName')?.value || '',
        companyType: document.getElementById('companyType')?.value || '',
        contactName: document.getElementById('contactName')?.value || '',
        contactPhone: document.getElementById('contactPhone')?.value || '',
        region: document.getElementById('region')?.value || '',
        
        // 创建时间
        createTime: new Date().toISOString()
    };
    
    return data;
}

// 其他功能
function goBack() {
    window.location.href = 'tenant-list.html';
}

function saveDraft() {
    const formData = collectFormData();
    localStorage.setItem('tenantFormDraft', JSON.stringify(formData));
    showNotification('草稿已保存', 'success');
}

function submitForm() {
    const form = document.getElementById('tenantForm');
    if (form) {
        form.dispatchEvent(new Event('submit'));
    }
}

// 弹窗功能
function showTerms() {
    const modal = document.getElementById('termsModal');
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeTermsModal() {
    const modal = document.getElementById('termsModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function showPrivacy() {
    const modal = document.getElementById('privacyModal');
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closePrivacyModal() {
    const modal = document.getElementById('privacyModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// 表单验证初始化
function initializeValidation() {
    const inputs = document.querySelectorAll('.form-input, .form-select');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            // 清除错误状态
            this.classList.remove('error');
            const errorEl = this.parentNode.querySelector('.field-error');
            if (errorEl) {
                errorEl.remove();
            }
        });
    });
}

// 通知功能
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">&times;</button>
        </div>
    `;
    
    // 添加到页面
    document.body.appendChild(notification);
    
    // 自动移除
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

console.log('=== TENANT FORM JavaScript 加载完成 ===');