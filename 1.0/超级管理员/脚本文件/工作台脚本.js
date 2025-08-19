// 工作台脚本
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工作台
    initWorkbench();
    
    // 绑定事件
    bindEvents();
    
    // 加载数据
    loadWorkbenchData();
});

function initWorkbench() {
    console.log('工作台初始化完成');
}

function bindEvents() {
    // 绑定快捷操作按钮事件
    const quickActions = document.querySelectorAll('.quick-action');
    quickActions.forEach(action => {
        action.addEventListener('click', function() {
            const actionType = this.dataset.action;
            handleQuickAction(actionType);
        });
    });
    
    // 绑定待办事项点击事件
    const todoItems = document.querySelectorAll('.todo-item');
    todoItems.forEach(item => {
        item.addEventListener('click', function() {
            const todoId = this.dataset.id;
            handleTodoClick(todoId);
        });
    });
}

function handleQuickAction(actionType) {
    switch(actionType) {
        case 'audit':
            window.location.href = '事前审核记录.html';
            break;
        case 'check':
            window.location.href = '事中审核检查.html';
            break;
        case 'task':
            window.location.href = '事后审核任务列表.html';
            break;
        case 'result':
            window.location.href = '审核结果.html';
            break;
        default:
            console.log('未知操作类型:', actionType);
    }
}

function handleTodoClick(todoId) {
    console.log('点击待办事项:', todoId);
    // 这里可以添加具体的待办事项处理逻辑
}

function loadWorkbenchData() {
    // 模拟加载工作台数据
    updateStatistics();
    updateRecentActivities();
}

function updateStatistics() {
    // 更新统计数据
    const stats = {
        todayAudit: 156,
        pendingTasks: 23,
        completedTasks: 89,
        alertCount: 5
    };
    
    // 更新页面显示
    const statElements = document.querySelectorAll('.stat-number');
    if (statElements.length >= 4) {
        statElements[0].textContent = stats.todayAudit;
        statElements[1].textContent = stats.pendingTasks;
        statElements[2].textContent = stats.completedTasks;
        statElements[3].textContent = stats.alertCount;
    }
}

function updateRecentActivities() {
    // 更新最近活动
    console.log('更新最近活动数据');
    // 这里可以添加动态更新最近活动的逻辑
}

// 定时刷新数据
setInterval(function() {
    loadWorkbenchData();
}, 30000); // 每30秒刷新一次