from django import template
from django.contrib.auth.models import User

from takeaway.models import Cart, CartDetail

register = template.Library()


@register.inclusion_tag('takeaway/header.html')
def getCartCount(user=None):
    cart_count = 0

    if user.is_authenticated:
        print("user登录了：" + user.username)

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            print("购物车发生异常")
            cart_count = 0
            return {'cart_count': cart_count,
                    'user': user}

        cart_detail_list = CartDetail.objects.filter(cart=cart)
        for cart_detail in cart_detail_list:
            cart_count += cart_detail.count

        print("购物车数量：" + str(cart_count))

    return {'cart_count': cart_count,
            'user': user}

