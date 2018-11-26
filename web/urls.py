"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from mysite.views import index, news_lis, filter_test
from mysite import views as siteviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('news_list/<str:news_type>', news_lis),
    path('filter/', filter_test),
    path('all/', siteviews.searchall),
    path('search_name/', siteviews.searchname),
    path('search_price/', siteviews.searchprice),
    path('search_sort/', siteviews.searchsort),
    path('reg/', siteviews.reg),  # 打开注册页面
    path('register/', siteviews.register),  # 提交注册
    path('check/', siteviews.check),  # 检查用户名是否注册
    # path('change/', siteviews.change),
    # path('changepass/', siteviews.changepass)
]

