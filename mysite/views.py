from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    # return HttpResponse('中文site')
    return render(request,'index.html')


def news_lis(request, new_type):
    dic = {'economic':'经济','sport':'体育'}
    return render(request,'newlist.html',{'news_type':dic[new_type]})