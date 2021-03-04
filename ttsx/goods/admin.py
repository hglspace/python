from django.contrib import admin

# Register your models here.
from goods.models import GoodsInfo

class GoodsInfoAdmin(admin.ModelAdmin):
    # list_display = ['id','商品名称','商品价格','商品描述']
    list_display = ['id', 'goods_name', 'goods_price', 'goods_desc']
    list_per_page = 10
admin.site.register(GoodsInfo,GoodsInfoAdmin)
