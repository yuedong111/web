from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .models import Goods, Users
from django.db.models import Q
import json


def index(request):
    # return HttpResponse('中文site')
    return render(request, "index.html")


def news_lis(request, news_type):
    news_dict = {"economic": "经济", "sport": "体育"}
    news_titles = []
    if news_type == "economic":
        news_titles = [
            ("12/5", "作者成为全国首富。"),
            ("12/4", "作者成为全省首富。"),
            ("12/3", "作者成为全市首富。"),
            ("12/2", "作者成为镇里首富。"),
            ("12/1", "作者成为村里首富。"),
        ]
    return render(
        request,
        "news_list.html",
        {"news_type": news_dict[news_type], "news_titles": news_titles},
    )


def filter_test(request):
    return render(request, "filter.html", {"letters": "abc", "number": 1})


def searchall(request):
    goods_list = Goods.objects.all()
    return render(request, "search_result.html", {"goods_list": goods_list})


def searchname(request):
    goods_name = request.GET["goods_name"]
    goods_list = Goods.objects.filter(goods_name=goods_name)
    return render(request, "search_result.html", {"goods_list": goods_list})


def searchprice(request):
    min_price = request.GET["min_price"]
    max_price = request.GET["max_price"]
    goods_list = Goods.objects.filter(
        goods_price__gt=min_price, goods_price__lt=max_price
    )
    return render(request, "search_result.html", {"goods_list": goods_list})


def searchsort(request):
    sort = {
        "all_asc": Goods.objects.order_by("goods_price"),
        "all_desc": Goods.objects.order_by("-goods_price"),
        "result_asc": Goods.objects.filter(goods_price__lt="5").order_by("goods_price"),
    }
    return render(
        request, "search_result.html", {"goods_list": sort[request.GET["sort"]]}
    )


def reg(request):
    return render(request, "register.html")


def check(request):
    user_name = request.GET["user_name"]
    user = Users.objects.filter(user_name=user_name)
    if user:
        status = 100
    else:
        status = 200
    return HttpResponse(status)


def register(request):
    user_name = request.GET["user_name"]
    password = request.GET["password"]
    try:
        user = Users(user_name=user_name, password=password)
        user.save()
        status = 200
    except:
        status = 100
    return HttpResponse(json.dumps({"status": status}))
