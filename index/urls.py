from django.urls import path
# 从当前应用的views模块导入所有的视图
from .views import *

# 定义URL路由列表
urlpatterns = [
    # 根路径映射到indexView，命名是index，可以用于模板和代码中的反向解析URL
    #path("", indexView, name='index')
    path('',indexClassView.as_view(),name='index')
]