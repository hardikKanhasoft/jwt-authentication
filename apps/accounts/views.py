from django.shortcuts import render
from rest_framework.views import APIView
from apps.accounts.serializers import (
    UserSerializers,
    LoginSerializers,
    UserProfileSerializers,
    UserChangePasswordSerializer,
)
from jwt_auth.jwt_custom_token import get_tokens_for_user
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.
class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # for encrypt password
            user.set_password(request.data.get('password'))
            user.save()
            tokens = get_tokens_for_user(user=user)
            return Response(
                {"tokens": tokens, "message": "User registred successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )    
        
        
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        email = serializer.data.get("email")
        password = serializer.data.get("password")        
        user = authenticate(email=email, password=password)
        if user is None:
            return Response(
                {"errors": {"non_field_errors": ["Email or password is not valid"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        tokens = get_tokens_for_user(user=user)
        return Response(
            {"tokens": tokens, "message": "Login successfully"},
            status=status.HTTP_200_OK,
        )
        
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        import pdb;pdb.set_trace()
        print("request.user", request.user)
        serializer = UserProfileSerializers(request.user)
        return Response(
            {'data':serializer.data}, 
            status=status.HTTP_200_OK,
            )
        
        
class UserChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        
        if serializer.is_valid():
            return Response(
                {"message": "Password changed successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"errors": serializer.errors},
            )