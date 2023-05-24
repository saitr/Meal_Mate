from rest_framework import serializers
from apps.models import *
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','phone_number','email','address')
        # extra_kwargs= {'password':{'write_only':True}}

    def create(self, validated_data):
        otp = get_random_string(length=6, allowed_chars='1234567890')
        user = User.objects.create_user(**validated_data)
        user.otp = otp
        user.save()
        subject = 'Verify your email'
        message = f'Your OTP is {otp}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [validated_data['email']]
        send_mail(subject, message, from_email, recipient_list)
        return user
    

class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')


################# subscribers serializer ##################

class SubscribersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberModel
        fields = ('id','subscriber_email')


    def create(self,validated_data):
        subscriber = SubscriberModel.objects.create(**validated_data)
        subscriber.save()
        subject = "Thanks For Subscribing"
        message = f"Thanks for choosing to become active member now you are in the list of people where they don't miss the opportunity to grab good deals"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [validated_data['subscriber_email']]
        send_mail(subject,message,from_email,recipient_list)
        return subscriber



