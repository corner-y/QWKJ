/**
 * 平台运营看板组件管理器
 * 负责动态加载和管理各个组件模块
 */

class DashboardComponentManager {
    constructor() {
        this.components = {
            'metrics-overview': {
                container: 'metrics-overview-container',
                file: '../组件/_metrics-overview.html'
            },
            'tenant-analysis': {
                container: 'tenant-analysis-container',
                file: '../组件/_tenant-analysis.html'
            },
            'revenue-analysis': {
                container: 'revenue-analysis-container',
                file: '../组件/_revenue-analysis.html'
            },
            'system-monitoring': {
                container: 'system-monitoring-container',
                file: '../组件/_system-monitoring.html'
            },
            'tenant-activity': {
                container: 'tenant-activity-container',
                file: '../组件/_tenant-activity.html'
            },
            'operation-data': {
                container: 'operation-data-container',
                file: '../组件/_operation-data.html'
            },
            'settings-modal': {
                container: 'settings-modal-container',
                file: '../组件/_settings-modal.html'
            }
        };
        this.loadedComponents = new Set();
    }

    /**
     * 初始化所有组件
     */
    async init() {
        try {
            console.log('开始加载仪表板组件...');
            
            // 并行加载所有组件
            const loadPromises = Object.keys(this.components).map(componentName => 
                this.loadComponent(componentName)
            );
            
            await Promise.all(loadPromises);
            
            console.log('所有组件加载完成');
            
            // 初始化组件功能
            this.initializeComponentFunctions();
            
        } catch (error) {
            console.error('组件加载失败:', error);
        }
    }

    /**
     * 加载单个组件
     */
    async loadComponent(componentName) {
        const component = this.components[componentName];
        if (!component) {
            console.warn(`组件 ${componentName} 不存在`);
            return;
        }

        try {
            const response = await fetch(component.file);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const html = await response.text();
            const container = document.getElementById(component.container);
            
            if (container) {
                container.innerHTML = html;
                this.loadedComponents.add(componentName);
                console.log(`组件 ${componentName} 加载成功`);
            } else {
                console.warn(`容器 ${component.container} 不存在`);
            }
            
        } catch (error) {
            console.error(`加载组件 ${componentName} 失败:`, error);
        }
    }

    /**
     * 重新加载指定组件
     */
    async reloadComponent(componentName) {
        console.log(`重新加载组件: ${componentName}`);
        await this.loadComponent(componentName);
        
        // 重新初始化该组件的功能
        this.initializeSpecificComponent(componentName);
    }

    /**
     * 初始化组件功能
     */
    initializeComponentFunctions() {
        // 初始化核心指标
        if (this.loadedComponents.has('metrics-overview')) {
            this.initMetricsOverview();
        }
        
        // 初始化租户分析
        if (this.loadedComponents.has('tenant-analysis')) {
            this.initTenantAnalysis();
        }
        
        // 初始化收入分析
        if (this.loadedComponents.has('revenue-analysis')) {
            this.initRevenueAnalysis();
        }
        
        // 初始化系统监控
        if (this.loadedComponents.has('system-monitoring')) {
            this.initSystemMonitoring();
        }
        
        // 初始化租户活跃度
        if (this.loadedComponents.has('tenant-activity')) {
            this.initTenantActivity();
        }
        
        // 初始化运营数据
        if (this.loadedComponents.has('operation-data')) {
            this.initOperationData();
        }
        
        // 初始化设置弹窗
        if (this.loadedComponents.has('settings-modal')) {
            this.initSettingsModal();
        }
    }

    /**
     * 初始化特定组件功能
     */
    initializeSpecificComponent(componentName) {
        switch (componentName) {
            case 'metrics-overview':
                this.initMetricsOverview();
                break;
            case 'tenant-analysis':
                this.initTenantAnalysis();
                break;
            case 'revenue-analysis':
                this.initRevenueAnalysis();
                break;
            case 'system-monitoring':
                this.initSystemMonitoring();
                break;
            case 'tenant-activity':
                this.initTenantActivity();
                break;
            case 'operation-data':
                this.initOperationData();
                break;
            case 'settings-modal':
                this.initSettingsModal();
                break;
        }
    }

    // 各组件初始化方法
    initMetricsOverview() {
        console.log('初始化核心指标概览');
        // 这里可以添加图表初始化、事件绑定等逻辑
    }

    initTenantAnalysis() {
        console.log('初始化租户分析');
        
        // 初始化租户增长趋势折线图
        const growthCtx = document.getElementById('tenantGrowthChart');
        if (growthCtx) {
            new Chart(growthCtx, {
                type: 'line',
                data: {
                    labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
                    datasets: [{
                        label: '租户数量',
                        data: [120, 135, 142, 158, 167, 176],
                        borderColor: '#4ecdc4',
                        backgroundColor: 'rgba(78, 205, 196, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            grid: {
                                color: 'rgba(0,0,0,0.1)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        }
        
        // 初始化租户类型分布饼状图
        const typeCtx = document.getElementById('tenantTypeChart');
        if (typeCtx) {
            new Chart(typeCtx, {
                type: 'doughnut',
                data: {
                    labels: ['三甲医院', '二甲医院', '专科医院', '医保机构'],
                    datasets: [{
                        data: [68, 52, 24, 12],
                        backgroundColor: ['#4ecdc4', '#45b7d1', '#f9ca24', '#a55eea'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    cutout: '60%'
                }
            });
        }
    }

    initRevenueAnalysis() {
        console.log('初始化收入分析');
        
        // 初始化收入趋势折线图
        const revenueCtx = document.getElementById('revenueChart');
        if (revenueCtx) {
            new Chart(revenueCtx, {
                type: 'line',
                data: {
                    labels: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
                    datasets: [{
                        label: '总收入',
                        data: [1.8, 2.1, 1.9, 2.3, 2.5, 2.2, 2.4, 2.6, 2.3, 2.7, 2.4, 2.34],
                        borderColor: '#45b7d1',
                        backgroundColor: 'rgba(69, 183, 209, 0.1)',
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: '#45b7d1',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            grid: {
                                color: 'rgba(0,0,0,0.1)'
                            },
                            ticks: {
                                callback: function(value) {
                                    return '¥' + value + 'M';
                                }
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    }
                }
            });
        }
    }

    initSystemMonitoring() {
        console.log('初始化系统监控');
        // 初始化系统监控实时数据
    }

    initTenantActivity() {
        console.log('初始化租户活跃度');
        // 初始化活跃度热力图和活动图表
        if (window.chartManager) {
            window.chartManager.initActivityHeatmap();
            window.chartManager.initActivityChart();
        }
    }

    initOperationData() {
        console.log('初始化运营数据');
        // 初始化运营数据表格和统计
        
        // 调试：强制显示所有统计卡片
        setTimeout(() => {
            const statCards = document.querySelectorAll('.stat-card');
            console.log('找到统计卡片数量:', statCards.length);
            statCards.forEach((card, index) => {
                console.log(`卡片 ${index + 1}:`, card);
                card.style.display = 'block';
                card.style.visibility = 'visible';
                card.style.opacity = '1';
            });
            
            const statsGrid = document.querySelector('.stats-grid');
            if (statsGrid) {
                console.log('找到stats-grid:', statsGrid);
                statsGrid.style.display = 'flex';
                statsGrid.style.flexWrap = 'wrap';
            }
        }, 1000);
    }

    initSettingsModal() {
        console.log('初始化设置弹窗');
        // 初始化设置弹窗的标签页切换和表单处理
    }

    /**
     * 获取已加载的组件列表
     */
    getLoadedComponents() {
        return Array.from(this.loadedComponents);
    }

    /**
     * 检查组件是否已加载
     */
    isComponentLoaded(componentName) {
        return this.loadedComponents.has(componentName);
    }
}

// 全局组件管理器实例
window.dashboardManager = new DashboardComponentManager();

// 页面加载完成后初始化组件
document.addEventListener('DOMContentLoaded', function() {
    window.dashboardManager.init();
});

// 导出供其他脚本使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DashboardComponentManager;
}