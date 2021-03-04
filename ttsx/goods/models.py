from django.db import models

# Create your models here.
class GoodsCategory(models.Model):
    '''商品分类模型'''

    cagname = models.CharField(max_length=30)
    cag_css = models.CharField(max_length=20)
    cag_imag = models.ImageField(upload_to='cag')

class GoodsInfo(models.Model):

    goods_name = models.CharField(max_length=100,verbose_name='商品名称')
    goods_unit = models.CharField(max_length=50,verbose_name='商品单位')
    goods_price = models.IntegerField(default=0,verbose_name='商品价格')
    goods_img = models.ImageField(upload_to='goods')
    goods_desc = models.CharField(max_length=2000,verbose_name='商品描述')
    goods_cag = models.ForeignKey('GoodsCategory',verbose_name='商品分类')

    def __str__(self):
        return self.goods_name+',' + str(self.goods_price)