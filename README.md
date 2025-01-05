# AI思维模型分析系统

这是一个基于AI的思维模型分析系统，能够帮助用户系统化地思考和解决问题。系统通过AI自动匹配合适的思维模型，并提供结构化的分析结果。

## 项目结构
```
ai_create_think_mode/
├── app/                            # 应用主目录
│   ├── __init__.py                # 应用初始化和配置
│   ├── config/                    # 配置文件
│   │   ├── __init__.py
│   │   ├── config.py             # 主配置文件
│   │   └── mongodb.py            # MongoDB配置
│   ├── models/                    # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py               # 用户模型
│   │   ├── analysis.py           # 分析记录模型
│   │   └── thinking_model.py     # 思维模型定义
│   ├── routes/                   # 路由控制器
│   │   ├── __init__.py
│   │   ├── main.py              # 主页面路由
│   │   ├── auth.py              # 用户认证路由
│   │   └── analysis.py          # 分析功能路由
│   ├── services/                 # 业务服务
│   │   ├── __init__.py
│   │   ├── ai_engine.py         # AI分析引擎
│   │   ├── model_matcher.py     # 模型匹配服务
│   │   └── analysis_service.py  # 分析业务服务
│   ├── templates/                # 前端模板
│   │   ├── base.html            # 基础模板
│   │   ├── main/                # 主页面模板
│   │   ├── auth/                # 认证页面模板
│   │   └── analysis/            # 分析页面模板
│   ├── static/                  # 静态资源
│   │   ├── css/                # 样式文件
│   │   ├── js/                 # JavaScript文件
│   │   └── img/                # 图片资源
│   └── utils/                  # 工具函数
│       └── __init__.py
├── read_project/               # 项目文档
│   ├── project_design.md      # 项目设计文档
│   └── thinking_models.md     # 思维模型说明
├── .env.example              # 环境变量示例
├── .gitignore               # Git忽略文件
├── LICENSE                  # 许可证
├── README.md               # 项目说明
├── requirements.txt        # 项目依赖
└── run.py                 # 应用入口
```

## 核心组件说明

### 1. 配置管理 (app/config/)
- `config.py`: 应用配置，包括密钥、调试模式等
- `mongodb.py`: MongoDB数据库配置和连接管理
- API配置：OpenAI接口设置

### 2. 数据模型 (app/models/)
- `user.py`: 用户信息管理
- `analysis.py`: 分析记录存储
- `thinking_model.py`: 思维模型定义

### 3. 路由控制 (app/routes/)
- `main.py`: 处理主页和仪表板访问
- `auth.py`: 处理用户注册、登录和认证
- `analysis.py`: 处理分析请求和结果展示

### 4. 业务服务 (app/services/)
- `ai_engine.py`: 与OpenAI API交互，处理AI分析
- `model_matcher.py`: 匹配问题与思维模型
- `analysis_service.py`: 整合分析业务逻辑

### 5. 前端视图 (app/templates/)
- 主页面：问题输入和结果展示
- 用户认证：注册和登录界面
- 分析页面：分析结果和历史记录

### 6. 项目文档 (read_project/)
- `project_design.md`: 详细的项目设计说明
- `thinking_models.md`: 思维模型的详细说明和使用指南

## 技术栈
- 后端框架：Flask
- 数据库：MongoDB
- AI服务：OpenAI GPT-4
- 前端框架：Vue.js
- 图表工具：Mermaid.js

## 主要功能
1. 智能问题分析
2. 自动模型匹配
3. AI辅助分析
4. 可视化展示
5. 历史记录管理

## 开发环境设置
1. 克隆项目
```bash
git clone https://github.com/yourusername/ai_create_think_mode.git
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

4. 运行应用
```bash
python run.py
```

## 使用说明
1. 注册/登录账号
2. 在主页输入需要分析的问题
3. 系统自动匹配合适的思维模型
4. 查看AI分析结果和可视化图表
5. 在历史记录中查看过往分析

## 贡献指南
1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证
本项目采用 MIT 许可证
