from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail,EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.models import *
from apps.forms import OrderForm



############################ Order Page ##########################################


def checkout(request):
    if request.user.is_authenticated and request.user.is_logged_in or request.user.is_superuser:
        cart = Cart.objects.filter(user=request.user)
        form = OrderForm(user=request.user)

        # Calculate the subtotal for each item in the cart
        item_subtotals = []
        for cart_item in cart:
            quantity = cart_item.quantity
            total_price = cart_item.item.item_price * quantity
            item_subtotal = total_price
            item_subtotals.append(item_subtotal)

        total = sum(item_subtotals)

        if request.method == 'POST':
            form = OrderForm(request.POST,user=request.user)
            if form.is_valid():
                # Get form data
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                address = form.cleaned_data.get('address', request.user.address)
                zip_code = form.cleaned_data['zip_code']
                place = form.cleaned_data['place']
                payment_method = form.cleaned_data['payment_method']

                # Create the order
                order = Order.objects.create(user=request.user, first_name=first_name, last_name=last_name, address=address, zip_code=zip_code, place=place, payment_method=payment_method)

                # Create order items from cart items
                for cart_item in cart:
                    quantity = cart_item.quantity
                    total_price = cart_item.item.item_price * quantity
                    order_item = OrderItem.objects.create(order=order, item=cart_item.item, total_price=total_price, quantity=quantity)

                # Clear the cart
                cart.delete()

                return redirect('home')
        else:
            form = OrderForm(user=request.user)

        # Add total to the context dictionary
        context = {'cart_items': cart, 'form': form, 'item_subtotals': item_subtotals, 'total': total, 'total_price': total_price}

        return render(request, 'checkout.html', context)


