from django.urls import path
from .views import *


urlpatterns = [
    path('.html', commodityView, name='commodity'),
    path('/detail.<int:id>.html', detailView, name='detail'),
    path('/collect.html',collectView,name='collect'),
]