// 简单的Node.js HTTP服务器 - 完整版，解决乱码和路径问题
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

// 设置端口
const PORT = 8000;

// 创建服务器
const server = http.createServer((req, res) => {
    // 解析URL，确保中文路径正确解码
    const parsedUrl = url.parse(req.url);
    let filePath = decodeURIComponent(parsedUrl.pathname);
    
    console.log(`原始请求URL: ${req.url}`);
    console.log(`解码后的路径: ${filePath}`);
    
    // 特殊处理：忽略Vite客户端请求
    if (filePath.includes('@vite/client')) {
        console.log(`忽略Vite客户端请求: ${filePath}`);
        res.writeHead(200, { 'Content-Type': 'text/javascript; charset=utf-8' });
        res.end('// Vite client is not needed for this simple server', 'utf-8');
        return;
    }
    
    // 处理根路径
    if (filePath === '/') {
        filePath = path.join('.', '1.0', '超级管理员', '登录.html');
    } else if (filePath.startsWith('/')) {
        // 对于以/开头的绝对路径，我们只需要在前面加一个点
        filePath = '.' + filePath;
    }
    
    // 规范化路径分隔符，确保在Windows上也能正常工作
    filePath = filePath.replace(/\//g, path.sep);
    
    // 处理根路径请求
    if (filePath === './') {
        filePath = path.join('.', '1.0', '超级管理员', '登录.html');
    }
    
    console.log(`接收到请求: ${filePath}`);

    // 获取文件扩展名
    const extname = String(path.extname(filePath)).toLowerCase();
    
    // 设置MIME类型和字符编码
    const mimeTypes = {
        '.html': { type: 'text/html', encoding: 'utf-8' },
        '.css': { type: 'text/css', encoding: 'utf-8' },
        '.js': { type: 'text/javascript', encoding: 'utf-8' },
        '.json': { type: 'application/json', encoding: 'utf-8' },
        '.png': { type: 'image/png', encoding: null },
        '.jpg': { type: 'image/jpeg', encoding: null },
        '.gif': { type: 'image/gif', encoding: null },
        '.svg': { type: 'image/svg+xml', encoding: 'utf-8' }
    };

    const contentTypeInfo = mimeTypes[extname] || { type: 'application/octet-stream', encoding: null };

    // 读取文件并发送响应
    fs.readFile(filePath, contentTypeInfo.encoding, (error, content) => {
        if (error) {
            console.error(`错误: ${error.code} - ${filePath}`);
            if (error.code === 'ENOENT') {
                res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
                res.end(`<html><body><h1>404: 文件未找到</h1><p>请求的文件不存在: ${filePath}</p></body></html>`);
            } else {
                res.writeHead(500, { 'Content-Type': 'text/html; charset=utf-8' });
                res.end(`<html><body><h1>500: 服务器错误</h1><p>错误代码: ${error.code}</p></body></html>`);
            }
        } else {
            res.writeHead(200, { 
                'Content-Type': `${contentTypeInfo.type}${contentTypeInfo.encoding ? '; charset=' + contentTypeInfo.encoding : ''}` 
            });
            res.end(content);
        }
    });
});

// 启动服务器，绑定到所有网络接口，确保可以从任何网络访问
server.listen(PORT, '0.0.0.0', () => {
    console.log(`Node.js服务器已启动在 http://0.0.0.0:${PORT}`);
    console.log(`访问 http://localhost:${PORT} 或 http://127.0.0.1:${PORT} 查看登录页面`);
    console.log(`当前工作目录: ${process.cwd()}`);
});