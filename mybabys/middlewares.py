from django.http import HttpResponseRedirect
class PrintHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("请求头信息：", request.headers)
        response = self.get_response(request)
        return response


class CheckLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 仅对特定路径验证登录
        if request.path.startswith('/cart/') or request.path.startswith('/order/'):
            if not request.user.is_authenticated:
                return HttpResponseRedirect('/login/')
        response = self.get_response(request)
        return response

class PrintIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        print("请求 IP 地址：", ip)
        response = self.get_response(request)
        return response
