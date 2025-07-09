import string
import time
import random
from statistics import quantiles

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from commodity.models import CommodityInfos
from shopper.form import LoginForm, LoginModelForm
from shopper.models import OrderInfos, CartInfos
from shopper.pays import get_pay


# Create your views here.

@login_required(login_url='/shopper/login.html')
def shopperView(request):
    """
    Django内置装饰器@login_required设置用户登录访问权限
    如果用户在没有登录的情况下访问个人中心，程序会自动跳转到指定的路由
    只有完成登录后才可以正常访问个人中心
    """
    title = "个人中心"
    classContent = 'informations'
    # 变量t，来自请求参数t，代表用户购买商品的支付时间
    t = request.GET.get('t', '')
    p = request.GET.get('p', 1)
    # 获取payTime
    payTime = request.session.get('payTime', '')
    if t and payTime and t == payTime:
        # 当两者都不为空且相等，则说明订单支付成功
        # 从会话获取订单的购买记录
        payInfo = request.session.get('payInfo', '')
        OrderInfos.objects.create(**payInfo)
        # 在会话Session中删除该订单的支付时间和订单内容
        del request.session['payInfo']
        del request.session['payTime']
    # 根据当前用户查询用户订单信息
    orderInfos = OrderInfos.objects.filter(user_id=request.user.id).order_by('-create')
    # 分页
    paginator = Paginator(orderInfos, 7)
    try:
        pages = paginator.page(p)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return render(request, 'shopper.html', locals())


def  loginView(request):
    """
    用户登录视图函数，处理用户登录请求，
    支持现有用户认证和新用户注册
    """
    # 定义变量title和classContent用于设置公用模板base.html的模板变量
    title = "用户登录"
    classContent = "logins"
    # 对用户的请求方式进行判断
    if request.method == "POST":
        # 实例化登录模型并绑定POST数据
        # infos = LoginForm(data= request.POST)
        infos = LoginModelForm(data= request.POST)
        # 验证表单字段的数据是否正确
        # if infos.is_valid():
        # 获取表单原始数据
        data = infos.data
        # 如果是POST请求，那么视图函数会执行注册和登录操作
        # 获取请求参数username和password
        username = data['username']
        password = data['password']
        # 查询username的数据是否存在于内置模型User
        if User.objects.filter(username=username):
            # 验证账号和密码是否与模型User中对应的一致
            user = authenticate(username=username, password=password)
            # 如果通过验证，使用内置函数login执行登录操作，登录成功后
            # 跳转到个人中心页面
            if user:
                login(request, user)
                return redirect(reverse('shopper:shopper'))
        else:
            # username不存在于内置模型User，执行注册
            state = "注册成功"
            d = dict(username=username, password=password, is_staff=1, is_active=1)
            user = User.objects.create_user(**d)
            user.save()
        # else:
        #     # 获取错误信息，并以JSON格式输出
        #     error_msg = infos.errors.as_json()
        #     print(error_msg)
    else:
        # 处理HTTP的GET请求
        # infos = LoginForm()
        infos = LoginModelForm()
    return render(request, 'login.html', locals())
def logoutView(request):
    # 调用Django的内置函数
    logout(request)
    # 网页重定向到首页
    return redirect(reverse('index:index'))

@login_required(login_url='/shopper/login.html')
def shopcartView(request):
    """
    定义购物车页面的业务逻辑
    管理购物车商品
    添加和更新商品数量
    """
    title = "我的购物车"
    classContent = "shopcarts"
    # 获取当前用户ID，因为我们设置了login_required，
    # 所以可以通过当前请求获取用户相关的信息
    userId = request.user.id
    # 获取商品id
    id = request.GET.get('id', '')
    # 获取商品数量
    quantity = request.GET.get('quantity', 1)
    # 判断id是否为空，如果不为空，那就说明当前的请求中有参数id和quantity
    # 证明是用户通过单击商品详情页的加入购物车按钮触发的，需要将id、quantity、userId
    # 添加到购物车的信息表中
    if id:
        CartInfos.objects.update_or_create(
            commodityInfos_id=id,
            user_id=userId,
            defaults={'quantity': quantity}
        )
        # 操作成功后，重定向到购物车页面
        return redirect('shopper:shopcart')
    # 获取当前用户的购物车记录
    getUserId = CartInfos.objects.filter(user_id=userId)
    # 构建商品ID到数量的映射字典
    commodityDict = {x.commodityInfos_id : x.quantity for x in getUserId}
    # 根据商品ID查询商品信息
    commodityInfos = CommodityInfos.objects.filter(id__in=commodityDict.keys())
    return render(request, 'shopcart.html', locals())

def deleteAPI(request):
    """
    购物车删除API视图函数
    处理购物车的删除商品请求，支持按用户删除和按商品id删除
    """
    # 作为HTTP响应内容，如果state是success，那么说明成功删除
    # 如果state是fail，说明删除失败
    result = {'state': 'success'}
    # 获取用户id，如果不存在参数userId,那么变量userId设为空字符
    userId = request.GET.get('userId', '')
    # 获取商品id
    commodityId = request.GET.get('commodityId', '')
    if userId:
        # userId不为空，则删除全部商品
        CartInfos.objects.filter(user_id=userId).delete()
    elif commodityId:
        # 如果userId为空，则判断commodityId是否为空
        # 如果不为空说明是删除某一个商品
        CartInfos.objects.filter(commodityInfos_id=commodityId).delete()
    else:
        # 如果两个id都为空，说明请求没有设置任何参数，当前请求不是删除商品操作
        result= {'state': 'fail'}
    # 返回JSON格式的结果作为当前HTTP响应的内容
    return JsonResponse(result)

def paysView(request):
    """
    支付视图函数，生成支付宝支付链接，处理支付前的订单信息准备
    """
    # 从请求中获取请求参数total（支付金额参数）
    total = request.GET.get('total', 0)
    # 去掉货币符号
    total = total.replace('￥', '')
    # 金额格式的验证
    try:
        # 如果total为空或者0，说明的当前购物车应付金额为0
        # 或者HTTP请求没有设置请求参数，可以直接重新访问购物车页面
        total = float(total)
    except ValueError:
        return redirect('shopper:shopcart')
    if total > 0:
        # 用户正在结算操作
        # 生成安全的订单编号
        timestamp = int(time.time() * 1000)
        random_str = "".join(random.choices(string.digits, k=6))
        out_trade_no = f"{timestamp}{random_str}"
        # 格式化金额为两位的小数
        total_amount = "{:.2f}".format(total)
        # 准备订单信息，并且存入会话中，支付成功后会创建订单
        payInfo = dict(price=total, user_id=request.user.id, state="已支付")
        request.session['payInfo'] = payInfo
        # 存储订单号主要用来回调验证
        request.session['payTime'] = out_trade_no
        # 构建回调的URL
        domain = 'http://' + request.get_host()
        return_url = f"{domain}/shopper/pay_callback/"
        # 打印一些调试信息
        print(f"out_trade_no: {out_trade_no}, type: {type(out_trade_no)}")
        print(f"total_amount: {total_amount},type: {type(total_amount)}")
        print(f"return_url: {return_url}, type: {type(return_url)}" )
        # 获取支付宝的支付链接
        url = get_pay(out_trade_no, total_amount, return_url)
        print("支付宝支付链接:", url)
        # 重定向到支付页面或者返回错误
        if url:
            return redirect(url)
        else:
            return redirect('shopper:shopcart')
    else:
        return redirect('shopper:shopcart')

def payCallbackView(request):
    """
    处理支付回调逻辑，可以做一些验证支付结果等操作
    """
    payTime = request.session.get('payTime', '')
    if payTime:
        payInfo = request.session.get('payInfo', '')
        if payInfo:
            OrderInfos.objects.create(**payInfo)
            # 删除session中的信息
            del request.session['payInfo']
            del request.session['payTime']
    # 跳转个人中心
    return redirect(reverse('shopper:shopper'))