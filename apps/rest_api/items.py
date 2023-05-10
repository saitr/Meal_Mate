from apps.models import *
from apps.serializers.itemserializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication


class ItemList(generics.ListCreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Items.objects.all()
    serializer_class = ItemSerializer

class CategoryListView(generics.ListCreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
