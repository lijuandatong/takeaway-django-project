from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from takeaway.models import Food, UserProfile, Wallet, Cart, CartDetail, Order, OrderDetail, Comment,Checkout
import sqlite3


from django.http import JsonResponse
from .forms import CheckoutForm
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


def AddComment(request):
    if request.method == 'POST':
        form = Comment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('takeaway/review.html', pk=comment.article.pk)
    else:
        form = Comment()
    return render(request, 'takeaway/review.html', {'form': form})


class ChargeView(View):
    def get(self, request):
        username = request.GET['username']
        #amount = request.GET['amount']

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
        username = request.GET['username']
        food_id = request.GET['food_id']
        count = request.GET['count']
        if count is None:
            count = 1

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        try:
            food = Food.objects.get(food_id=food_id)
        except Food.DoesNotExist:
            return None

        cart = Cart.objects.get_or_create(user=user)[0]
        cart.save()

        cart_detail = CartDetail.objects.get_or_create(cart=cart, food=food)[0]
        cart_detail.count = cart_detail.count + int(count)
        cart_detail.save()

        cart_detail_list = CartDetail.objects.filter(cart=cart)
        total_count = 0
        for cart_detail in cart_detail_list:
            total_count += cart_detail.count

        return HttpResponse(str(total_count))


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
    context_dict = {'bold message': 'product!'}
    return render(request, 'takeaway/product.html', context=context_dict)


def user_checkout(request):
    context_dict = {}
    context_dict['boldmessage'] = 'checkout page!'

    return render(request, 'takeaway/checkout.html', context=context_dict)


def user_cart(request):
    context_dict = {}
    context_dict['boldmessage'] = 'cart page!'

    return render(request, 'takeaway/cart.html', context=context_dict)






class checkout_save_data(View):
    def get(self, request):
        
        first_name = request.GET['first_name']
        last_name = request.GET['last_name']
        address = request.GET['address']
        city = request.GET['city']
        zipcode = request.GET['zipcode']
        email = request.GET['email']
        phone = request.GET['phone']

        # Create a new customer object with the retrieved information
        checkout = Checkout.objects.create(first_name=first_name, last_name=last_name, address=address,
                            city=city, zipcode=zipcode, email=email, phone=phone)[0]

        # Save the customer object to the database
        checkout.save()
        messages.success(request, 'Order placed successfully.')

        # Return a JSON response indicating success
        response = {'success': True}
        return JsonResponse(response)

   