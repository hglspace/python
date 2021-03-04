import time

from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from cart.models import OrderInfo, OrderGoods
from goods.models import GoodsInfo


def add_cart(request):
    goods_id = request.GET.get('id','')
    if goods_id:
        prev_url = request.META['HTTP_REFERER']
        response = redirect(prev_url)
        goods_count = request.COOKIES.get(goods_id)
        if goods_count:
            goods_count = int(goods_count) + 1
        else:
            goods_count = 1
        response.set_cookie(goods_id,goods_count)
    return response

def show_cart(request):
    cart_goods_list = []
    cart_goods_count = 0
    cart_goods_money = 0
    for goods_id,goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id = goods_id)
        cart_goods.goods_num = goods_num
        cart_goods.total_money = int(goods_num) * cart_goods.goods_price
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)
        cart_goods_money += int(goods_num) * cart_goods.goods_price
    return render(request,'cart.html',{'cart_goods_list':cart_goods_list,
                                       'cart_goods_count':cart_goods_count,
                                       'cart_goods_money':cart_goods_money})

def remove_cart(request):
    goods_id = request.GET.get('id', '')
    if goods_id:
        prev_url = request.META['HTTP_REFERER']
        response = redirect(prev_url)
        goods_count = request.COOKIES.get(goods_id,'')
        if goods_count:
            response.delete_cookie(goods_id)
    return  response

def place_order(request):
    cart_goods_list = []
    cart_goods_count = 0
    cart_goods_money = 0
    for goods_id,goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id = goods_id)
        cart_goods.goods_num = goods_num
        cart_goods.total_money = int(goods_num) * cart_goods.goods_price
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)
        cart_goods_money += int(goods_num) * cart_goods.goods_price
    return render(request,'place_order.html',{'cart_goods_list':cart_goods_list,
                                       'cart_goods_count':cart_goods_count,
                                       'cart_goods_money':cart_goods_money})

def submit_order(request):
    # 获得订单信息
    addr = request.POST.get('addr', '')
    recv = request.POST.get('recv', '')
    tele = request.POST.get('tele', '')
    extra = request.POST.get('extra', '')

    # 保存订单信息
    order_info = OrderInfo()
    order_info.order_addr = addr
    order_info.order_tele = tele
    order_info.order_recv = recv
    order_info.order_extra = extra

    # 生成订单编号
    order_info.order_id = str(int(time.perf_counter() * 1000)) + str(int(time.perf_counter() * 1000000))
    order_info.save()

    # 跳转页面
    response = redirect('/cart/submit_success/?id=%s' % order_info.order_id)

    # 保存订单商品信息
    for goods_id, goods_num in request.COOKIES.items():
        if goods_id == 'csrftoken':
            continue
        # 查询商品信息
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        # 创建订单商品信息
        order_goods = OrderGoods()
        order_goods.goods_info = cart_goods
        order_goods.goods_order = order_info
        order_goods.goods_num = goods_num
        order_goods.save()
        # 删除购物车信息
        response.delete_cookie(goods_id)
    return response

def submit_success(request):
    """显示订单结果"""

    order_id = request.GET.get('id')

    order_info = OrderInfo.objects.get(order_id=order_id)
    order_goods_list = OrderGoods.objects.filter(goods_order=order_info)

    # 商品总价
    total_money = 0
    # 商品总数量
    total_num = 0
    for goods in order_goods_list:
        goods.total_money = goods.goods_num * goods.goods_info.goods_price
        total_money += goods.total_money
        total_num += goods.goods_num

    return render(request, 'success.html', {'order_info': order_info,
                                            'order_goods_list': order_goods_list,
                                            'total_money': total_money,
                                            'total_num': total_num})