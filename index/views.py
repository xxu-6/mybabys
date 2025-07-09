from django.shortcuts import render
from django.views.generic import TemplateView

from commodity.models import CommodityInfos, Types


# Create your views here.
def indexView(request):
    title="首页"
    classContent=""
    commodityInfos=CommodityInfos.objects.order_by("-sold").all()[:8]
    types=Types.objects.all()

    c1=[x.seconds for x in types if x.firsts=='儿童服饰']
    clothes=CommodityInfos.objects.filter(types__in=c1).order_by("-sold").order_by('-sold')[:5]

    f1=[x.seconds for x in types if x.firsts=='奶粉辅食']
    food=CommodityInfos.objects.filter(types__in=f1).order_by("-sold").order_by('-sold')[:5]

    g1=[x.seconds for x in types if x.firsts=='儿童用品']
    goods=CommodityInfos.objects.filter(types__in=g1).order_by("-sold").order_by('-sold')[:5]

    return render(request, 'index.html', locals())

class indexClassView(TemplateView):
    template_name="index.html"
    template_engine= None
    content_type=None
    extra_context={'title':'首页','classContent':''}
    def get_context_data(self, **kwargs):
        context=super(indexClassView,self).get_context_data(**kwargs)
        context['commodityInfos']=CommodityInfos.objects.order_by("-sold").all()[:8]
        types = Types.objects.all()
        c1 = [x.seconds for x in types if x.firsts == '儿童服饰']
        context['clothes']= CommodityInfos.objects.filter(types__in=c1).order_by("-sold").order_by('-sold')[:5]
        f1 = [x.seconds for x in types if x.firsts == '奶粉辅食']
        context['food']= CommodityInfos.objects.filter(types__in=f1).order_by("-sold").order_by('-sold')[:5]
        g1 = [x.seconds for x in types if x.firsts == '儿童用品']
        context['goods'] = CommodityInfos.objects.filter(types__in=g1).order_by("-sold").order_by('-sold')[:5]
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

def page_not_found(request, exception):
    return render(request, '404.html',status=404)

def page_error(request):
    return render(request, '404.html',status=500)
