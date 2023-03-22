from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from takeaway.models import Food, UserProfile, Wallet, Cart, CartDetail, Order, OrderDetail, Comment
import sqlite3

from django.http import JsonResponse
from django.contrib import messages


class IndexView(View):
    def get(self, request):
        cart_count = 0

        if request.user.is_authenticated:
            print("用户登录了")
            cart_count = getCartCount(request.user)

        # Query the database for a list of ALL foods currently stored.
        food_list = Food.objects.all()

        context_dict = {'foods': food_list[1:],
                        'special_food': food_list[0],
                        'cart_count': cart_count}

        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.
        return render(request, 'takeaway/index.html', context=context_dict)


class AccountView(View):

    def get_user_details(self, username):
        print('get detials 函数进入')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        wallet = Wallet.objects.get_or_create(user=user)[0]

        return user, user_profile, wallet

    @method_decorator(login_required)
    def get(self, request, username):
        print('get函数进入')
        try:
            (user, user_profile, wallet) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('takeaway:index'))

        context_dict = {'user': user,
                        'user_profile': user_profile,
                        'wallet': wallet,
                        }
        return render(request, 'takeaway/account.html', context_dict)


class OrderView(View):

    def get_order(self, username):
        print('get detials 函数进入')
        try:
            user = User.objects.get(username=username)
            order = Order.objects.filter(user=user)
            # orderdetail = []
            # for i in len(order):
            #     orderdetail.append(OrderDetail.objects.filter(order=order[i]))
            # orderdetail = OrderDetail.objects.filter(order=order[1])
            orderdetail = OrderDetail.objects.all()
        except User.DoesNotExist:
            return None
        except Order.DoesNotExist:
            return None
        except OrderDetail.DoesNotExist:
            return None

        return user, order, orderdetail

    @method_decorator(login_required)
    def get(self, request, username):
        print('get函数进入')
        try:
            (user, order, orderdetail) = self.get_order(username)
        except TypeError:
            return redirect(reverse('takeaway:index'))

        context_dict = {'user': user,
                        'orders': order[:],
                        'orderdetails': orderdetail[:],
                        }
        return render(request, 'takeaway/order_history.html', context_dict)


class OrderDetailsView(View):

    def get_order_details(self, order_id):
        print('get detials 函数进入')

        try:
            order = Order.objects.get(order_id=order_id)
            orderdetail = OrderDetail.objects.filter(order=order)
        except Order.DoesNotExist:
            return None
        except OrderDetail.DoesNotExist:
            return None

        return order, orderdetail

    @method_decorator(login_required)
    def get(self, request, order_id):
        print('get函数进入')
        try:
            (order, orderdetail) = self.get_order_details(order_id)
        except TypeError:
            return redirect(reverse('takeaway:index'))

        context_dict = {'order': order,
                        'orderdetails': orderdetail[:],
                        }
        return render(request, 'takeaway/review.html', context_dict)


class ReviewView(View):
    def get(self, request):
        # print(request.get())
        username = request.GET['username']
        comment = request.GET['review']
        try:
            user = User.objects.get(username=username)
            # food = Food.objects.get(comment=comment)
            food_id = '002'
            food = Food.objects.get(food_id=food_id)
        except User.DoesNotExist:
            return None
        except Food.DoesNotExist:
            return None

        review = Comment.objects.create(comment=comment, user=user, food=food)
        review.save()

        return HttpResponse(review.comment)


class ChargeView(View):
    def get(self, request):
        username = request.GET['username']
        amount = request.GET['amount']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        wallet = Wallet.objects.get_or_create(user=user)[0]
        wallet.cash = wallet.cash + float(amount)
        wallet.save()

        return HttpResponse(wallet.cash)


class AddCartView(View):
    def get(self, request):
        food_id = request.GET['food_id']
        count = request.GET['count']
        if count is None:
            count = 1

        try:
            food = Food.objects.get(food_id=food_id)
        except Food.DoesNotExist:
            return None

        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart.save()

        cart_detail = CartDetail.objects.get_or_create(cart=cart, food=food)[0]
        cart_detail.count = cart_detail.count + int(count)
        cart_detail.total_price = food.discounted_price * cart_detail.count
        cart_detail.total_discount = (food.price - food.discounted_price) * cart_detail.count
        cart_detail.save()

        cart_detail_list = CartDetail.objects.filter(cart=cart)
        total_count = 0
        for cart_detail in cart_detail_list:
            total_count += cart_detail.count

        return HttpResponse(str(total_count))


class MinusQuantityFromCart(View):
    def get(self, request):
        food_id = request.GET['food_id']

        try:
            food = Food.objects.get(food_id=food_id)
        except Food.DoesNotExist:
            return None

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return None

        cart_detail = CartDetail.objects.get(cart=cart, food=food)
        cart_detail.count = cart_detail.count - 1
        cart_detail.total_price = food.discounted_price * cart_detail.count
        cart_detail.total_discount = (food.price - food.discounted_price) * cart_detail.count
        cart_detail.save()

        cart_detail_list = CartDetail.objects.filter(cart=cart)
        total_count = 0
        for cart_detail in cart_detail_list:
            total_count += cart_detail.count

        return HttpResponse(str(total_count))


class RemoveFoodFromCart(View):
    def get(self, request):
        print("购物车移除商品")
        cart_detail_id = request.GET['cart_detail_id']
        CartDetail.objects.get(id=cart_detail_id).delete()

        return HttpResponse()


def getCartCount(user):
    cart_count = 0

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return cart_count

    cart_detail_list = CartDetail.objects.filter(cart=cart)
    for cart_detail in cart_detail_list:
        cart_count += cart_detail.count

    return cart_count


def product(request):
    food_id = '002'
    food = Food.objects.get(food_id=food_id)
    address = food.address
    comments = Comment.objects.filter(food=food)
    context_dict = {'bold message': 'product!', 'address': address, 'comments': comments, 'food': food}
    return render(request, 'takeaway/product.html', context=context_dict)


class CartView(View):
    @method_decorator(login_required)
    def get(self, request):
        print("购物车页面进入")
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return None

        cart_detail_list = CartDetail.objects.filter(cart=cart)

        total_price = 0
        total_discount = 0
        for cart_detail in cart_detail_list:
            print("购物车里的商品为：" + cart_detail.food.title)
            total_price += cart_detail.total_price
            total_discount += cart_detail.total_discount

        context_dict = {'cart_id': cart.cart_id,
                        'cart_detail_list': cart_detail_list,
                        'total_price': total_price,
                        'total_discount': total_discount}
        return render(request, 'takeaway/cart.html', context_dict)


class CheckoutView(View):
    @method_decorator(login_required)
    def get(self, request, cart_id):
        # 下单并进入支付页面
        order = Order.objects.get_or_create(user=request.user)[0]
        # "0"未支付 "1"支付
        order.delivery_state = "0"
        order.save()
        print("下单成功,orderid为：" + str(order.order_id))

        cart = Cart.objects.get(cart_id=cart_id)
        cart_detail_list = CartDetail.objects.filter(cart=cart)

        total_price = 0
        total_discount = 0

        for cart_detail in cart_detail_list:
            order_detail = OrderDetail.objects.get_or_create(order=order, food=cart_detail.food)[0]
            order_detail.count = cart_detail.count
            order_detail.save()
            print("订单明细保存成功，food为：" + str(order_detail.food.food_id))

            total_price += cart_detail.total_price
            total_discount += cart_detail.total_discount

        print("下单页面进入")

        wallet = Wallet.objects.get_or_create(user=request.user)[0]
        cash = wallet.cash
        points = wallet.points

        context_dict = {'order_id': order.order_id,
                        'total_price': total_price,
                        'total_discount': total_discount,
                        'cash': cash,
                        'points': points}

        return render(request, 'takeaway/checkout.html', context_dict)


class PlaceOrder(View):
    def get(self, request):
        first_name = request.GET['first_name']
        last_name = request.GET['last_name']
        street = request.GET['address']
        city = request.GET['city']
        zipcode = request.GET['zipcode']
        email = request.GET['email']
        phone = request.GET['phone']
        points = request.GET['payment_points']
        cash = request.GET['payment_cash']
        order_id = request.GET['order_id']

        # Create a new customer object with the retrieved information
        order = Order.objects.get(order_id=order_id)
        order.first_name = first_name
        order.last_name = last_name
        order.city = city
        order.zipcode = zipcode
        order.email = email
        order.phone = phone
        order.street = street
        if points == 0:
            order.payment = '￡' + str(cash)
        elif cash == 0:
            order.payment = str(points) + 'points'
        else:
            order.payment = '￡' + str(cash) + ' + ' + str(points) + ' points'

        print('存入的payment为：' + order.payment)
        order.delivery_state = "1"
        order.save()

        # 还要更新用户钱包数据

        response = {'success': True}
        return JsonResponse(response)
