# -*- coding: utf-8 -*-
# @Time : 2018/11/28 15:21
# @Author : chenpeng
# @Site : pengguoko@163.com
# @File : forms.py

from django import forms


class NameForm(forms.Form):
    user_name = forms.CharField(label='姓名', max_length=20)


class ContackForm(forms.Form):
    subject = forms.CharField(label='主题', label_suffix=':',
                              widget=forms.TextInput(attrs={'style': 'width:440px','maxlength':'100'}))
    message = forms.CharField(label='消息', label_suffix='：', widget=forms.Textarea(attrs={'cols': '60', 'rows': '10'}))
    sender = forms.EmailField(label='发送人', help_text='请输入正确的邮箱地址！', label_suffix='：')
    cc_myself = forms.BooleanField(label='是否抄送自己', label_suffix='：', required=False)


class FileMailForm(forms.Form):
    addressees = forms.CharField(label='收件地址', help_text='多个收件地址请用逗号“,”分隔', label_suffix='：',
                                 widget=forms.TextInput(attrs={'style': 'width:440px', 'maxlength': '100'}))
    subject = forms.CharField(label='邮件标题', label_suffix='：',
                              widget=forms.TextInput(attrs={'style': 'width:440px', 'maxlength': '100'}))
    message = forms.CharField(label='邮件内容', label_suffix='：', widget=forms.Textarea(attrs={'cols': '60', 'rows': '10'}))
    file = forms.FileField(label='添加附件', label_suffix='：')
    cc_myself = forms.BooleanField(label='抄送自己', label_suffix='：', required=False)


class TextEmailForm(FileMailForm):
    file = None