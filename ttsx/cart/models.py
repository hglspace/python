from django.db import models

# Create your models here.
class OrderInfo(models.Model):

    status = (
        (1,'待付款'),
        (2,'待发货'),
        (3,'待收货'),
        (4,'已完成'),
    )

    order_id = models.CharField(max_length=100)
    order_addr = models.CharField(max_length=100)
    order_recv = models.CharField(max_length=50)
    order_tele = models.CharField(max_length=11)
    order_fee = models.IntegerField(default=10)
    order_extra = models.CharField(max_length=200)
    order_status = models.IntegerField(default=1,choices=status)

class OrderGoods(models.Model):

    goods_info = models.ForeignKey('goods.GoodsInfo')
    goods_num = models.IntegerField()
    goods_order = models.ForeignKey('orderInfo')