/**
 * 医疗智能审核系统 - 通用JavaScript库
 * 基于现代Web标准，提供统一的交互逻辑和工具函数
 */

// 全局配置
const CONFIG = {
  // API基础路径
  API_BASE: '/api/v1',
  
  // 页面路径配置
  PAGES: {
    // 登录相关
    LOGIN: '/login.html',
    INDEX: '/index.html',
    
    // 通用页面
    PROFILE: '/common/profile.html',
    NOTIFICATIONS: '/common/notifications.html',
    
    // 企业管理员页面
    ADMIN_DASHBOARD: '/enterprise-admin/dashboard.html',
    USER_LIST: '/enterprise-admin/user-list.html',
    USER_FORM: '/enterprise-admin/user-form.html',
    DEPARTMENT_MANAGEMENT: '/enterprise-admin/department-management.html',
    RULE_CONFIGURATOR: '/enterprise-admin/rule-configurator.html',
    RULE_PARAMETERS: '/enterprise-admin/rule-parameters.html',
    KB_CATALOGS: '/enterprise-admin/kb-catalogs.html',
    KB_IMPORT: '/enterprise-admin/kb-import.html',
    
    // 业务操作员页面
    WORKBENCH: '/operator/workbench.html',
    PRE_AUDIT_RECORDS: '/operator/pre-audit-records.html',
    AUDIT_DETAILS: '/operator/audit-details.html',
    IN_PROCESS_CHECK: '/operator/in-process-check.html',
    ALERT_QUEUE: '/operator/alert-queue.html',
    POST_AUDIT_TASK_LIST: '/operator/post-audit-task-list.html',
    POST_AUDIT_TASK_FORM: '/operator/post-audit-task-form.html',
    POST_AUDIT_RESULTS: '/operator/post-audit-results.html',
    
    // 报表页面
    REPORT_RULE_ANALYSIS: '/reports/report-rule-analysis.html',
    REPORT_DEPARTMENT_ANALYSIS: '/reports/report-department-analysis.html',
    REPORT_WORKLOAD_STATS: '/reports/report-workload-stats.html',
    
    // 超级管理员页面
    PLATFORM_DASHBOARD: '/工作台/平台运营看板.html',
    TENANT_LIST: '/用户权限管理/组织管理/租户管理.html',
    TENANT_FORM: '/用户权限管理/组织管理/租户表单.html'
  },
  
  // 本地存储键名
  STORAGE_KEYS: {
    USER_INFO: 'userInfo',
    TOKEN: 'authToken',
    THEME: 'theme',
    LANGUAGE: 'language',
    MENU_COLLAPSED: 'menuCollapsed'
  },
  
  // 消息类型
  MESSAGE_TYPES: {
    SUCCESS: 'success',
    ERROR: 'error',
    WARNING: 'warning',
    INFO: 'info'
  }
};

// 工具函数类
class Utils {
  /**
   * 格式化日期
   * @param {Date|string} date 日期对象或字符串
   * @param {string} format 格式化模板
   * @returns {string} 格式化后的日期字符串
   */
  static formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
    if (!date) return '-';
    
    const d = new Date(date);
    if (isNaN(d.getTime())) return '-';
    
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
  }
  
  /**
   * 格式化金额
   * @param {number} amount 金额
   * @param {string} currency 货币符号
   * @returns {string} 格式化后的金额字符串
   */
  static formatCurrency(amount, currency = '¥') {
    if (amount === null || amount === undefined) return '-';
    
    const num = Number(amount);
    if (isNaN(num)) return '-';
    
    return currency + num.toLocaleString('zh-CN', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  }
  
  /**
   * 格式化文件大小
   * @param {number} bytes 字节数
   * @returns {string} 格式化后的文件大小
   */
  static formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
  
  /**
   * 防抖函数
   * @param {Function} func 要防抖的函数
   * @param {number} wait 等待时间
   * @returns {Function} 防抖后的函数
   */
  static debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
  
  /**
   * 节流函数
   * @param {Function} func 要节流的函数
   * @param {number} limit 时间限制
   * @returns {Function} 节流后的函数
   */
  static throttle(func, limit) {
    let inThrottle;
    return function(...args) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }
  
  /**
   * 深拷贝对象
   * @param {any} obj 要拷贝的对象
   * @returns {any} 拷贝后的对象
   */
  static deepClone(obj) {
    if (obj === null || typeof obj !== 'object') return obj;
    if (obj instanceof Date) return new Date(obj.getTime());
    if (obj instanceof Array) return obj.map(item => Utils.deepClone(item));
    if (typeof obj === 'object') {
      const clonedObj = {};
      for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
          clonedObj[key] = Utils.deepClone(obj[key]);
        }
      }
      return clonedObj;
    }
  }
  
  /**
   * 生成UUID
   * @returns {string} UUID字符串
   */
  static generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
  
  /**
   * 验证邮箱格式
   * @param {string} email 邮箱地址
   * @returns {boolean} 是否有效
   */
  static validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }
  
  /**
   * 验证手机号格式
   * @param {string} phone 手机号
   * @returns {boolean} 是否有效
   */
  static validatePhone(phone) {
    const re = /^1[3-9]\d{9}$/;
    return re.test(phone);
  }
  
  /**
   * 获取URL参数
   * @param {string} name 参数名
   * @returns {string|null} 参数值
   */
  static getUrlParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
  }
  
  /**
   * 设置URL参数
   * @param {string} name 参数名
   * @param {string} value 参数值
   */
  static setUrlParam(name, value) {
    const url = new URL(window.location);
    url.searchParams.set(name, value);
    window.history.replaceState({}, '', url);
  }
}

// 本地存储管理类
class Storage {
  /**
   * 设置本地存储
   * @param {string} key 键名
   * @param {any} value 值
   */
  static set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('设置本地存储失败:', error);
    }
  }
  
  /**
   * 获取本地存储
   * @param {string} key 键名
   * @param {any} defaultValue 默认值
   * @returns {any} 存储的值
   */
  static get(key, defaultValue = null) {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
      console.error('获取本地存储失败:', error);
      return defaultValue;
    }
  }
  
  /**
   * 删除本地存储
   * @param {string} key 键名
   */
  static remove(key) {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error('删除本地存储失败:', error);
    }
  }
  
  /**
   * 清空本地存储
   */
  static clear() {
    try {
      localStorage.clear();
    } catch (error) {
      console.error('清空本地存储失败:', error);
    }
  }
}

// HTTP请求类
class Http {
  /**
   * 发送GET请求
   * @param {string} url 请求URL
   * @param {Object} params 请求参数
   * @returns {Promise} 请求Promise
   */
  static async get(url, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const fullUrl = queryString ? `${url}?${queryString}` : url;
    
    return this.request(fullUrl, {
      method: 'GET'
    });
  }
  
  /**
   * 发送POST请求
   * @param {string} url 请求URL
   * @param {Object} data 请求数据
   * @returns {Promise} 请求Promise
   */
  static async post(url, data = {}) {
    return this.request(url, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }
  
  /**
   * 发送PUT请求
   * @param {string} url 请求URL
   * @param {Object} data 请求数据
   * @returns {Promise} 请求Promise
   */
  static async put(url, data = {}) {
    return this.request(url, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }
  
  /**
   * 发送DELETE请求
   * @param {string} url 请求URL
   * @returns {Promise} 请求Promise
   */
  static async delete(url) {
    return this.request(url, {
      method: 'DELETE'
    });
  }
  
  /**
   * 通用请求方法
   * @param {string} url 请求URL
   * @param {Object} options 请求选项
   * @returns {Promise} 请求Promise
   */
  static async request(url, options = {}) {
    const token = Storage.get(CONFIG.STORAGE_KEYS.TOKEN);
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
      }
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
      const response = await fetch(CONFIG.API_BASE + url, finalOptions);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('请求失败:', error);
      throw error;
    }
  }
}

// 消息提示类
class Message {
  /**
   * 显示消息
   * @param {string} text 消息文本
   * @param {string} type 消息类型
   * @param {number} duration 显示时长
   */
  static show(text, type = CONFIG.MESSAGE_TYPES.INFO, duration = 3000) {
    // 创建消息容器
    let container = document.getElementById('message-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'message-container';
      container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        pointer-events: none;
      `;
      document.body.appendChild(container);
    }
    
    // 创建消息元素
    const message = document.createElement('div');
    message.className = `message message-${type}`;
    message.style.cssText = `
      background: white;
      border-radius: 6px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      padding: 12px 16px;
      margin-bottom: 8px;
      border-left: 4px solid var(--${type === 'success' ? 'success' : type === 'error' ? 'error' : type === 'warning' ? 'warning' : 'info'}-color);
      pointer-events: auto;
      transform: translateX(100%);
      transition: transform 0.3s ease;
      max-width: 300px;
      word-wrap: break-word;
    `;
    
    message.textContent = text;
    container.appendChild(message);
    
    // 动画显示
    setTimeout(() => {
      message.style.transform = 'translateX(0)';
    }, 10);
    
    // 自动隐藏
    setTimeout(() => {
      message.style.transform = 'translateX(100%)';
      setTimeout(() => {
        if (message.parentNode) {
          message.parentNode.removeChild(message);
        }
      }, 300);
    }, duration);
  }
  
  /**
   * 显示成功消息
   * @param {string} text 消息文本
   */
  static success(text) {
    this.show(text, CONFIG.MESSAGE_TYPES.SUCCESS);
  }
  
  /**
   * 显示错误消息
   * @param {string} text 消息文本
   */
  static error(text) {
    this.show(text, CONFIG.MESSAGE_TYPES.ERROR);
  }
  
  /**
   * 显示警告消息
   * @param {string} text 消息文本
   */
  static warning(text) {
    this.show(text, CONFIG.MESSAGE_TYPES.WARNING);
  }
  
  /**
   * 显示信息消息
   * @param {string} text 消息文本
   */
  static info(text) {
    this.show(text, CONFIG.MESSAGE_TYPES.INFO);
  }
}

// 页面导航类
class Navigation {
  /**
   * 跳转到指定页面
   * @param {string} page 页面路径
   * @param {Object} params 页面参数
   */
  static goto(page, params = {}) {
    let url = page;
    
    // 如果是相对路径，添加基础路径
    if (!page.startsWith('http') && !page.startsWith('/')) {
      url = '/' + page;
    }
    
    // 添加参数
    if (Object.keys(params).length > 0) {
      const queryString = new URLSearchParams(params).toString();
      url += (url.includes('?') ? '&' : '?') + queryString;
    }
    
    window.location.href = url;
  }
  
  /**
   * 返回上一页
   */
  static back() {
    window.history.back();
  }
  
  /**
   * 刷新当前页面
   */
  static reload() {
    window.location.reload();
  }
  
  /**
   * 替换当前页面
   * @param {string} page 页面路径
   * @param {Object} params 页面参数
   */
  static replace(page, params = {}) {
    let url = page;
    
    if (!page.startsWith('http') && !page.startsWith('/')) {
      url = '/' + page;
    }
    
    if (Object.keys(params).length > 0) {
      const queryString = new URLSearchParams(params).toString();
      url += (url.includes('?') ? '&' : '?') + queryString;
    }
    
    window.location.replace(url);
  }
}

// 模态框管理类
class Modal {
  /**
   * 显示模态框
   * @param {string} modalId 模态框ID
   */
  static show(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
      
      // 点击背景关闭
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          this.hide(modalId);
        }
      });
    }
  }
  
  /**
   * 隐藏模态框
   * @param {string} modalId 模态框ID
   */
  static hide(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.style.display = 'none';
      document.body.style.overflow = '';
    }
  }
  
  /**
   * 切换模态框显示状态
   * @param {string} modalId 模态框ID
   */
  static toggle(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      if (modal.style.display === 'flex') {
        this.hide(modalId);
      } else {
        this.show(modalId);
      }
    }
  }
}

// 表单验证类
class Validator {
  /**
   * 验证表单
   * @param {HTMLFormElement} form 表单元素
   * @param {Object} rules 验证规则
   * @returns {Object} 验证结果
   */
  static validate(form, rules = {}) {
    const errors = {};
    const formData = new FormData(form);
    
    for (const [field, rule] of Object.entries(rules)) {
      const value = formData.get(field);
      const fieldErrors = [];
      
      // 必填验证
      if (rule.required && (!value || value.trim() === '')) {
        fieldErrors.push(rule.requiredMessage || `${field}不能为空`);
      }
      
      // 长度验证
      if (value && rule.minLength && value.length < rule.minLength) {
        fieldErrors.push(rule.minLengthMessage || `${field}长度不能少于${rule.minLength}个字符`);
      }
      
      if (value && rule.maxLength && value.length > rule.maxLength) {
        fieldErrors.push(rule.maxLengthMessage || `${field}长度不能超过${rule.maxLength}个字符`);
      }
      
      // 正则验证
      if (value && rule.pattern && !rule.pattern.test(value)) {
        fieldErrors.push(rule.patternMessage || `${field}格式不正确`);
      }
      
      // 自定义验证
      if (value && rule.validator && typeof rule.validator === 'function') {
        const customResult = rule.validator(value);
        if (customResult !== true) {
          fieldErrors.push(customResult || `${field}验证失败`);
        }
      }
      
      if (fieldErrors.length > 0) {
        errors[field] = fieldErrors;
      }
    }
    
    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  }
  
  /**
   * 显示验证错误
   * @param {Object} errors 错误信息
   */
  static showErrors(errors) {
    // 清除之前的错误信息
    document.querySelectorAll('.form-error').forEach(el => el.remove());
    
    for (const [field, fieldErrors] of Object.entries(errors)) {
      const input = document.querySelector(`[name="${field}"]`);
      if (input) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'form-error';
        errorDiv.textContent = fieldErrors[0];
        input.parentNode.appendChild(errorDiv);
        
        // 添加错误样式
        input.style.borderColor = 'var(--error-color)';
      }
    }
  }
  
  /**
   * 清除验证错误
   */
  static clearErrors() {
    document.querySelectorAll('.form-error').forEach(el => el.remove());
    document.querySelectorAll('.form-input, .form-select, .form-textarea').forEach(el => {
      el.style.borderColor = '';
    });
  }
}

// 加载状态管理类
class Loading {
  /**
   * 显示加载状态
   * @param {string} target 目标元素选择器
   * @param {string} text 加载文本
   */
  static show(target = 'body', text = '加载中...') {
    const element = typeof target === 'string' ? document.querySelector(target) : target;
    if (!element) return;
    
    // 创建加载遮罩
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.8);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 999;
    `;
    
    const content = document.createElement('div');
    content.style.cssText = `
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
    `;
    
    const spinner = document.createElement('div');
    spinner.className = 'loading';
    
    const textEl = document.createElement('div');
    textEl.textContent = text;
    textEl.style.color = 'var(--text-secondary)';
    
    content.appendChild(spinner);
    content.appendChild(textEl);
    overlay.appendChild(content);
    
    // 设置相对定位
    if (getComputedStyle(element).position === 'static') {
      element.style.position = 'relative';
    }
    
    element.appendChild(overlay);
  }
  
  /**
   * 隐藏加载状态
   * @param {string} target 目标元素选择器
   */
  static hide(target = 'body') {
    const element = typeof target === 'string' ? document.querySelector(target) : target;
    if (!element) return;
    
    const overlay = element.querySelector('.loading-overlay');
    if (overlay) {
      overlay.remove();
    }
  }
}

// 用户认证管理类
class Auth {
  /**
   * 检查用户是否已登录
   * @returns {boolean} 是否已登录
   */
  static isLoggedIn() {
    return !!Storage.get(CONFIG.STORAGE_KEYS.TOKEN);
  }
  
  /**
   * 获取当前用户信息
   * @returns {Object|null} 用户信息
   */
  static getCurrentUser() {
    return Storage.get(CONFIG.STORAGE_KEYS.USER_INFO);
  }
  
  /**
   * 设置用户信息
   * @param {Object} userInfo 用户信息
   * @param {string} token 认证令牌
   */
  static setUser(userInfo, token) {
    Storage.set(CONFIG.STORAGE_KEYS.USER_INFO, userInfo);
    Storage.set(CONFIG.STORAGE_KEYS.TOKEN, token);
  }
  
  /**
   * 用户登出
   */
  static logout() {
    Storage.remove(CONFIG.STORAGE_KEYS.USER_INFO);
    Storage.remove(CONFIG.STORAGE_KEYS.TOKEN);
    Navigation.replace(CONFIG.PAGES.LOGIN);
  }
  
  /**
   * 检查页面访问权限
   * @param {Array} requiredRoles 需要的角色
   * @returns {boolean} 是否有权限
   */
  static hasPermission(requiredRoles = []) {
    if (!this.isLoggedIn()) return false;
    
    const user = this.getCurrentUser();
    if (!user || !user.roles) return false;
    
    if (requiredRoles.length === 0) return true;
    
    return requiredRoles.some(role => user.roles.includes(role));
  }
}

// 页面初始化
document.addEventListener('DOMContentLoaded', function() {
  // 检查登录状态（除登录页面外）
  console.log('当前页面路径:', window.location.pathname);
  console.log('是否已登录:', Auth.isLoggedIn());
  
  if (!window.location.pathname.includes('login.html') && !Auth.isLoggedIn()) {
    console.log('用户未登录，正在设置演示用户...');
    // 为演示目的，设置默认用户
    if (window.location.pathname.includes('超级管理员/')) {
      console.log('设置超级管理员用户');
      Auth.setUser({
        id: 1,
        username: 'admin',
        name: '超级管理员',
        roles: ['超级管理员']
      }, 'demo-token-123');
    } else if (window.location.pathname.includes('enterprise-admin/')) {
      console.log('设置企业管理员用户');
      Auth.setUser({
        id: 2,
        username: 'enterprise_admin',
        name: '企业管理员',
        roles: ['enterprise-admin']
      }, 'demo-token-456');
    } else {
      console.log('跳转到登录页面');
      Navigation.replace(CONFIG.PAGES.LOGIN);
      return;
    }
  } else {
    console.log('用户已登录或在登录页面');
  }
  
  // 初始化通用事件监听
  initEventListeners();
  
  // 初始化用户信息显示
  initUserInfo();
});

/**
 * 初始化事件监听器
 */
function initEventListeners() {
  // 全局点击事件
  document.addEventListener('click', function(e) {
    // 处理返回按钮
    if (e.target.matches('.back-btn, .back-btn *')) {
      e.preventDefault();
      Navigation.back();
    }
    
    // 处理模态框关闭按钮
    if (e.target.matches('.modal-close')) {
      const modal = e.target.closest('.modal');
      if (modal) {
        Modal.hide(modal.id);
      }
    }
    
    // 处理登出按钮
    if (e.target.matches('.logout-btn')) {
      e.preventDefault();
      if (confirm('确定要退出登录吗？')) {
        Auth.logout();
      }
    }
  });
  
  // 表单提交事件
  document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.classList.contains('validate-form')) {
      e.preventDefault();
      
      // 这里可以添加通用的表单验证逻辑
      console.log('表单提交:', new FormData(form));
    }
  });
  
  // 输入框焦点事件（清除错误状态）
  document.addEventListener('focus', function(e) {
    if (e.target.matches('.form-input, .form-select, .form-textarea')) {
      e.target.style.borderColor = '';
      const errorEl = e.target.parentNode.querySelector('.form-error');
      if (errorEl) {
        errorEl.remove();
      }
    }
  }, true);
}

/**
 * 初始化用户信息显示
 */
function initUserInfo() {
  const user = Auth.getCurrentUser();
  if (user) {
    // 更新用户名显示
    document.querySelectorAll('.user-name').forEach(el => {
      el.textContent = user.name || user.username || '用户';
    });
    
    // 更新用户角色显示
    document.querySelectorAll('.user-role').forEach(el => {
      el.textContent = user.roleName || '用户';
    });
    
    // 更新用户头像
    document.querySelectorAll('.user-avatar').forEach(el => {
      if (user.avatar) {
        el.src = user.avatar;
      }
    });
  }
}

// 导出到全局
window.Utils = Utils;
window.Storage = Storage;
window.Http = Http;
window.Message = Message;
window.Navigation = Navigation;
window.Modal = Modal;
window.Validator = Validator;
window.Loading = Loading;
window.Auth = Auth;
window.CONFIG = CONFIG;

// 常用的全局函数
window.goBack = () => Navigation.back();
window.showModal = (id) => Modal.show(id);
window.hideModal = (id) => Modal.hide(id);
window.showMessage = (text, type) => Message.show(text, type);
window.formatDate = (date, format) => Utils.formatDate(date, format);
window.formatCurrency = (amount) => Utils.formatCurrency(amount);