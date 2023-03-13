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

from takeaway.models import Food, UserProfile, Wallet


class IndexView(View):
    def get(self, request):
        # Query the database for a list of ALL foods currently stored.
        food_list = Food.objects.all()

        context_dict = {'foods': food_list[1:],
                        'special_food': food_list[0]}

        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.
        return render(request, 'takeaway/index.html', context=context_dict)
    
    def product(request):
        context_dict = {}
        context_dict['boldmessage'] = 'product!'
        return render(request, 'takeaway/product.html', context=context_dict)


class AccountView(View):

    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        wallet = Wallet.objects.get_or_create(user=user)[0]

        return user, user_profile, wallet

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, wallet) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('takeaway:index'))

        context_dict = {'user': user,
                        'user_profile': user_profile,
                        'wallet': wallet,
                        }
        return render(request, 'takeaway/account.html', context_dict)


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
