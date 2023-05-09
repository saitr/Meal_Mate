from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.models import *



############### Adding to the Cart ########################

def add_to_cart(request, item_id):
    # Check if user is authenticated
    if not request.user.is_authenticated and request.user.token and request.user.is_logged_in or request.user.is_superuser:
        return redirect('signin')

    # Retrieve the item from the database
    item = Items.objects.get(pk=item_id)

    # Check if the item is already in the user's cart
    cart_item, created = Cart.objects.get_or_create(item=item, user=request.user)
    if not created:
        # If the item already exists in the user's cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    # Redirect back to the previous page
    return redirect(request.META.get('HTTP_REFERER', 'home'))




##################### Cart List ######################### 


# def cart_list(request):
#     cart_list = Cart.objects.get(user= request.user)

#     if request.user.is_authenticated and request.user.token and  request.user.is_logged_in:
#         cart_list = Cart.objects.get(user= request.user)

#     return render(request,'cart.html',{'cart_list':cart_list})


def cart_list(request):
    if request.user.is_authenticated and request.user.token and request.user.is_logged_in or request.user.is_superuser:
        cart_items = Cart.objects.filter(user=request.user)
        subtotal = 0

        for item in cart_items:
            subtotal += item.item.item_price * item.quantity
            
        context = {'cart_items': cart_items,'subtotal': subtotal}
        return render(request, 'cart.html', context)
    else:
        return redirect('signin')



############################### Update Cart Items ###############################


def update_cart_item(request, item_id):
    # Check if user is authenticated
    if not request.user.is_authenticated and request.user.token and request.user.is_logged_in  or request.user.is_superuser:
        return redirect('signin')

    # Retrieve the cart item from the database
    cart_item = Cart.objects.get(pk=item_id, user=request.user)

    # Update the quantity based on the action parameter
    action = request.POST.get('action')
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            # If the quantity reaches 0, remove the item from the cart
            cart_item.delete()
            return redirect('cart_list')

    # Save the updated cart item
    cart_item.save()

    # Redirect to the cart page
    return redirect('cart_list')



