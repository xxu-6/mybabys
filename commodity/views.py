# Django 快捷函数：用于渲染模板并返回 HTTP 响应
from django.forms import model_to_dict
from django.shortcuts import render

# Django 分页工具：用于处理数据分页
from django.core.paginator import Paginator  # 分页器类，将查询集分页
from django.core.paginator import EmptyPage  # 页码超出范围时抛出的异常
from django.core.paginator import PageNotAnInteger  # 页码非整数时抛出的异常

# 导入当前应用的模型
from .models import *

# HTTP 响应工具：用于返回 JSON 格式的响应
from django.http import JsonResponse

# 数据库表达式：用于执行原子性更新操作（避免并发问题）
from django.db.models import F

# Create your views here.

def commodityView(request):
    """
    商品列表页视图函数
    - 支持分类、排序、搜索
    - 实现分页
    """
    title = '商品列表'
    # 页面分类标识
    classContent = 'commoditys'
    # 生成商品分类列表，为一级分类去重
    firsts = Types.objects.values('firsts').distinct()
    # 查询Types的所有数据
    typesList = Types.objects.all()
    # 获取请求参数
    # t:分类ID，筛选商品类型，查询某个分页的商品信息
    # 首先查询模型Type的字段id等于t的数据A
    # 然后从数据A中获取字段seconds的数据B
    # 最后查询模型CommodityInfos等于数据B的数据
    # 得到某个分页的商品信息
    t = request.GET.get('t', '')
    # s用于设置商品的排序方式
    # 如果s为空，则默认变量s等于sold
    # sold代表模型CommodityInfos的字段sold
    # 请求参数s的值为sold、price、create、likes
    s = request.GET.get('s', 'sold')
    # p用于设置商品信息的页数，默认等于1，代表当前第一页的商品信息
    # 当前排序的第1-第6的商品信息
    p = request.GET.get('p', '1')
    # n是商品搜索功能的关键字，和模型CommodityInfos的字段name进行模糊匹配
    # 查询条件:name_contains=n
    n = request.GET.get('n', '')

    # 初始化商品查询集
    commodityInfos = CommodityInfos.objects.all()
    # 通过判断变量n t s  是否为空，决定变量commodityInfos是否添加相应的查询条件
    # 每执行一次查询条件，查询结果重新赋值给变量commodityInfos，覆盖上一次的查询结果
    # 目的就是让n t s 对应的查询结果能够互相兼容
    if t:
        # 根据分类Id筛选商品
        types = Types.objects.filter(id=t).first()
        commodityInfos = commodityInfos.filter(types=types.seconds)
    if s:
        # 根据指定字段排序，添加负号表示降序
        commodityInfos = commodityInfos.order_by('-' + s)
    if n:
        # 根据关键词模糊搜索商品名
        commodityInfos = commodityInfos.filter(name__contains=n)

    # 分页处理
    # 每页显示6条商品信息，如果参数p的值不是整数，那么默认返回第一页的商品信息
    # 如果参数p的值大于分页后的总页数，那么默认返回最后一个商品信息
    paginator = Paginator(commodityInfos, 6)
    try:
        # 获取指定页的数据
        pages = paginator.page(p)
    except PageNotAnInteger:
        # 页码非整数，返回第一页
        pages = paginator.page(1)
    except EmptyPage:
        # 页码超出范围，返回最后一页
        pages = paginator.page(paginator.num_pages)

    return render(request, 'commodity.html', locals())


# def commodityView(request):
#     """
#     商品列表API
#     """
#     # 从HTTP请求对象request获取请求参数types、search、sort、p
#     types = request.GET.get('types', '')
#     search = request.GET.get('search', '')
#     sort = request.GET.get('sort', 'sold')
#     p = request.GET.get('p', 1)
#     # 从模型Type中查找所有分类写入变量context
#     context = {'state': "success", 'msg': "获取成功", 'data': {}}
#     context['data']['types'] = []
#     firsts = Types.objects.values_list('firsts', flat=True).distinct()
#     for f in firsts:
#         t = Types.objects.filter(firsts=f).values_list('seconds', flat=True).all()
#         context['data']['types'].append(dict(name=f, value=list(t)))
#     # 根据请求参数对模型CommodityInfos进行数据查询，把查询结果存入变量cf中
#     cf = CommodityInfos.objects.all()
#     if types:
#         cf = cf.filter(types=types)
#     if sort:
#         cf = cf.order_by("-" + sort)
#     if search:
#         cf = cf.filter(name__contains=search)
#     result = []
#     # 对查询结果cf进行遍历，每次遍历都会调用model_to_dict将模型字段转换为字典格式，并写入result
#     # 如果模型字段格式为日期或文件，那么model_to_dict将会把字段转换为日期对象和文件对象，但是JsonResponse
#     # 无法将日期对象和文件对象转换为JSON格式，所以对于特殊的模型字段，需要自行转换
#     for c in cf.all():
#         d = model_to_dict(c)
#         d['create'] = c.create.strftime('%Y-%m-%d')
#         d['img'] = c.img.url
#         d['details'] = c.details.url
#         result.append(d)
#     # 调用分页函数，将列表result作为分页对象，得到分页数据，并写入context
#     # 通过实例化JsonResponse将变量context作为响应数据
#     pages, previous, nexts, pageCount = get_page_data(result, p)
#     context['data']['commodityInfos'] = dict(
#         data=pages,
#         previous=previous,
#         nexts=nexts,
#         count=cf.count(),
#         pageCount=pageCount)
#     #  json_dumps_params={'ensure_ascii': False} 将Python对象序列化
#     #  ensure_ascii为True会把非ASCII字节(中文)转换为Unicode编码
#     #  为False会保留原始字符
#     return JsonResponse(context, safe=False, json_dumps_params={'ensure_ascii': False})
def detailView(request, id):
    """
    商品详情页视图函数
    - 获取指定ID的商品详情
    - 获取销量前五的相关商品
    - 检查商品是否被当前用户收藏
    """
    title = '商品介绍'
    classContent = 'datails'
    # 查询除了当前商品外的前五个商品（推荐商品）
    items = CommodityInfos.objects.exclude(id=id).order_by('-sold')[:5]
    # 查询指定ID的商品，如果没有就返回None
    commoditys = CommodityInfos.objects.filter(id=id).first()
    # 从Session中获取用户收藏列表
    likesList = request.session.get('likes', [])
    # 判断当前商品是否被用户收藏
    likes = True if id in likesList else False

    return render(request, 'details.html', locals())

def collectView(request):
    """
    商品收藏视图函数（AJAX接口）
    - 处理用户的收藏请求
    - 更新商品收藏的数量
    - 记录用户收藏状态到Session
    Session Cookie
    """
    # 首先从请求对象request获取请求参数id的值，并赋值给变量id
    # 代表当前商品的主键id
    id = request.GET.get('id', '')
    # 然后设置响应内容result，以字典的形式表示
    result = {"result": "已收藏"}
    # 最后从请求对象request获取会话Session数据likes，
    # 如果存在数据，那么赋值给变量likes，否则变量likes设置为空列表
    likes = request.session.get('likes', [])
    # 如果变量id不为空，并且变量id不在likes中，那么说明当前的商品
    # 还没有被当前用户加入收藏，程序将执行商品收藏的操作
    if id and not int(id) in likes:
        # 使用F表达式原子性的增加商品收藏数，避免并发问题
        # 将变量id作为模型CommodityInfos的查询条件，再由查询对象使用update方法和F方法
        # 实现字段likes的自增一操作
        CommodityInfos.objects.filter(id=id).update(likes=F('likes') + 1)
        # 然后将响应内容result改为收藏成功
        result["result"] = "收藏成功"
        # 最后，将当前商品的id写入会话session数据likes，标记当前商品已经被用户收藏了
        request.session['likes'] = likes + [int(id)]
    # 返回JSON的响应
    # JsonResponse有将Python的字典转换为JSON数据
    # 使用HttpResponse实现：
    # HttpResponse(json.dumps(result), content_type='application/json')
    return JsonResponse(result)

def get_page_data(ojb, p, page_count=10):
    """
    封装Django的内置分页功能
    :param ojb: 分页对象，列表或者模型
    :param p: 页数，获取当前页数对应的数据
    :param page_count: 每页的数据量，默认一页10行数据
    """
    previous, next = 0, 0
    # orphans:最后一页允许最少的剩余条数
    ps = Paginator(ojb, page_count, 0)
    try:
        pages = ps.page(p)
    except PageNotAnInteger:
        # 如果参数p不是整型，返回第一页的数据
        pages = ps.get_page(1)
    except EmptyPage:
        # 如果用户访问的页数大于实际页数，那么就返回最后一页的数据
        pages = ps.get_page(ps.num_pages)
    if pages.has_previous():
        previous = pages.previous_page_number()
    if pages.has_next():
        next = pages.next_page_number()
    count = ps.count
    # 将分页对象转换为列表返回
    pages = pages.object_list
    return pages, count, previous, next
