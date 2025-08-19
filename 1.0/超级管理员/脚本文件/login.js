// 登录页面脚本 - 实现假登录功能
console.log('login.js loaded');

// 获取表单元素
const loginForm = document.getElementById('loginForm');
const errorMessage = document.getElementById('errorMessage');

// 表单提交处理
loginForm.addEventListener('submit', function(event) {
    // 阻止表单默认提交
    event.preventDefault();
    
    // 获取表单数据
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // 简单的表单验证
    if (!username || !password) {
        showError('请输入用户名和密码');
        return;
    }
    
    // 隐藏错误信息
    hideError();
    
    // 模拟登录过程（假登录）
    console.log('正在处理登录请求...');
    
    // 这里可以添加登录请求的动画或其他效果
    const loginBtn = loginForm.querySelector('button[type="submit"]');
    const originalBtnText = loginBtn.textContent;
    loginBtn.disabled = true;
    loginBtn.textContent = '登录中...';
    
    // 使用setTimeout模拟网络延迟
    setTimeout(() => {
        console.log('登录成功，用户名:', username);
        
        // 登录成功后跳转到平台运营看板页面
        window.location.href = '/1.0/超级管理员/工作台/平台运营看板.html';
        
        // 恢复按钮状态（实际上跳转后不会执行到这里）
        loginBtn.disabled = false;
        loginBtn.textContent = originalBtnText;
    }, 1000);
});

// 显示错误信息
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

// 隐藏错误信息
function hideError() {
    errorMessage.style.display = 'none';
}