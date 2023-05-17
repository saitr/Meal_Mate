from rest_framework import generics,status
from apps.models import *
from apps.serializers.cartserializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response

class CartListView(generics.ListAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # def get(self,request,username):
    #     cart_list = Cart.objects.filter(username= request.user.username)
    #     serializer = CartListSerializer
    #     return Response({'status': 200, 'cart_list': cart_list})
    @swagger_auto_schema(tags=['Cart List'])

    def get(self, request, user_id):
        cart_list = Cart.objects.filter(user=user_id)
        serializer = CartListSerializer(cart_list, many=True)
        return Response({'status': 200, 'cart_list': serializer.data})
    

class CartAddView(generics.GenericAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            # 'email': openapi.Schema(type=openapi.TYPE_STRING),
            'user': openapi.Schema(type=openapi.TYPE_INTEGER),
            'item_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ),
    tags=['Cart Add']
    )
    # def post(self, request,username):

    #     # cart_items= Cart.objects.(user=request.user)
    #     serializer = CartAddSerializer(many=True)
    #     return Response({'stauts':201,'cart_items':serializer})

    def post(self, request,user_id):
        data = {'user': user_id, 'item': request.data.get('item_id'), 'quantity': request.data.get('quantity')}
        # data = {'user': request.user.id, 'item': request.data.get('item.id'), 'quantity': request.data.get('quantity')}
        serializer = CartAddSerializer(data=data)
        if serializer.is_valid():
            cart_item = serializer.save()
            return Response({'status': 201, 'cart_item': [serializer.data]})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class CartItemUpdateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CartListSerializer

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            # 'email': openapi.Schema(type=openapi.TYPE_STRING),
            'action':openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    tags=['Cart Item Update']
    )

    def put(self, request, pk,user_Id):
        try:
            cart_item = Cart.objects.get(pk=pk, user=request.user.id)
        except Cart.DoesNotExist:
            return Response({'status': 404, 'message': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action', '').lower()

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                cart_item.delete()
                return Response({'status': 204, 'message': 'Cart item deleted.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'status': 400, 'message': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.save()
        serializer = CartListSerializer(cart_item)
        return Response({'status': 200, 'cart_item': serializer.data})



# class CartDelete(generics.DestroyAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = CartListSerializer

#     def delete(self, request, pk):
#         cart_items = Cart.objects.filter(user=request.user,pk=pk)


class CartDestroyView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(tags=['Delete Cart Item'])
    # @swagger_auto_schema(operation={
    #     'operation_id': 'DeleteCartItem',
    #     'tags': ['Cart Item Delete'],
    #     'summary': 'Delete a cart item',
    # },
    # tags=['Cart Item Delete']
    # )
    def destroy(self,request,pk):
        cart_items = Cart.objects.filter(user=request.user,pk=pk)
        cart_items.delete()
        return Response({'status':'Deleted'})
    



