from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail,EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
# form imports 
from apps.forms import SignUpForm,VerifyOTPForm,SignInForm,ChangeUserDetails, SubscribersForm
from django.http import HttpResponse
from apps.models import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.authtoken.models import Token
import secrets
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
##checks for login
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # check if email already exists
            email = form.cleaned_data.get('email')
            print('thisis the email',email)
            # to check if the username already exists 
            username = form.cleaned_data.get('username')

            if User.objects.filter(email=email,username=username).exists():
                form.add_error('email', 'Email already exists')
                return render(request, 'signup.html', {'form': form})
            
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
                return render(request, 'signup.html', {'form': form})
            # generate OTP and save it to user model
            otp = get_random_string(length=6, allowed_chars='1234567890')
            user = User.objects.create(
                username=form.cleaned_data.get('username'),
                email=email,
                phone_number=form.cleaned_data.get('phone_number'),
                address=form.cleaned_data.get('address'),
                otp=otp,
                password = form.cleaned_data.get('password')
            )


            # to create a token 

            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token(user=user)
            
            token.key = secrets.token_urlsafe(32)
            token.created = timezone.now()
            token.expires = token.created + timedelta(days=7)
            token.save()

            

            
            # Send email with OTP
            subject = 'Verify your email'
            message = f'Your OTP is {otp}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            
            # Redirect to verify page
            return redirect('verify', email=email)
    else: 
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})





############################## to verify the email while signing up##################################

def verify(request, email):
    user = User.objects.get(email=email)

    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            if otp == user.otp:
                user.is_active = True
                user.is_verified = True
                user.is_logged_in = True
                user.save()

                # Send thank you email
                subject =  'Welcome To The Family'
                from_email = settings.DEFAULT_FROM_EMAIL
                to = [email]

                html_content = render_to_string('thankyouemail.html')
                text_content = strip_tags(html_content)

                msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, 'text/html')
                msg.send()

                # Authenticate and log in the user
                
                login(request,user)
                user.save_token()

                
                if login:
                    print('successfully logged in')
                else:
                    print('failed to login')

                if request.user.is_authenticated:
                    print("Logged in")
                else:
                    print("Not logged in")
                return redirect('home')
            else:
                form.add_error('otp', 'Invalid OTP. Please try again.')
    else:
        form = VerifyOTPForm()

    return render(request, 'verify.html', {'form': form})

#######################################logout view#######################################



def logout_user(request):
    if request.user.is_authenticated:
        user = request.user
        user.token = None
        print('thisi sit',user.token)
        user.is_logged_in = False
        user.save()
        logout(request)
    return redirect('signin')




########################################### signin view###################################


# def signin(request):
#     if request.method == 'POST':
#         form = SignInForm(request.POST)
#         if form.is_valid():
#             username= form.cleaned_data['username']
#             print('login username',username)
#             password= form.cleaned_data['password']
#             print('login password',password)
            
#             user = User.objects.get(username=username,password=password)
#             if user:
#                 login_user = user

#                 login(request,login_user)
#                 try:
#                     token = Token.objects.get(user=user)
#                 except Token.DoesNotExist:
#                     token = Token(user=user)
                
#                 token.key = secrets.token_urlsafe(32)
#                 token.created = timezone.now()
#                 token.expires = token.created + timedelta(days=7)
#                 token.save()

#                 if login:
#                     print('login successful')
#                 else:
#                     print('login failed')
#                 user.is_logged_in = True
#                 user.save()
#                 return redirect('home')
#             else:
#                 form.add_error('no correct username or password')
   
#     else:
#         form = SignInForm()
#     return render(request, 'signin.html', {'form': form})



def signin(request):
    
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username, password=password)
            except User.DoesNotExist:
                form.add_error(None, 'Incorrect username or password')
                return render(request, 'signin.html', {'form': form})

            login(request, user)
            
            # # Delete any existing tokens for the user
            user.save_token()

            user.is_logged_in = True
            user.save()

            return redirect('home')

    else:
        form = SignInForm()

    return render(request, 'signin.html', {'form': form})



############################ user details ##################################

# @login_required
# def user_details(request):
#     user = request.user

#     if request.method == 'POST':
#         form = ChangeUserDetails(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             phone_number = form.cleaned_data['phone_number']
#             address = form.cleaned_data['address']

#             request.user.username = username
#             request.user.email = email
#             request.user.phone_number = phone_number
#             request.user.address = address

#             user.save()
#             return redirect('home')
#     else: 
#         form = ChangeUserDetails()
#     # user = request.user
#     # context = {'user': user}
#     return render(request, 'user_details.html',{'form':form})


@login_required
def user_details(request):
    user = request.user
    users = User.objects.all()
    if request.method == 'POST':
        form = ChangeUserDetails(request.POST,request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            display_picture = form.cleaned_data['display_picture']

            request.user.username = username
            request.user.email = email
            request.user.phone_number = phone_number
            request.user.address = address
            
            # Save display picture if provided
            if display_picture:
                user.display_picture = display_picture
                
            request.user.save()
            return redirect('home')
    else:
        initial_data = {
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'address': user.address,
        }
        form = ChangeUserDetails(initial=initial_data)
    
    return render(request, 'user_details.html', {'form': form,'users': users})





################### Subscribers #####################

# @login_required
# def subscribers(request):
#     if request.method == 'POST':
#         form = SubscribersForm(request.POST)
#         if form.is_valid():
#             subscribers_email = form.cleaned_data['subscriber_email']
#             # if SubscriberModel.objects.filter(subscriber_email=subscriber_email).exists():
#             #     form.add_error('email', 'Email already exists')
#             #     return render(request, 'home.html', {'form': form})
#             subscriber = SubscriberModel.objects.create(
#                 subscriber_email = form.cleaned_data['subscriber_email']
#             )
        
#         # to send the thanks email for the subscribers 

#             subject = 'Thanks For Subscribing'
#             message = "Thanks for choosing to become active member now you are in the list of people where they don't miss the opportunity to grab good deals"
#             from_email = settings.DEFAULT_FROM_EMAIL
#             recipient_list = [subscribers_email]
#             send_mail(subject,message,from_email,recipient_list)
#             return redirect('home')
#         else:
#             form = SubscribersForm()
#         return render(request,'subscriber.html',{'form':form})
        

@login_required
def subscribers(request):
    if request.method == 'POST':
        form = SubscribersForm(request.POST)
        print('this is the subscriber form',form)
        if form.is_valid():
            subscriber_email = form.cleaned_data['subscriber_email']
            print('this is the subscribers form input email',subscriber_email)
            
            # Check if subscriber with the same email already exists

            
            # Create the new subscriber if it's a unique email
            subscriber = SubscriberModel.objects.create(
                subscriber_email=subscriber_email
            )
            print('this is the subscriber email',subscriber)

                # Send the thanks email to the subscriber
            subject = 'Thanks For Subscribing'
            message = "Thanks for choosing to become an active member. You are now in the list of people who don't miss the opportunity to grab good deals."
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [subscriber_email]
            send_mail(subject, message, from_email, recipient_list)

            return redirect('home')
    else:
        form = SubscribersForm()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    return render(request, 'home.html', {'form': form})








