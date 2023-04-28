from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail,EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.models import *


def item_list(request):
    user = request.user
    if user.is_authenticated and user.is_logged_in or user.is_superuser:
        items = Items.objects.all()
        categories = Categories.objects.all()

        available_items = [item for item in items if item.is_available]

        # above line with normal for loop 

        # available_items = []
        # for item in items:
        #     if item.is_available:
        #         available_items.append(item)

        context = {'items': available_items,'categories': categories}
        return render(request, 'home.html', context)
    else: 
        return redirect('signin')
    



