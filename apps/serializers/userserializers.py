from rest_framework import serializers
from apps.models import *


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','phone_number','email','address')
        # extra_kwargs= {'password':{'write_only':True}}

    def create(self,    validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')
