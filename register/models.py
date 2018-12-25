from django.db import models

# Create your models here.


class UserModel(models.Model):
	email = models.EmailField('邮箱')
	password = models.CharField('密码', max_length=256)
	name = models.CharField('姓名', max_length=25)
	age = models.IntegerField('年龄')
	birthday = models.DateField('生日')
