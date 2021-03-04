from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from goods.models import GoodsCategory, GoodsInfo


def index(request):

    categories = GoodsCategory.objects.all()
    for cag in categories:
       #  一对多关系，查询多的一方, 会在一的这一方有一个属性，多的一方的模型类名小写_set
       # GoodsInfo.objects.filter(goods_cag = cag)
        cag.goods_list = cag.goodsinfo_set.order_by('-id')[:4]
    cart_goods_list = []
    cart_goods_count = 0
    for goods_id,goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id = goods_id)
        cart_goods.goods_num = goods_num
        cart_goods_list.append(cart_goods)
        carg_goods_count = cart_goods_count + int(goods_num)

    return render(request,'index.html',{'categories':categories,
                                        'cart_goods_list':cart_goods_list,
                                        'cart_goods_count':cart_goods_count})

def detail(request):
    categories = GoodsCategory.objects.all()
    cart_goods_list = []
    cart_goods_count = 0
    for goods_id,goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods=GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)
    goods_id = request.GET.get('id',1)
    goods_data = GoodsInfo.objects.get(id = goods_id)
    return render(request,'detail.html',{'categories':categories,
                                         'cart_goods_list':cart_goods_list,
                                         'cart_goods_count':cart_goods_count,
                                         'goods_data':goods_data})

def goods(request):
    cag_id = request.GET.get('cag', '1')

    page_id = request.GET.get('page', '1')
    current_cag = GoodsCategory.objects.get(id=cag_id)
    # current_cag.goodsinfo_set.all()
    # GoodsInfo.objects.filter(goods_cag = current_cag)
    goods_data = GoodsInfo.objects.filter(goods_cag_id = cag_id)
    # 实例化Paginator分页器对象，参1是需要分页的数据，参2是每一页显示的数量
    paginator = Paginator(goods_data,12)
    page_data = paginator.page(page_id)
    categories = GoodsCategory.objects.all()
    cart_goods_list = []
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)
    return render(request,'goods.html',{'current_cag':current_cag,
                                        'page_data':page_data,
                                        'cart_goods_list':cart_goods_list,
                                        'cart_goods_count':cart_goods_count,
                                        'categories':categories,
                                        'paginator':paginator,
                                        'cag_id':cag_id})