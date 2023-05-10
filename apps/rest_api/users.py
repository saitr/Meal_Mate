from apps.models import *
from apps.serializers.userserializers import *
from rest_framework import generics
from django.contrib.auth import authenticate, logout
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
# from aserializers import UserSerializer


User = get_user_model()
class SignUpView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer


class SigninView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignInSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.get(username=username, password=password)
        if user:
            user.is_logged_in = True
            refresh = RefreshToken.for_user(user)
            print('this is refresh token',refresh)
            access_token = str(refresh.access_token)
            user.jwt_token = RefreshToken.for_user(user)
            print('this is access token',access_token)
            user.save()
            
            return Response({'status':200,'refresh': str(refresh), 'access': str(refresh.access_token)})
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class LogoutView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        user.is_logged_in = False
        user.jwt_token = None
        user.save()
        logout(request)
        return Response({'detail': 'Successfully logged out'})