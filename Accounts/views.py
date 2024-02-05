from django.http import request
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics,permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import LogoutSerializer, RegistrationSerializer, CheckEmailSerializer, AuthorizeSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import CustomUser

class RegistrationAPIView(generics.GenericAPIView):
    serializer_class=RegistrationSerializer
    permission_classes = []
    authentication_classes = []

    @swagger_auto_schema(tags=['Accounts'])
    def post(self, request):
        print(request.data.get("managerRenewedIDFront"))
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    @swagger_auto_schema(tags=['Accounts'])
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

class LoginRefreshView(TokenRefreshView):
    @swagger_auto_schema(tags=['Accounts'])
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = []

    @swagger_auto_schema(tags=['Accounts'])
    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message':'You have logged out successfully'},status=status.HTTP_204_NO_CONTENT)

class CheckEmailView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = CheckEmailSerializer

    @swagger_auto_schema(tags=['Accounts'])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        is_email_available = not CustomUser.objects.filter(email=email).exists()

        return Response({'is_email_available': is_email_available}, status=status.HTTP_200_OK)


class AuthorizeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class  = AuthorizeSerializer

    @swagger_auto_schema(tags=['Accounts'])
    def post(self, request, *args, **kwargs):
        return Response({'message': 'User is authenticated'}, status=status.HTTP_200_OK)