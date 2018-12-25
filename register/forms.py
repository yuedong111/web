# -*- coding: utf-8 -*-
# @Time : 2018/12/25 13:52
# @Author : chenpeng
# @Site : pengguoko@163.com
# @File : forms.py

from django import forms
from register import models


class RegisterForm(forms.ModelForm):
	class Meta:
		model = models.UserModel
		fields = '__all__'
		widgets = {
			'password': forms.PasswordInput()
		}