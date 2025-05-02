# 项目文档

## 项目概述
本项目包含一个Python后端项目和一个React前端项目。前端使用ECharts进行图表可视化展示，UI组件库采用Ant Design。主页有图表菜单，点击不同菜单可展示不同类型的图表，包括饼图、柱状图、折线图等。所有图表数据均通过Python后端接口获取，后端可随机生成假数据。

## 项目结构
```
/第五周
├── backend
│   ├── app.py
│   └── venv
└── frontend
    ├── public
    ├── src
    │   ├── App.js
    │   └── App.css
    └── package.json
```

## 后端项目
### 环境搭建
1. 进入 `backend` 目录：`cd /Users/yangqi/Desktop/Private/私活/Python+react（2025-04-23）/第五周/backend`
2. 激活虚拟环境：`source venv/bin/activate`
3. 安装依赖：`pip3 install flask`

### 运行项目
在 `backend` 目录下运行以下命令：
```bash
python3 app.py
```

### 接口文档
- **接口地址**：`http://127.0.0.1:5000/get_chart_data/<chart_type>`
- **请求方法**：`GET`
- **参数说明**：`chart_type` 为图表类型，可选值有 `pie`, `bar`, `line`, `china_map`, `graph`, `scatter`, `radar`, `path`。
- **响应示例**：
```json
[
  {
    "name": "A",
    "value": 50
  },
  {
    "name": "B",
    "value": 30
  }
]
```

## 前端项目
### 环境搭建
进入 `frontend` 目录并安装依赖：
```bash
cd /Users/yangqi/Desktop/Private/私活/Python+react（2025-04-23）/第五周/frontend
npm install echarts antd
```

### 运行项目
在 `frontend` 目录下运行以下命令：
```bash
npm start
```

## 注意事项
- 确保后端服务已启动，前端才能正常获取数据。
- 前端项目运行在 `http://localhost:3000`，后端项目运行在 `http://127.0.0.1:5000`。