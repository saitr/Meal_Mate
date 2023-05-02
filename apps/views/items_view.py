from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail,EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.models import *


# def item_list(request):
#     user = request.user
#     if user.is_authenticated and user.is_logged_in or user.is_superuser:
#         items = Items.objects.all()
#         categories = Categories.objects.all()
#         cart_items = Cart.objects.filter(user=request.user)
#         # available_items = [item for item in items if item.is_available]

#         # above line with normal for loop 

#         # available_items = []
#         # for item in items:
#         #     if item.is_available:
#         #         available_items.append(item)

#         context = {'items': items,'categories': categories,'cart_items': cart_items}
#         return render(request, 'home.html', context)
#     else: 
#         return redirect('signin')

def item_list(request):
    user = request.user
    if user.is_authenticated and user.is_logged_in or user.is_superuser:
        items = Items.objects.all()
        categories = Categories.objects.all()
        cart_items = Cart.objects.filter(user=request.user)
        
        cart_dict = {item.item_id: item for item in cart_items}  # build dictionary

        context = {'items': items, 'categories': categories, 'cart_dict': cart_dict}
        return render(request, 'home.html', context)
    else: 
        return redirect('signin')

    



######################## To make the items available ################################


def make_item_available(request):
    item_id = request.GET.get('item_id')
    item = Items.objects.get(id=item_id)
    item.is_available = True
    item.save()
    return redirect('home')

def make_item_unavailable(request):
    item_id = request.GET.get('item_id')
    item = Items.objects.get(id=item_id)
    item.is_available = False
    item.save()
    return redirect('home')


################### Filterning of the items with the categories ######################

def filter_items(request, category_id):
    category = Categories.objects.get(pk=category_id)
    items = Items.objects.filter(category=category, is_available=True)
    categories = Categories.objects.all()
    context = {'items': items, 'categories': categories}
    return render(request, 'home.html', context)








