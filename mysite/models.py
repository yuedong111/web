from django.db import models

# Create your models here.


class Goods(models.Model):
    goods_name = models.CharField(max_length=30)
    goods_number = models.IntegerField()
    goods_price = models.FloatField()
    goods_sales = models.IntegerField('销量', default=0)

    class Meta:
        verbose_name_plural = "商品管理"
        verbose_name = "商品"

    def sales_volume(self):
        return self.goods_sales * self.goods_price

    sales_volume.short_description = '销售额'
    goods_amount = property(sales_volume)

    def __str__(self):
        return self.goods_name


class Users(models.Model):
    user_name = models.CharField(max_length=20,  primary_key=True)
    password = models.CharField(max_length=16)


class GoodsInfo(models.Model):
    goods_name = models.CharField(max_length=30, primary_key=True)
    goods_number = models.IntegerField()
    goods_price = models.FloatField()
