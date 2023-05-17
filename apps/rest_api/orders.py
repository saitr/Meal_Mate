from rest_framework import generics,status
from apps.models import *
from apps.serializers.orderserializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class OrderAdd(generics.GenericAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(tags=['Checkout']) 
    def post(self,request):
        cart = Cart.objects.filter(user=request.user)
        data = {
            'user':request.user.id,
            'first_name':request.data.get('first_name'),
            'last_name':request.data.get('last_name'),
            'address':request.data.get('address'),
            'zip_code':request.data.get('zip_code'),
            'place':request.data.get('place'),
            'payment_method':request.data.get('payment_method')
        }
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()

            # create order items for each cart item
            
            for cart_item in cart:
                order_item_data = {
                    'order': order.id,
                    'item': cart_item.item.id,
                    'total_price': cart_item.item.item_price * cart_item.quantity,
                    'quantity': cart_item.quantity
                }
                order_item_serializer = OrderItemSerializer(data=order_item_data)
                if order_item_serializer.is_valid():
                    order_item_serializer.save()
                else:
                    return Response(order_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # delete the user's cart after creating the order and order items
            cart.delete()

            # serialize the order with its order items and return in response
            serializer = OrderSerializer(order, context={'request': request})
            return Response({
                'status': 201,
                'order': serializer.data
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

