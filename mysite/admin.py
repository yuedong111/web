from django.contrib import admin
from .models import Goods
# Register your models here.


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('goods_name','goods_number','goods_price','goods_sales','goods_amount')


admin.site.register(Goods,GoodsAdmin)
