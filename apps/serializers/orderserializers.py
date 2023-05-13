from apps.models import *
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('user','first_name','last_name','address','zip_code','place','payment_method')

    def create(self,validated_data):
        order = Order.objects.create(**validated_data)
        return order
    

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order','item','total_price','quantity')

    def create(self,validated_data):
        order_item = OrderItem.objects.create(**validated_data)
        return order_item
    
    