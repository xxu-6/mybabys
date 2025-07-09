from django.urls import path
from .views import *

urlpatterns = [
    #个人中心页
    path('.html', shopperView, name='shopper'),
    #     # 登录注册页
    path('/login.html', loginView, name='login'),
    # 注销
    path('/logout.html', logoutView, name='logout'),
    # 购物车页
    path('/shopcart.html', shopcartView, name='shopcart'),
    # 删除商品API路由
    path('/delete.html', deleteAPI, name='delete'),
    # 支付页面路由
    path('/pays.html', paysView, name='pays'),
    path('/pay_callback/', payCallbackView, name='pay_callback'),





]