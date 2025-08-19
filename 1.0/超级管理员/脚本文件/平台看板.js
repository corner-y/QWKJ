/**
 * 平台运营看板主要功能脚本
 * 处理菜单导航、页面交互等功能
 */

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('平台运营看板页面加载完成');
    
    // 初始化菜单导航
    initializeNavigation();
    
    // 初始化其他功能
    initializeOtherFeatures();
});

/**
 * 初始化导航菜单功能
 */
function initializeNavigation() {
    // 获取所有导航项
    const navItems = document.querySelectorAll('.nav-item');
    
    // 为每个导航项添加点击事件
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // 移除所有活动状态
            navItems.forEach(nav => nav.classList.remove('active'));
            
            // 添加当前项的活动状态
            this.classList.add('active');
            
            console.log('导航到:', this.textContent.trim());
        });
    });
    
    // 处理导航组的展开/收起
    const navGroups = document.querySelectorAll('.nav-group');
    navGroups.forEach(group => {
        const title = group.querySelector('.nav-group-title');
        if (title) {
            title.addEventListener('click', function() {
                group.classList.toggle('expanded');
            });
        }
    });
}

/**
 * 初始化其他功能
 */
function initializeOtherFeatures() {
    // 这里可以添加其他页面功能的初始化代码
    console.log('其他功能初始化完成');
}

/**
 * 显示设置弹窗
 */
function showSettings() {
    if (window.showModal) {
        window.showModal('settingsModal');
    }
}

/**
 * 切换数据时间段
 */
function switchDataPeriod(period, button) {
    // 移除所有按钮的活动状态
    document.querySelectorAll('.period-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 添加当前按钮的活动状态
    button.classList.add('active');
    
    console.log('切换数据时间段到:', period);
    
    // 这里可以添加重新加载数据的逻辑
    // updateOperationData(period);
}

/**
 * 切换租户分析时间范围
 */
function switchTenantAnalysisTime(days, button) {
    // 移除所有按钮的活动状态
    document.querySelectorAll('.time-filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 添加当前按钮的活动状态
    button.classList.add('active');
    
    console.log('切换租户分析时间范围到:', days + '天');
    
    // 这里可以添加重新加载图表数据的逻辑
    // updateTenantAnalysisChart(days);
}

/**
 * 刷新仪表板数据
 */
function refreshDashboard() {
    console.log('刷新仪表板数据...');
    
    // 显示加载状态
    const refreshBtn = document.querySelector('.btn-secondary');
    const originalText = refreshBtn.textContent;
    refreshBtn.textContent = '刷新中...';
    refreshBtn.disabled = true;
    
    // 模拟数据刷新
    setTimeout(() => {
        refreshBtn.textContent = originalText;
        refreshBtn.disabled = false;
        console.log('数据刷新完成');
    }, 2000);
}

/**
 * 打开设置弹窗
 */
function openSettings() {
    console.log('打开设置弹窗');
    // 这里可以添加打开设置弹窗的逻辑
}

/**
 * 导出函数供全局使用
 */
window.showSettings = showSettings;
window.switchDataPeriod = switchDataPeriod;
window.switchTenantAnalysisTime = switchTenantAnalysisTime;
window.refreshDashboard = refreshDashboard;
window.openSettings = openSettings;