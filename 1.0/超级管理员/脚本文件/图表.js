// 图表初始化管理器
class ChartManager {
    constructor() {
        this.charts = {};
        this.initializeCharts();
    }

    // 初始化所有图表
    initializeCharts() {
        // 等待DOM加载完成
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.setupCharts();
            });
        } else {
            this.setupCharts();
        }
    }

    // 设置所有图表
    setupCharts() {
        // 延迟执行，确保组件已加载
        setTimeout(() => {
            this.initTenantGrowthChart();
            this.initTenantTypeChart();
            this.initRevenueChart();
            this.initActivityChart();
            this.initActivityHeatmap();
        }, 500);
    }

    // 租户增长趋势图表
    initTenantGrowthChart() {
        const canvas = document.getElementById('tenantGrowthChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        this.charts.tenantGrowth = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['1月', '2月', '3月', '4月', '5月', '6月', '7月'],
                datasets: [{
                    label: '新增租户',
                    data: [12, 15, 8, 22, 18, 25, 20],
                    borderColor: '#4ecdc4',
                    backgroundColor: 'rgba(78, 205, 196, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#4ecdc4',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5
                }, {
                    label: '流失租户',
                    data: [2, 3, 1, 4, 2, 3, 2],
                    borderColor: '#ff6b6b',
                    backgroundColor: 'rgba(255, 107, 107, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#ff6b6b',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: '#ddd',
                        borderWidth: 1
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        },
                        ticks: {
                            color: '#666'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        },
                        ticks: {
                            color: '#666'
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

    // 租户类型分布图表
    initTenantTypeChart() {
        const canvas = document.getElementById('tenantTypeChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        this.charts.tenantType = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['三甲医院', '二甲医院', '专科医院', '医保机构', '其他'],
                datasets: [{
                    data: [68, 52, 24, 12, 8],
                    backgroundColor: [
                        '#4ecdc4',
                        '#45b7d1',
                        '#f9ca24',
                        '#a55eea',
                        '#fd79a8'
                    ],
                    borderWidth: 3,
                    borderColor: '#fff',
                    hoverBorderWidth: 4,
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: '#ddd',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                            }
                        }
                    }
                },
                cutout: '60%',
                animation: {
                    animateRotate: true,
                    duration: 1000
                }
            }
        });
    }

    // 月度收入趋势图表
    initRevenueChart() {
        const canvas = document.getElementById('revenueChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        this.charts.revenue = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
                datasets: [{
                    label: '订阅收入',
                    data: [1800000, 1950000, 2100000, 2200000, 2150000, 2300000, 2250000, 2400000, 2350000, 2500000, 2450000, 2340000],
                    backgroundColor: '#4ecdc4',
                    borderRadius: 4,
                    borderSkipped: false
                }, {
                    label: '使用量收入',
                    data: [300000, 320000, 350000, 380000, 360000, 400000, 390000, 420000, 410000, 450000, 440000, 430000],
                    backgroundColor: '#45b7d1',
                    borderRadius: 4,
                    borderSkipped: false
                }, {
                    label: '增值服务',
                    data: [150000, 160000, 180000, 200000, 190000, 220000, 210000, 240000, 230000, 260000, 250000, 240000],
                    backgroundColor: '#f9ca24',
                    borderRadius: 4,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: '#ddd',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ¥' + context.parsed.y.toLocaleString();
                            },
                            footer: function(tooltipItems) {
                                let total = 0;
                                tooltipItems.forEach(function(tooltipItem) {
                                    total += tooltipItem.parsed.y;
                                });
                                return '总计: ¥' + total.toLocaleString();
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        stacked: true,
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#666'
                        }
                    },
                    y: {
                        stacked: true,
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        },
                        ticks: {
                            color: '#666',
                            callback: function(value) {
                                return '¥' + (value / 1000000).toFixed(1) + 'M';
                            }
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

    // 租户活跃度图表
    initActivityChart() {
        const canvas = document.getElementById('activityChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        this.charts.activity = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['第1周', '第2周', '第3周', '第4周'],
                datasets: [{
                    label: '活跃租户数',
                    data: [135, 138, 140, 142],
                    borderColor: '#4ecdc4',
                    backgroundColor: 'rgba(78, 205, 196, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#4ecdc4',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }, {
                    label: '新增活跃租户',
                    data: [8, 5, 7, 6],
                    borderColor: '#45b7d1',
                    backgroundColor: 'rgba(69, 183, 209, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#45b7d1',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }, {
                    label: '流失活跃租户',
                    data: [2, 3, 1, 2],
                    borderColor: '#ff6b6b',
                    backgroundColor: 'rgba(255, 107, 107, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#ff6b6b',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: '#ddd',
                        borderWidth: 1
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        },
                        ticks: {
                            color: '#666'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        },
                        ticks: {
                            color: '#666'
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

    // 初始化活跃度热力图
    initActivityHeatmap() {
        const container = document.querySelector('.heatmap-grid');
        if (!container) return;

        // 生成过去35天的热力图数据（确保能填满5周）
        const today = new Date();
        const heatmapData = [];
        
        // 计算开始日期，确保从周日开始
        const startDate = new Date(today);
        startDate.setDate(today.getDate() - 34); // 过去35天
        
        // 找到最近的周日作为起始点
        const dayOfWeek = startDate.getDay();
        startDate.setDate(startDate.getDate() - dayOfWeek);
        
        for (let i = 0; i < 35; i++) {
            const date = new Date(startDate);
            date.setDate(startDate.getDate() + i);
            
            // 模拟活跃度数据 (0-100)
            const activity = Math.floor(Math.random() * 100);
            const level = Math.floor(activity / 20); // 0-5 levels
            
            heatmapData.push({
                date: date,
                activity: activity,
                level: Math.min(level, 5)
            });
        }

        // 清空容器
        container.innerHTML = '';

        // 生成热力图单元格
        heatmapData.forEach((data, index) => {
            const cell = document.createElement('div');
            cell.className = `heatmap-cell level-${data.level}`;
            
            // 格式化日期显示
            const month = data.date.getMonth() + 1;
            const day = data.date.getDate();
            const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
            const weekday = weekdays[data.date.getDay()];
            
            cell.title = `${month}月${day}日 ${weekday}\n活跃度: ${data.activity}%`;
            
            // 添加日期显示（只显示日期数字）
            cell.textContent = day;
            
            // 添加点击事件
            cell.addEventListener('click', () => {
                this.showHeatmapDetail(data);
            });
            
            container.appendChild(cell);
        });
    }

    // 显示热力图详情
    showHeatmapDetail(data) {
        // 这里可以显示详细信息的模态框
        console.log('热力图详情:', {
            date: data.date.toLocaleDateString(),
            activity: data.activity + '%',
            level: data.level
        });
    }

    // 刷新图表数据
    refreshCharts() {
        Object.values(this.charts).forEach(chart => {
            if (chart) {
                chart.update();
            }
        });
        // 重新生成热力图
        this.initActivityHeatmap();
    }

    // 销毁图表
    destroyCharts() {
        Object.values(this.charts).forEach(chart => {
            if (chart) {
                chart.destroy();
            }
        });
        this.charts = {};
    }
}

// 全局图表管理器实例
window.chartManager = new ChartManager();

// 添加时间筛选器事件监听
document.addEventListener('DOMContentLoaded', function() {
    // 时间筛选按钮事件
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('filter-btn')) {
            // 移除所有活跃状态
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // 添加当前按钮的活跃状态
            e.target.classList.add('active');
            
            // 获取选中的时间段
            const period = e.target.getAttribute('data-period');
            
            // 刷新图表数据（这里可以根据时间段加载不同的数据）
            if (window.chartManager) {
                window.chartManager.refreshCharts();
            }
        }
    });
});