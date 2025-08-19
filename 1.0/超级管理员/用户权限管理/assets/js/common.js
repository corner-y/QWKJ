/**
 * 通用JavaScript功能模块
 * 提供系统通用的工具函数和初始化逻辑
 */

// 通用工具函数
const CommonUtils = {
    /**
     * 显示消息提示
     */
    showMessage: function(message, type = 'info') {
        const alertClass = type === 'success' ? 'alert-success' : 
                          type === 'error' ? 'alert-danger' : 
                          type === 'warning' ? 'alert-warning' : 'alert-info';
        
        // 创建消息元素
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert ${alertClass} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // 添加到页面顶部
        const container = document.querySelector('.main-content') || document.body;
        container.insertBefore(alertDiv, container.firstChild);
        
        // 3秒后自动消失
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 3000);
    },

    /**
     * 格式化日期
     */
    formatDate: function(date, format = 'YYYY-MM-DD HH:mm:ss') {
        if (!date) return '';
        
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');
        const seconds = String(d.getSeconds()).padStart(2, '0');
        
        return format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day)
            .replace('HH', hours)
            .replace('mm', minutes)
            .replace('ss', seconds);
    },

    /**
     * 模拟API请求
     */
    mockApiRequest: function(url, options = {}) {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    ok: true,
                    data: {
                        success: true,
                        message: '操作成功',
                        data: []
                    }
                });
            }, 500);
        });
    }
};

// 页面初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('Common.js initialized');
});

// 导出到全局
window.CommonUtils = CommonUtils;