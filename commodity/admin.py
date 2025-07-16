from django.contrib import admin

from . import CommodityConfig
# Register your models here.
from .models import *
# admin.site.register(Types)
# admin.site.register(CommodityInfos)
# 修改title和header
# 站点标题
admin.site.site_title = '母婴后台系统'
# 站点头部标题
admin.site.site_header = "母婴电商后台管理系统"
# 首页标题
admin.site.index_title = "母婴平台管理"

# 注册Types模型到admin管理，并定义了在admin中展示的配置
@admin.register(Types)
class TypesAdmin(admin.ModelAdmin):
    # 设置在列表页要显示的字段，我们通过遍历的方式遍历模型的字段映射来获取所有字段并显示
    list_display = [x for x in list(Types._meta._forward_fields_map.keys())]
    # 设置搜索的字段
    search_fields = ['firsts', 'seconds']
    # 设置过滤的字段
    list_filter = ['firsts']

@admin.register(CommodityInfos)
class CommodityInfosAdmin(admin.ModelAdmin):
    list_display =  [x for x in list(CommodityInfos._meta._forward_fields_map.keys())]
    # 按照name字段进行搜索
    search_fields = ['name']
    # 设置按照哪个日期字段进行层级的导航
    date_hierarchy = 'create'
    # 重新定义函数formfield_for_dbfield，用来自定义模型字段在表单中的显示
    def formfield_for_dbfield(self, db_field, **kwargs):
        # 我们这里主要针对types字段
        if db_field.name == 'types':
            # 动态设置types字段的可选值，从Types模型的对象中获取seconds字段的值作为候选项
            db_field.choices = [(x['seconds'], x['seconds']) for x in Types.objects.values('seconds') ]
        # 调用父类的方法，返回处理后的字段表单配置
        return super().formfield_for_dbfield(db_field, **kwargs)
    # 页面布局设置
    # 通过fieldsets划分不同的字段分组，让新增和修改页的表单布局更加清晰
    fieldsets = (
        # 第一组
        ('商品信息',{
            # 显示的字段
            'fields': ('name', 'sezes', 'types', 'price', 'discount')
        }),
        # 第二组
        ('收藏数量',{
            # collapse，让这个分组默认是折叠的（可展开）
            'classes': ('collapse',),
            'fields': ('likes',),
        }),
    )
    # 将模型中的types字段下拉选择框改成水平的单选按钮
    # admin.VERTICAL  垂直
    # radio_fields = {'types': admin.HORIZONTAL}
    # 数据排序，设置后台数据列表页的默认排序方式，按照id字段进行升序排序
    ordering = ['id']
    # 支持哪些字段点击表头进行排序
    sortable_by = ('price', 'discount')
    # 定义在数据列表页显示的模型字段
    list_display = ['id', 'name','sezes','types', 'price', 'discount']
    # 在数据列表的右侧添加筛选栏，按照types字段进行筛选
    list_filter = ['types']
    # 设置分页每页显示的数据条数
    list_per_page = 100
    # 最大显示数量
    list_max_show_all = 200
    # 允许在数据列表页面直接编辑name字段的值，不需要进入修改页面
    list_editable = ['name']
    # 在列表页面添加搜素框，支持按照name和types字段的值进行搜素数据
    search_fields = ['name', 'types']
    # 启用另存为按钮
    save_as = True
    # 下拉框位置，False表示不显示在顶部
    actions_on_top = False
    actions_on_bottom = True
    # 在list_display添加自定义字段colored_name
    list_display.append('colored_name')
    # def get_readonly_fields(self, request, obj = None):
    #     if request.user.is_superuser:
    #         self.readonly_fields = []
    #     else:
    #         self.readonly_fields = ['types']
    #     return self.readonly_fields

    # 根据当前的用户名设置数据访问权限
    def get_queryset(self, request):
        # 获取父类ModelAdmin的函数get_queryset()生成的模型查询对象，查询全数据
        qs = super().get_queryset(request)
        # 判断当前用户角色，如果是超级管理员，返回全部数据，否则返回id小于2的数据
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(id__lt=2)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'types':
            kwargs['choices'] = (('童装', '童装'), ('进口奶粉', '进口奶粉'))
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        对数据的修改实现日志记录
        request:当前用户的请求对象
        obj:模型的数据对象
        form:模型表单，是Django自动创建的模型表单
        change:判断当前请求是来自于数据修改页（True）还是数据新增页False
        """
        if change:
            # 获取当前用户名
            user = request.user.username
            # 使用模型获取数据,pk代表有主键属性的字段
            name = self.model.objects.get(pk=obj.pk).name
            # 使用表达获取数据
            types = form.cleaned_data['types']
            # 写入日志文件
            f = open("d://log.txt", 'a', encoding='utf-8')
            f.write(name + "商品类型：" + types + "被" + user + "修改" + '\r\n')
            f.close()
        else:
            pass
        super().save_model(request, obj, form, change)

    def get_datas(self, request, queryset):
        """
            queryset:代表已经被勾选的数据对象
            """
        temp = []
        for d in queryset:
            t = [d.name, d.types, str(d.discount)]
            temp.append(t)
            f = open("d://data.txt", 'a', encoding='utf-8')
        for t in temp:
            f.write(",".join(t) + '\r\n')
            f.close()

        self.message_user(request, "数据导出成功")
        # 设置函数的显示名称
    get_datas.short_description = "导出所选数据"

    # 添加到acton中
    actions = ['get_datas']