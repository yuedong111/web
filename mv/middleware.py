# -*- coding: utf-8 -*-
# @Time : 2018/12/25 15:59
# @Author : chenpeng
# @Site : pengguoko@163.com
# @File : middleware.py

from django.http import HttpResponseForbidden


class AaccessRestrictionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.wite_ip = ['127.0.0.1','192.168.31.18']  # 初始化ip地址白名单

    def __call__(self, request):
        ip = request.META['REMOTE_ADDR']  # 获取访问用户的ip
        if ip not in self.wite_ip:  # 如果ip不在白名单中
            return HttpResponseForbidden('您被禁止访问！')  # 返回响应
        response = self.get_response(request)
        return response