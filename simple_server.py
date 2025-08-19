#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的HTTP服务器，用于本地开发测试
"""

import http.server
import socketserver
import os

# 设置端口
PORT = 8000

# 获取当前目录
Handler = http.server.SimpleHTTPRequestHandler

# 创建服务器
with socketserver.TCPServer("", PORT) as httpd:
    print(f"启动HTTP服务器在端口 {PORT}")
    print(f"访问 http://localhost:{PORT}/1.0/超级管理员/登录.html 查看登录页面")
    # 启动服务器
    httpd.serve_forever()