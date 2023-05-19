from apps.models import *
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('user','first_name','last_name','address','zip_code','place','payment_method')

    def create(self,validated_data):
        order = Order.objects.create(**validated_data)
        return order
    # def get_order_items(self, order):
    #     order_items = OrderItem.objects.filter(order=order)
    #     serializer = OrderItemSerializer(order_items, many=True)
    #     return serializer.data
    

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order','item','total_price','quantity')

    def create(self,validated_data):
        order_item = OrderItem.objects.create(**validated_data)
        return order_item
    

# class OrderSerializer(serializers.ModelSerializer):
#     order_items = OrderItemSerializer(many=True)  # Include nested serializer for OrderItem

#     class Meta:
#         model = Order
#         fields = ('user', 'first_name', 'last_name', 'address', 'zip_code', 'place', 'payment_method','order_items')

#     def create(self, validated_data):
#         order_items_data = validated_data.pop('order_items')
#         order = Order.objects.create(**validated_data)

#         for order_item_data in order_items_data:
#             OrderItem.objects.create(order=order, **order_item_data)

#         return order

    
    