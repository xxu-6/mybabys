# Mybabys 项目说明

## 项目介绍
Mybabys 是一个基于 Django 的电商平台项目，主要功能包括商品展示、购物车管理、用户登录和订单处理。项目使用 Layui 前端框架进行界面设计。

## 目录结构
```
mybabys/
├── commodity/        # 商品模块
├── index/              # 首页模块
├── shopper/            # 购物车/订单模块
├── pstatic/            # 静态资源
└── templates/          # 模板文件
```

## 主要功能
- 商品分类展示
- 商品详情查看
- 购物车管理
- 用户登录/登出
- 订单生成与支付

## 技术栈
- 后端：Python + Django
- 前端：HTML + CSS + JavaScript
- UI 框架：Layui
- 数据库：SQLite

## 快速开始
1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 数据库迁移：
```bash
python manage.py migrate
```

3. 启动开发服务器：
```bash
python manage.py runserver
```

## 使用说明
- 首页：http://localhost:8000/
- 商品列表：http://localhost:8000/commodity/
- 商品详情：http://localhost:8000/commodity/detail/<商品ID>
- 购物车：http://localhost:8000/shopper/cart/
- 登录：http://localhost:8000/shopper/login/

## 模型说明
- `Types`：商品分类
- `CommodityInfos`：商品信息
- `CartInfos`：购物车信息
- `OrderInfos`：订单信息

## 开发者
- 使用 `pstatic/js/script.js` 实现页面交互效果
- 使用 `parallax.min.js` 实现视差滚动效果

## 许可证
该项目遵循 MIT 许可证

## 贡献指南
请遵循 PEP8 Python 编码规范，保持代码简洁易读