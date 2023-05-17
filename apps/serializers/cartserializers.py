from apps.models import *
from rest_framework import serializers
from rest_framework.response import Response


class CartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        # depth = 2


class CartAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'item', 'quantity')

    # def create(self, validated_data):
    #     user = validated_data['user']
    #     item = validated_data['item']
    #     quantity = validated_data['quantity']

    #     # Check if the item already exists in the cart
    #     try:
    #         cart_items = Cart.objects.get(user=user, item=item)
    #         cart_items.quantity += 1
    #         cart_items.save()
    #     except Cart.DoesNotExist:
    #         cart_items = Cart.objects.create(user=user, item=item, quantity=quantity)

    #     return cart_items
    # def create(self, validated_data):
    #     user = validated_data['user']
    #     item = validated_data['item']
    #     quantity = validated_data['quantity']

    #     # Check if the item already exists in the cart
    #     cart_item, created = Cart.objects.get_or_create(user=user, item=item, defaults={'quantity': quantity})

    #     if not created:
    #         # Item already exists in the cart, increment the quantity
    #         cart_item.quantity += 1
    #         cart_item.save()

    #     return cart_item

    def create(self, validated_data):
        user = validated_data['user']
        item = validated_data['item']
        quantity = validated_data['quantity']
        cart_item, created = Cart.objects.get_or_create(user=user, item=item, quantity= quantity)

        if not created:
            # Item already exists in the cart, increment the quantity
            cart_item.quantity += 1
            cart_item.save()
            # return Response({'status':'Item already exists in the cart'})

        return cart_item
        