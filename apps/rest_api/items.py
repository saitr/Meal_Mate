from apps.models import *
from apps.serializers.itemserializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response

class ItemList(generics.ListCreateAPIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Items.objects.all()
    serializer_class = ItemSerializer
    # @swagger_auto_schema(tags=['Item List'])
    # def get(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)
    
    # @swagger_auto_schema(tags=['Create Item']) 
    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)

class CategoryListView(generics.ListCreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    # @swagger_auto_schema(tags=['Category List'])
    # def get(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)
    
    # @swagger_auto_schema(tags=['Create Category'])
    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)
