# -*- coding: utf-8 -*-
# @Time : 2018/12/25 15:44
# @Author : chenpeng
# @Site : pengguoko@163.com
# @File : context_processor.py


def getuserip(request):
	ip = request.META['REMOTE_ADDR']
	if ip == '127.0.0.1':
		return {'user_type': '本机用户'}
	return {'user_type': '外部用户(%s)' % ip}