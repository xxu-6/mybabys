"""
URL configuration for mybabys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path('media/(?P<path>.*)',serve,{'document_root': settings.MEDIA_ROOT},name='media'),
    path('', include(('index.urls','index'), namespace='index')),
    path('shopper', include(('shopper.urls','shopper'), namespace='shopper')),
    path('commodity', include(('commodity.urls','commodity'), namespace='commodity')),
    #path('api/v1/commodity/',include(('commodity.urls', 'commodity'), namespace='commodity')),

]
from index import views
handler404=views.page_not_found
handler500=views.page_error