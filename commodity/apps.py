from django.apps import AppConfig

"""
这段代码定义了 Django 应用的配置类，主要完成以下工作：
默认自动字段设置：
default_auto_field 指定了应用中模型的主键默认使用的字段类型
BigAutoField 提供了更大的数值范围，适合可能产生大量记录的应用
若不设置，Django 默认为 AutoField（32 位整数，最大支持约 21 亿条记录）
应用标识：
name 属性指定了应用的内部名称，必须与项目中应用的文件夹名称一致
Django 在加载应用、处理依赖关系和路由时使用此名称
用户友好名称：
verbose_name 为应用提供了一个更具描述性的名称
该名称将显示在 Django 管理员界面左侧的应用列表中
推荐使用中文或其他易于理解的语言，提高后台管理的可读性
"""
class CommodityConfig(AppConfig):
    # 设置默认的自动字段类型
    # BigAutoField 是 64 位整数类型，适用于数据量极大的场景
    # 避免普通 AutoField(32位) 在数据量超过 21 亿时可能出现的溢出问题
    default_auto_field = 'django.db.models.BigAutoField'

    # 应用的内部名称，必须与项目中应用的文件夹名称一致
    # Django 通过此名称识别和导入应用
    name = 'commodity'

    # 应用的可读名称，将显示在 Django 管理员界面和其他地方
    # 用于提高界面的可读性，替代默认的应用文件夹名称
    verbose_name = '商品管理'