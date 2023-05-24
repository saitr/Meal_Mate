from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail,EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.models import *
from apps.forms import SignUpForm,VerifyOTPForm,SignInForm,ChangeUserDetails, SubscribersForm


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

def item_list(request, category_id=None):
    user = request.user
    if user.is_authenticated and (user.is_logged_in or user.is_superuser):
        cart_count = Cart.objects.filter(user=request.user).count()
        categories = Categories.objects.all()
        selected_category = None

        if category_id:
            selected_category = Categories.objects.get(pk=category_id)
            items = Items.objects.filter(category=selected_category)
        else:
            items = Items.objects.all()

        cart_items = Cart.objects.filter(user=request.user)
        cart_dict = {item.item_id: item for item in cart_items}

        if request.method == 'POST':
            form = SubscribersForm(request.POST)
            print('this is the subscriber form', form)
            if form.is_valid():
                subscriber_email = form.cleaned_data['subscriber_email']
                # print('this is the subscriber form input email', subscriber_email)

                # Check if subscriber with the same email already exists
                if SubscriberModel.objects.filter(subscriber_email=subscriber_email).exists():
                    form.add_error('subscriber_email', 'You are already subscribed')
                else:
                    # Create the new subscriber if it's a unique email
                    subscriber = SubscriberModel.objects.create(
                        subscriber_email=subscriber_email
                    )
                    print('this is the subscriber email', subscriber)

                    # Send the thanks email to the subscriber
                    subject = 'Thanks For Subscribing'
                    message = "Thanks for choosing to become an active member. You are now in the list of people who don't miss the opportunity to grab good deals."
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [subscriber_email]
                    send_mail(subject, message, from_email, recipient_list)

                    return redirect('home')
        else:
            form = SubscribersForm()

        form_context = {'form': form}
        context = {'items': items, 'categories': categories, 'cart_dict': cart_dict, 'selected_category': selected_category, 'cart_count': cart_count, 'form_context': form_context}
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

# def filter_items(request, category_id):
#     category = Categories.objects.get(pk=category_id)
#     items = Items.objects.filter(category=category, is_available=True)
#     categories = Categories.objects.all()
#     context = {'items': items, 'categories': categories}

#     return render(request, 'home.html', context)

def filter_items(request, category_id):
    category = Categories.objects.get(pk=category_id)
    items = Items.objects.filter(category=category, is_available=True)
    categories = Categories.objects.all()
    
    # Get the cart items for the current user
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_dict = {}
        for cart_item in cart_items:
            cart_dict[cart_item.item.id] = cart_item.quantity
    else:
        cart_dict = {}
        
    context = {'items': items, 'categories': categories, 'cart_dict': cart_dict}

    return render(request, 'home.html', context)



