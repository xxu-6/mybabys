from django.contrib import admin

from .models import *
# Register your models here.
# admin.site.register(CartInfos)
# admin.site.register(OrderInfos)
# 注册CartInfos模型到admin管理，并自定义他在admin中的展示配置
@admin.register(CartInfos)
class CartInfosAdmin(admin.ModelAdmin):
    # 设置在列表页显示字段是id和quantity
    list_display = ['id', 'quantity']

@admin.register(OrderInfos)
class OrderInfosAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'create', 'state']
    # 按照state字段来进行过滤
    list_filter = ['state']
    # 设置按照created日期字段进行层级导航
    date_hierarchy = 'create'