/**
 * 规则参数配置管理
 */
class RuleParametersManager {
    constructor() {
        this.currentTab = 'basic';
        this.parameters = {};
        this.init();
    }

    /**
     * 初始化
     */
    init() {
        this.loadParameters();
        this.bindEvents();
        this.renderParameterTabs();
        this.renderParameters();
    }

    /**
     * 绑定事件
     */
    bindEvents() {
        // 保存全部按钮
        document.getElementById('saveAllParamsBtn')?.addEventListener('click', () => {
            this.saveAllParameters();
        });

        // 恢复默认按钮
        document.getElementById('resetDefaultBtn')?.addEventListener('click', () => {
            this.resetToDefault();
        });

        // 标签页切换
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('nav-tab')) {
                const tabId = e.target.dataset.tab;
                this.switchTab(tabId);
            }
        });

        // 参数值变化监听
        document.addEventListener('input', (e) => {
            if (e.target.classList.contains('param-input')) {
                this.updateParameter(e.target);
            }
        });

        // 开关切换
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('param-toggle')) {
                this.toggleParameter(e.target);
            }
        });
    }

    /**
     * 加载参数配置
     */
    loadParameters() {
        // 模拟从后端加载参数配置
        this.parameters = {
            basic: {
                title: '基础参数',
                groups: [
                    {
                        title: '审核阈值设置',
                        params: [
                            {
                                key: 'audit_threshold',
                                label: '审核阈值',
                                description: '超过此金额的医疗费用将触发人工审核',
                                type: 'number',
                                value: 5000,
                                unit: '元',
                                min: 1000,
                                max: 50000
                            },
                            {
                                key: 'auto_approve_limit',
                                label: '自动通过限额',
                                description: '低于此金额的费用可自动通过审核',
                                type: 'number',
                                value: 1000,
                                unit: '元',
                                min: 100,
                                max: 5000
                            },
                            {
                                key: 'risk_score_threshold',
                                label: '风险评分阈值',
                                description: '超过此评分的案例将被标记为高风险',
                                type: 'range',
                                value: 75,
                                unit: '分',
                                min: 0,
                                max: 100
                            }
                        ]
                    },
                    {
                        title: '时间设置',
                        params: [
                            {
                                key: 'audit_timeout',
                                label: '审核超时时间',
                                description: '审核任务的最大处理时间',
                                type: 'number',
                                value: 24,
                                unit: '小时',
                                min: 1,
                                max: 168
                            },
                            {
                                key: 'auto_close_days',
                                label: '自动关闭天数',
                                description: '超过指定天数未处理的任务将自动关闭',
                                type: 'number',
                                value: 7,
                                unit: '天',
                                min: 1,
                                max: 30
                            }
                        ]
                    }
                ]
            },
            advanced: {
                title: '高级参数',
                groups: [
                    {
                        title: '算法参数',
                        params: [
                            {
                                key: 'ml_confidence_threshold',
                                label: 'AI置信度阈值',
                                description: 'AI模型预测结果的最低置信度要求',
                                type: 'range',
                                value: 85,
                                unit: '%',
                                min: 50,
                                max: 99
                            },
                            {
                                key: 'anomaly_detection_sensitivity',
                                label: '异常检测敏感度',
                                description: '异常行为检测的敏感程度',
                                type: 'range',
                                value: 70,
                                unit: '%',
                                min: 10,
                                max: 100
                            }
                        ]
                    },
                    {
                        title: '系统开关',
                        params: [
                            {
                                key: 'enable_auto_audit',
                                label: '启用自动审核',
                                description: '是否启用AI自动审核功能',
                                type: 'toggle',
                                value: true
                            },
                            {
                                key: 'enable_real_time_monitor',
                                label: '启用实时监控',
                                description: '是否启用实时费用监控',
                                type: 'toggle',
                                value: true
                            },
                            {
                                key: 'enable_smart_alert',
                                label: '启用智能预警',
                                description: '是否启用基于AI的智能预警系统',
                                type: 'toggle',
                                value: false
                            }
                        ]
                    }
                ]
            },
            notification: {
                title: '通知设置',
                groups: [
                    {
                        title: '邮件通知',
                        params: [
                            {
                                key: 'email_notification',
                                label: '启用邮件通知',
                                description: '是否发送邮件通知',
                                type: 'toggle',
                                value: true
                            },
                            {
                                key: 'email_frequency',
                                label: '邮件发送频率',
                                description: '邮件通知的发送频率',
                                type: 'select',
                                value: 'daily',
                                options: [
                                    { value: 'realtime', label: '实时' },
                                    { value: 'hourly', label: '每小时' },
                                    { value: 'daily', label: '每日' },
                                    { value: 'weekly', label: '每周' }
                                ]
                            }
                        ]
                    },
                    {
                        title: '短信通知',
                        params: [
                            {
                                key: 'sms_notification',
                                label: '启用短信通知',
                                description: '是否发送短信通知',
                                type: 'toggle',
                                value: false
                            },
                            {
                                key: 'sms_urgent_only',
                                label: '仅紧急情况',
                                description: '仅在紧急情况下发送短信',
                                type: 'toggle',
                                value: true
                            }
                        ]
                    }
                ]
            }
        };
    }

    /**
     * 渲染参数标签页
     */
    renderParameterTabs() {
        const tabsContainer = document.querySelector('.params-nav');
        if (!tabsContainer) return;

        const tabs = Object.keys(this.parameters).map(key => {
            const config = this.parameters[key];
            return `
                <div class="nav-tab ${key === this.currentTab ? 'active' : ''}" data-tab="${key}">
                    ${config.title}
                </div>
            `;
        }).join('');

        tabsContainer.innerHTML = tabs;
    }

    /**
     * 切换标签页
     */
    switchTab(tabId) {
        this.currentTab = tabId;
        
        // 更新标签页状态
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabId);
        });

        // 渲染参数内容
        this.renderParameters();
    }

    /**
     * 渲染参数内容
     */
    renderParameters() {
        const panelContainer = document.querySelector('.params-panel');
        if (!panelContainer) return;

        const config = this.parameters[this.currentTab];
        if (!config) return;

        const content = config.groups.map(group => {
            const params = group.params.map(param => this.renderParameter(param)).join('');
            return `
                <div class="param-group">
                    <div class="group-title">${group.title}</div>
                    ${params}
                </div>
            `;
        }).join('');

        panelContainer.innerHTML = content;
    }

    /**
     * 渲染单个参数
     */
    renderParameter(param) {
        let control = '';
        
        switch (param.type) {
            case 'number':
                control = `
                    <input type="number" class="param-input" 
                           data-key="${param.key}" 
                           value="${param.value}" 
                           min="${param.min}" 
                           max="${param.max}">
                    <span class="param-unit">${param.unit}</span>
                `;
                break;
                
            case 'range':
                control = `
                    <input type="range" class="param-range" 
                           data-key="${param.key}" 
                           value="${param.value}" 
                           min="${param.min}" 
                           max="${param.max}">
                    <span class="param-unit">${param.value}${param.unit}</span>
                `;
                break;
                
            case 'toggle':
                control = `
                    <div class="param-toggle ${param.value ? 'active' : ''}" 
                         data-key="${param.key}" 
                         data-value="${param.value}"></div>
                `;
                break;
                
            case 'select':
                const options = param.options.map(opt => 
                    `<option value="${opt.value}" ${opt.value === param.value ? 'selected' : ''}>${opt.label}</option>`
                ).join('');
                control = `
                    <select class="param-input" data-key="${param.key}">
                        ${options}
                    </select>
                `;
                break;
        }

        return `
            <div class="param-item">
                <div class="param-info">
                    <div class="param-label">${param.label}</div>
                    <div class="param-description">${param.description}</div>
                </div>
                <div class="param-control">
                    ${control}
                </div>
            </div>
        `;
    }

    /**
     * 更新参数值
     */
    updateParameter(input) {
        const key = input.dataset.key;
        const value = input.type === 'number' ? parseFloat(input.value) : input.value;
        
        // 更新内存中的参数值
        this.updateParameterValue(key, value);
        
        // 如果是范围滑块，更新显示值
        if (input.type === 'range') {
            const unitSpan = input.nextElementSibling;
            if (unitSpan) {
                const param = this.findParameter(key);
                unitSpan.textContent = `${value}${param?.unit || ''}`;
            }
        }
    }

    /**
     * 切换开关参数
     */
    toggleParameter(toggle) {
        const key = toggle.dataset.key;
        const currentValue = toggle.dataset.value === 'true';
        const newValue = !currentValue;
        
        toggle.classList.toggle('active', newValue);
        toggle.dataset.value = newValue;
        
        this.updateParameterValue(key, newValue);
    }

    /**
     * 更新参数值到内存
     */
    updateParameterValue(key, value) {
        // 遍历所有分组查找参数
        Object.values(this.parameters).forEach(tab => {
            tab.groups.forEach(group => {
                const param = group.params.find(p => p.key === key);
                if (param) {
                    param.value = value;
                }
            });
        });
    }

    /**
     * 查找参数配置
     */
    findParameter(key) {
        for (const tab of Object.values(this.parameters)) {
            for (const group of tab.groups) {
                const param = group.params.find(p => p.key === key);
                if (param) return param;
            }
        }
        return null;
    }

    /**
     * 保存所有参数
     */
    async saveAllParameters() {
        try {
            // 收集所有参数值
            const allParams = {};
            Object.values(this.parameters).forEach(tab => {
                tab.groups.forEach(group => {
                    group.params.forEach(param => {
                        allParams[param.key] = param.value;
                    });
                });
            });

            // 模拟API调用
            await this.simulateApiCall('/api/rule-parameters', 'POST', allParams);
            
            this.showSaveStatus('参数保存成功', 'success');
        } catch (error) {
            console.error('保存参数失败:', error);
            this.showSaveStatus('参数保存失败', 'error');
        }
    }

    /**
     * 恢复默认设置
     */
    async resetToDefault() {
        if (!confirm('确定要恢复所有参数到默认值吗？此操作不可撤销。')) {
            return;
        }

        try {
            // 模拟API调用获取默认值
            await this.simulateApiCall('/api/rule-parameters/default', 'POST');
            
            // 重新加载参数
            this.loadParameters();
            this.renderParameters();
            
            this.showSaveStatus('已恢复默认设置', 'success');
        } catch (error) {
            console.error('恢复默认设置失败:', error);
            this.showSaveStatus('恢复默认设置失败', 'error');
        }
    }

    /**
     * 显示保存状态
     */
    showSaveStatus(message, type) {
        // 移除现有的状态提示
        const existingStatus = document.querySelector('.save-status');
        if (existingStatus) {
            existingStatus.remove();
        }

        // 创建新的状态提示
        const statusDiv = document.createElement('div');
        statusDiv.className = `save-status ${type}`;
        statusDiv.textContent = message;
        document.body.appendChild(statusDiv);

        // 显示动画
        setTimeout(() => statusDiv.classList.add('show'), 100);
        
        // 3秒后隐藏
        setTimeout(() => {
            statusDiv.classList.remove('show');
            setTimeout(() => statusDiv.remove(), 300);
        }, 3000);
    }

    /**
     * 模拟API调用
     */
    simulateApiCall(url, method, data = null) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                // 模拟90%的成功率
                if (Math.random() > 0.1) {
                    resolve({ success: true, data });
                } else {
                    reject(new Error('网络错误'));
                }
            }, 1000);
        });
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new RuleParametersManager();
});