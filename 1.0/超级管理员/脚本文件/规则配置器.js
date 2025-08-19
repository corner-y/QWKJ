/**
 * 规则配置中心 JavaScript 功能
 */

class RuleConfigurator {
    constructor() {
        this.rules = this.generateMockRules();
        this.departments = ['cardiology', 'orthopedics', 'neurosurgery', 'emergency'];
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadRuleMatrix();
    }

    // 绑定事件
    bindEvents() {
        // 批量配置按钮
        document.getElementById('batchConfigBtn')?.addEventListener('click', () => {
            this.showBatchConfigModal();
        });

        // 导出配置按钮
        document.getElementById('exportConfigBtn')?.addEventListener('click', () => {
            this.exportConfiguration();
        });

        // 保存全部按钮
        document.getElementById('saveAllBtn')?.addEventListener('click', () => {
            this.saveAllConfiguration();
        });

        // 搜索按钮
        document.getElementById('searchBtn')?.addEventListener('click', () => {
            this.searchRules();
        });

        // 筛选器变化
        ['ruleCategory', 'ruleScene', 'ruleStatus'].forEach(id => {
            document.getElementById(id)?.addEventListener('change', () => {
                this.filterRules();
            });
        });

        // 搜索框回车
        document.getElementById('searchRule')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchRules();
            }
        });
    }

    // 生成模拟规则数据
    generateMockRules() {
        return {
            drug: {
                policy: [
                    { id: 'drug-catalog-check', name: '医保目录准入检查', desc: '检查药品是否在国家医保目录范围内', enabled: { cardiology: true, orthopedics: true, neurosurgery: true, emergency: false } },
                    { id: 'drug-reimbursement-ratio', name: '药品报销比例检查', desc: '验证药品报销比例是否符合政策规定', enabled: { cardiology: true, orthopedics: false, neurosurgery: true, emergency: true } },
                    { id: 'special-drug-approval', name: '特殊药品审批检查', desc: '检查特殊药品是否有相应审批手续', enabled: { cardiology: false, orthopedics: true, neurosurgery: true, emergency: false } },
                    { id: 'drug-price-limit', name: '药品价格限制检查', desc: '验证药品价格是否超出限定标准', enabled: { cardiology: true, orthopedics: true, neurosurgery: false, emergency: true } },
                    { id: 'drug-category-limit', name: '药品类别限制检查', desc: '检查药品类别使用是否符合规定', enabled: { cardiology: true, orthopedics: true, neurosurgery: true, emergency: true } }
                ],
                regulation: [
                    { id: 'drug-dosage-limit', name: '药品用量限制', desc: '检查单次和总用药量是否超标', enabled: { cardiology: true, orthopedics: false, neurosurgery: true, emergency: false } },
                    { id: 'drug-frequency-limit', name: '用药频次限制', desc: '验证用药频次是否符合规定', enabled: { cardiology: false, orthopedics: true, neurosurgery: true, emergency: true } },
                    { id: 'drug-duration-limit', name: '用药疗程限制', desc: '检查用药疗程是否超出限定时间', enabled: { cardiology: true, orthopedics: true, neurosurgery: false, emergency: true } },
                    { id: 'drug-combination-check', name: '药品配伍检查', desc: '验证药品配伍使用的合理性', enabled: { cardiology: true, orthopedics: false, neurosurgery: true, emergency: false } }
                ],
                clinical: [
                    { id: 'drug-interaction', name: '药物相互作用检查', desc: '检查药物间是否存在不良相互作用', enabled: { cardiology: true, orthopedics: true, neurosurgery: true, emergency: false } },
                    { id: 'drug-contraindication', name: '药物禁忌症检查', desc: '验证患者是否存在用药禁忌症', enabled: { cardiology: false, orthopedics: true, neurosurgery: false, emergency: true } },
                    { id: 'drug-allergy-check', name: '药物过敏史检查', desc: '检查患者药物过敏史记录', enabled: { cardiology: true, orthopedics: false, neurosurgery: true, emergency: true } }
                ]
            },
            treatment: {
                policy: [
                    { id: 'treatment-catalog-check', name: '诊疗目录准入检查', desc: '检查诊疗项目是否在医保目录内', enabled: { cardiology: true, orthopedics: true, neurosurgery: false, emergency: true } },
                    { id: 'treatment-reimbursement', name: '诊疗报销比例检查', desc: '验证诊疗项目报销比例', enabled: { cardiology: false, orthopedics: true, neurosurgery: true, emergency: false } },
                    { id: 'treatment-approval', name: '诊疗项目审批检查', desc: '检查特殊诊疗项目审批手续', enabled: { cardiology: true, orthopedics: false, neurosurgery: true, emergency: true } }
                ],
                regulation: [
                    { id: 'treatment-frequency-limit', name: '诊疗频次限制', desc: '检查诊疗项目使用频次', enabled: { cardiology: true, orthopedics: true, neurosurgery: false, emergency: false } },
                    { id: 'treatment-indication', name: '诊疗适应症检查', desc: '验证诊疗项目适应症', enabled: { cardiology: false, orthopedics: false, neurosurgery: true, emergency: true } }
                ],
                clinical: [
                    { id: 'treatment-necessity', name: '诊疗必要性评估', desc: '评估诊疗项目的临床必要性', enabled: { cardiology: true, orthopedics: true, neurosurgery: true, emergency: false } },
                    { id: 'treatment-sequence', name: '诊疗顺序检查', desc: '检查诊疗项目执行顺序', enabled: { cardiology: false, orthopedics: true, neurosurgery: false, emergency: true } }
                ]
            },
            material: {
                policy: [
                    { id: 'material-catalog-check', name: '耗材目录准入检查', desc: '检查耗材是否在医保目录内', enabled: { cardiology: true, orthopedics: false, neurosurgery: true, emergency: false } },
                    { id: 'material-price-limit', name: '耗材价格限制', desc: '验证耗材价格是否超标', enabled: { cardiology: false, orthopedics: true, neurosurgery: false, emergency: true } }
                ],
                regulation: [
                    { id: 'material-quantity-limit', name: '耗材用量限制', desc: '检查耗材使用量是否合理', enabled: { cardiology: true, orthopedics: true, neurosurgery: true, emergency: false } },
                    { id: 'material-specification', name: '耗材规格检查', desc: '验证耗材规格是否符合要求', enabled: { cardiology: false, orthopedics: false, neurosurgery: true, emergency: true } }
                ],
                clinical: [
                    { id: 'material-indication', name: '耗材适应症检查', desc: '检查耗材使用适应症', enabled: { cardiology: true, orthopedics: true, neurosurgery: false, emergency: false } },
                    { id: 'material-compatibility', name: '耗材兼容性检查', desc: '验证耗材与设备的兼容性', enabled: { cardiology: false, orthopedics: true, neurosurgery: true, emergency: true } }
                ]
            }
        };
    }

    // 加载规则矩阵
    loadRuleMatrix() {
        // 这里可以添加动态加载逻辑
        console.log('规则矩阵已加载');
    }

    // 切换规则组展开/收起
    toggleGroup(groupId) {
        const groupRules = document.querySelector(`[data-group="${groupId}"]`);
        const toggleBtn = document.querySelector(`[onclick="toggleGroup('${groupId}')"]`);
        
        if (groupRules && toggleBtn) {
            const isExpanded = groupRules.style.display !== 'none';
            groupRules.style.display = isExpanded ? 'none' : 'block';
            toggleBtn.textContent = isExpanded ? '+' : '-';
        }
    }

    // 切换科室全选
    toggleDepartmentAll(deptId) {
        const switches = document.querySelectorAll(`[data-dept="${deptId}"] .rule-switch`);
        const allEnabled = Array.from(switches).every(sw => sw.checked);
        
        switches.forEach(sw => {
            sw.checked = !allEnabled;
            this.updateRuleStatus(sw.dataset.rule, deptId, !allEnabled);
        });
        
        this.updateStatistics();
    }

    // 切换规则组全选
    toggleGroupAll(groupId) {
        const switches = document.querySelectorAll(`[data-group="${groupId}"] .rule-switch`);
        const allEnabled = Array.from(switches).every(sw => sw.checked);
        
        switches.forEach(sw => {
            sw.checked = !allEnabled;
            const ruleId = sw.closest('.rule-row').dataset.rule;
            const deptId = sw.dataset.dept;
            this.updateRuleStatus(ruleId, deptId, !allEnabled);
        });
        
        this.updateStatistics();
    }

    // 更新规则状态
    updateRuleStatus(ruleId, deptId, enabled) {
        // 在实际应用中，这里会调用API更新后端数据
        console.log(`规则 ${ruleId} 在 ${deptId} 科室的状态更新为: ${enabled}`);
    }

    // 配置规则参数
    configureRule(ruleId) {
        const modal = document.getElementById('ruleParamsModal');
        const title = document.getElementById('modalTitle');
        const content = document.getElementById('modalContent');
        
        if (modal && title && content) {
            title.textContent = `配置规则参数 - ${ruleId}`;
            content.innerHTML = this.generateRuleParamsForm(ruleId);
            modal.style.display = 'block';
        }
    }

    // 查看规则详情
    viewRuleDetails(ruleId) {
        const modal = document.getElementById('ruleParamsModal');
        const title = document.getElementById('modalTitle');
        const content = document.getElementById('modalContent');
        
        if (modal && title && content) {
            title.textContent = `规则详情 - ${ruleId}`;
            content.innerHTML = this.generateRuleDetailsView(ruleId);
            modal.style.display = 'block';
        }
    }

    // 生成规则参数表单
    generateRuleParamsForm(ruleId) {
        return `
            <div class="param-form">
                <div class="form-group">
                    <label>阈值设置:</label>
                    <input type="number" class="form-control" placeholder="请输入阈值">
                </div>
                <div class="form-group">
                    <label>检查频率:</label>
                    <select class="form-control">
                        <option value="realtime">实时检查</option>
                        <option value="daily">每日检查</option>
                        <option value="weekly">每周检查</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>告警级别:</label>
                    <select class="form-control">
                        <option value="high">高风险</option>
                        <option value="medium">中风险</option>
                        <option value="low">低风险</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>备注说明:</label>
                    <textarea class="form-control" rows="3" placeholder="请输入备注信息"></textarea>
                </div>
            </div>
        `;
    }

    // 生成规则详情视图
    generateRuleDetailsView(ruleId) {
        return `
            <div class="rule-details">
                <div class="detail-item">
                    <label>规则ID:</label>
                    <span>${ruleId}</span>
                </div>
                <div class="detail-item">
                    <label>规则名称:</label>
                    <span>示例规则名称</span>
                </div>
                <div class="detail-item">
                    <label>规则描述:</label>
                    <span>这是一个示例规则的详细描述信息</span>
                </div>
                <div class="detail-item">
                    <label>适用场景:</label>
                    <span>事前审核、事中监控</span>
                </div>
                <div class="detail-item">
                    <label>风险级别:</label>
                    <span class="tag high-risk">高风险</span>
                </div>
                <div class="detail-item">
                    <label>创建时间:</label>
                    <span>2024-01-15 10:30:00</span>
                </div>
                <div class="detail-item">
                    <label>最后修改:</label>
                    <span>2024-01-20 14:25:00</span>
                </div>
            </div>
        `;
    }

    // 搜索规则
    searchRules() {
        const keyword = document.getElementById('searchRule')?.value.trim();
        if (!keyword) {
            this.showAllRules();
            return;
        }
        
        const ruleRows = document.querySelectorAll('.rule-row');
        ruleRows.forEach(row => {
            const ruleName = row.querySelector('.rule-name')?.textContent || '';
            const ruleDesc = row.querySelector('.rule-desc')?.textContent || '';
            const isMatch = ruleName.includes(keyword) || ruleDesc.includes(keyword);
            row.style.display = isMatch ? 'block' : 'none';
        });
    }

    // 显示所有规则
    showAllRules() {
        const ruleRows = document.querySelectorAll('.rule-row');
        ruleRows.forEach(row => {
            row.style.display = 'block';
        });
    }

    // 筛选规则
    filterRules() {
        const category = document.getElementById('ruleCategory')?.value;
        const scene = document.getElementById('ruleScene')?.value;
        const status = document.getElementById('ruleStatus')?.value;
        
        const ruleGroups = document.querySelectorAll('.rule-group');
        ruleGroups.forEach(group => {
            let shouldShow = true;
            
            if (category) {
                const groupType = group.querySelector('.group-header .group-name')?.textContent;
                shouldShow = shouldShow && groupType?.includes(category);
            }
            
            group.style.display = shouldShow ? 'block' : 'none';
        });
        
        // 根据场景和状态进一步筛选规则行
        const ruleRows = document.querySelectorAll('.rule-row');
        ruleRows.forEach(row => {
            let shouldShow = true;
            
            if (scene) {
                const sceneTags = row.querySelectorAll('.tag');
                const hasScene = Array.from(sceneTags).some(tag => 
                    tag.textContent.includes(scene.replace('-audit', '').replace('in-process', '事中'))
                );
                shouldShow = shouldShow && hasScene;
            }
            
            if (status) {
                const switches = row.querySelectorAll('.rule-switch');
                const isEnabled = Array.from(switches).some(sw => sw.checked);
                shouldShow = shouldShow && ((status === 'enabled' && isEnabled) || (status === 'disabled' && !isEnabled));
            }
            
            if (row.closest('.rule-group').style.display !== 'none') {
                row.style.display = shouldShow ? 'block' : 'none';
            }
        });
    }

    // 显示批量配置模态框
    showBatchConfigModal() {
        const modal = document.getElementById('ruleParamsModal');
        const title = document.getElementById('modalTitle');
        const content = document.getElementById('modalContent');
        
        if (modal && title && content) {
            title.textContent = '批量配置规则';
            content.innerHTML = `
                <div class="batch-config">
                    <div class="form-group">
                        <label>选择规则类型:</label>
                        <select class="form-control" id="batchRuleType">
                            <option value="">请选择规则类型</option>
                            <option value="drug">药品规则</option>
                            <option value="treatment">诊疗规则</option>
                            <option value="material">耗材规则</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>选择科室:</label>
                        <div class="checkbox-group">
                            <label><input type="checkbox" value="cardiology"> 心内科</label>
                            <label><input type="checkbox" value="orthopedics"> 骨科</label>
                            <label><input type="checkbox" value="neurosurgery"> 神经外科</label>
                            <label><input type="checkbox" value="emergency"> 急诊科</label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>批量操作:</label>
                        <div class="radio-group">
                            <label><input type="radio" name="batchAction" value="enable"> 启用选中规则</label>
                            <label><input type="radio" name="batchAction" value="disable"> 禁用选中规则</label>
                        </div>
                    </div>
                </div>
            `;
            modal.style.display = 'block';
        }
    }

    // 导出配置
    exportConfiguration() {
        const config = this.generateConfigurationData();
        const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `rule-config-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showMessage('配置导出成功', 'success');
    }

    // 生成配置数据
    generateConfigurationData() {
        const config = {
            exportTime: new Date().toISOString(),
            rules: {},
            statistics: this.getStatistics()
        };
        
        // 收集所有规则的配置状态
        const ruleRows = document.querySelectorAll('.rule-row');
        ruleRows.forEach(row => {
            const ruleId = row.dataset.rule;
            const switches = row.querySelectorAll('.rule-switch');
            config.rules[ruleId] = {};
            
            switches.forEach(sw => {
                const deptId = sw.dataset.dept;
                config.rules[ruleId][deptId] = sw.checked;
            });
        });
        
        return config;
    }

    // 保存全部配置
    saveAllConfiguration() {
        const config = this.generateConfigurationData();
        
        // 在实际应用中，这里会调用API保存到后端
        console.log('保存配置:', config);
        
        this.showMessage('配置保存成功', 'success');
    }

    // 更新统计信息
    updateStatistics() {
        const stats = this.getStatistics();
        
        document.getElementById('totalRules').textContent = stats.total;
        document.getElementById('enabledRules').textContent = stats.enabled;
        document.getElementById('disabledRules').textContent = stats.disabled;
        document.getElementById('coverageRate').textContent = stats.coverage + '%';
    }

    // 获取统计信息
    getStatistics() {
        const allSwitches = document.querySelectorAll('.rule-switch');
        const enabledSwitches = document.querySelectorAll('.rule-switch:checked');
        const totalRules = document.querySelectorAll('.rule-row').length;
        
        const enabled = enabledSwitches.length;
        const disabled = allSwitches.length - enabled;
        const coverage = totalRules > 0 ? Math.round((enabled / allSwitches.length) * 100) : 0;
        
        return {
            total: totalRules,
            enabled,
            disabled,
            coverage
        };
    }

    // 显示消息提示
    showMessage(message, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${type}`;
        messageDiv.textContent = message;
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
            color: white;
            border-radius: 4px;
            z-index: 10000;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        `;
        
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            document.body.removeChild(messageDiv);
        }, 3000);
    }

    // 关闭模态框
    closeModal() {
        const modal = document.getElementById('ruleParamsModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    // 保存模态框配置
    saveModalConfig() {
        // 在实际应用中，这里会收集表单数据并保存
        this.showMessage('参数配置保存成功', 'success');
        this.closeModal();
    }
}

// 全局函数，供HTML调用
function toggleGroup(groupId) {
    if (window.ruleConfigurator) {
        window.ruleConfigurator.toggleGroup(groupId);
    }
}

function toggleDepartmentAll(deptId) {
    if (window.ruleConfigurator) {
        window.ruleConfigurator.toggleDepartmentAll(deptId);
    }
}

function toggleGroupAll(groupId) {
    if (window.ruleConfigurator) {
        window.ruleConfigurator.toggleGroupAll(groupId);
    }
}

function configureRule(ruleId) {
    if (window.ruleConfigurator) {
        window.ruleConfigurator.configureRule(ruleId);
    }
}

function viewRuleDetails(ruleId) {
    if (window.ruleConfigurator) {
        window.ruleConfigurator.viewRuleDetails(ruleId);
    }
}

function closeModal() {
    if (window.ruleConfigurator) {
        window.ruleConfigurator.closeModal();
    }
}

function saveModalConfig() {
    if (window.ruleConfigurator) {
        window.ruleConfigurator.saveModalConfig();
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    window.ruleConfigurator = new RuleConfigurator();
    
    // 绑定规则开关变化事件
    document.addEventListener('change', (e) => {
        if (e.target.classList.contains('rule-switch')) {
            const ruleId = e.target.closest('.rule-row').dataset.rule;
            const deptId = e.target.dataset.dept;
            window.ruleConfigurator.updateRuleStatus(ruleId, deptId, e.target.checked);
            window.ruleConfigurator.updateStatistics();
        }
    });
    
    // 绑定模态框关闭事件
    document.addEventListener('click', (e) => {
        const modal = document.getElementById('ruleParamsModal');
        if (e.target === modal) {
            window.ruleConfigurator.closeModal();
        }
    });
});