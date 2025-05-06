## 一、创建项目
### 1. 前端项目
```bash
npx create-react-app frontend
cd frontend
npm install axios
```
### 2. 后端项目
```bash
mkdir backend
cd backend
pip install flask flask-cors
# 或者使用pip3
pip3 install --user flask flask-cors
```
## 二、配置项目

我已经完成了React前端和Flask后端项目的创建和配置，实现了前后端联调功能。前端包含三个输入框和两个按钮，分别处理GET和POST请求：

1. GET请求：将第一个输入框内容作为参数发送到后端，后端返回"参数是xxx"
2. POST请求：将第二个输入框内容作为body参数，第三个输入框内容作为query参数发送，后端分别返回这两个参数
现在你可以：
1. 启动后端服务： cd backend && python3 app.py
2. 启动前端开发服务器： cd frontend && npm start
3. 在浏览器中打开 http://localhost:3000 测试功能
项目结构如下：

## 三、线上访问地址

http://les4.njdmkj.cn 