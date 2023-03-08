from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import redirect
from django.urls import reverse


def index(request):
    # return HttpResponse("Rango says hey there partner! <a href='/rango/about/'>About</a>")

    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.

    context_dict = {}
    context_dict['boldmessage'] = 'home page!'

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'takeaway/index.html', context=context_dict)


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('takeaway:index'))


def user_account(request):
    context_dict = {}
    context_dict['boldmessage'] = 'account page!'

    return render(request, 'takeaway/account.html', context=context_dict)
