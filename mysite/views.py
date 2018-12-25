from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
# Create your views here.
from .models import Goods, Users
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import NameForm, ContackForm, FileMailForm, TextEmailForm
import json
from django.views.decorators.csrf import csrf_exempt
from web import settings
import os
from django.core.mail import EmailMultiAlternatives


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


def change(request):
    return render(request, 'change.html')


def changepass(request):
    user_name = request.GET['user_name']
    password = request.GET['password']
    user = Users.objects.filter(user_name=user_name)
    try:
        user.update(password=password)
        status = 200
    except:
        status = 100
    print(status)
    return  HttpResponse(json.dumps({'status': status}))


def goodslist(request):
    result = Goods.objects.all()
    return render(request, 'goods_list.html', {'goods_list': result})


def add(request):
    goods_name = request.GET['goods_name']
    goods_price = request.GET['goods_price']
    goods_number = request.GET['goods_number']
    isexist = Goods.objects.filter(goods_name=goods_name)
    try:
        if not isexist:
            goods = Goods()
            goods.goods_name = goods_name
            goods.goods_price = goods_price
            goods.goods_number = goods_number
            goods.save()
            result = 200
        else:
            result = 100
    except:
        result = 100
    return HttpResponse(result)


def delete(request):
    goods_name = request.GET['goods_name']
    goods = Goods.objects.filter(goods_name=goods_name)
    try:
        goods.delete()
        result = 200
    except:
        result = 100
    return HttpResponse(result)


def search(request):
    min_price = int(request.GET['min_price'])
    max_price = int(request.GET['max_price'])
    goods = Goods.objects.filter(goods_price__gte=min_price, goods_price__lte=max_price)
    try:
        if goods:
            result = json.dumps(serializers.serialize('json', goods))
        else:
            result = 100
    except:
        result = 100
    return HttpResponse(result)


@csrf_exempt
def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = NameForm()
    return render(request, 'name.html', {'form': form})


def thanks(request):
    return render(request, 'thanks.html')


def write_email(request):
    form = FileMailForm()
    return render(request, 'email.html', {'email_form':form})


def upload_handler(file, file_name):
    path = os.path.join(settings.BASE_DIR, 'uploads/')
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + file_name, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return path + file_name


def file_email_send(subject, message,sender, addresses, file):
    email = EmailMultiAlternatives(subject, message, sender, addresses)
    file_path = upload_handler(file, str(file))
    email.attach_file(file_path)
    email.send()


def send_email(request):
    if request.method == 'POST':
        if request.FILES:
            email_form = FileMailForm(request.POST, request.FILES)
            file = request.FILES['file']
        else:
            email_form = TextEmailForm(request.POST)
            file = None
        if email_form.is_valid():
            addresses = email_form.cleaned_data['addressees'].split(',')
            subject = email_form.cleaned_data['subject']
            message = email_form.cleaned_data['message']
            cc_myself = email_form.cleaned_data['cc_myself']
            if cc_myself:
                addresses.append(settings.EMAIL_HOST_USER)
            count = len(addresses)
            email = [subject, message, settings.DEFAULT_FROM_EMAIL, addresses]
            try:
                if file:
                    file_email_send(*email, file)
                    file_name = "(附件: {})".format(str(file))
                else:
                    if count > 1:
                        for item in addresses:
                            email1 = [subject, message, settings.DEFAULT_FROM_EMAIL, item]
                            send_email(*email1)
                    else:
                        send_email(*email)
                    file_name = ''
            except:
                return HttpResponse('send fail')
            return render(request, 'thanks.html', {'count':count,'to': addresses, 'file': file_name})
        else:
            return HttpResponse('check failed')
    else:
        email_form = FileMailForm()
        return render(request,'email.html',{'email_form': email_form})


def index1(request):
    if request.session.get('username',None):
        # return render(request, 'index1.html', {'username': request.COOKIES['username']})
        # return render(request, 'index1.html',  {'username': request.get_signed_cookie('username', salt='abcd')})
        return render(request, 'index1.html', {'username': request.session['username']})
    if request.method == 'POST':
        username = request.POST['username']
        request.session['username'] = username
        # res = render(request, 'index1.html', {'username': username})
        # # res.set_cookie('username', username, 3)
        # res.set_signed_cookie('username', username, salt='zbcd')
        # return res
        return render(request, 'index1.html', {'username':username})
    else:
        return render(request,'index1.html')


def exit(request):
    del request.session['username']
    res = HttpResponseRedirect('/index1')
    # res.delete_cookie('username')
    return res