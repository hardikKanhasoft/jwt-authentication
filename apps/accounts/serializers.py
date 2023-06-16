from rest_framework import serializers
from apps.accounts.models import User
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from jwt_auth.utils import Util
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "phone_no", "password", "is_tc"]
        


class LoginSerializers(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50)
    class Meta:
        model = User
        fields = ["email", "password"]
                
                
class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "phone_no"]
        
class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        style={"input_type": "password"}, min_length=3, max_length=50
    )
    new_password = serializers.CharField(
        style={"input_type": "password"}, min_length=3, max_length=50
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, min_length=3, max_length=50
    )
    
    class Meta:
        model = User
        fields = ["old_password", "new_password", "confirm_password"]
        
    
    def validate(self, attrs):
        
        user = self.context.get("user")
        email = user.email
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        
        authenticated_user = authenticate(email=email, password=old_password)
        if authenticated_user is None:
            raise serializers.ValidationError("Sorry, old password is wrong")
        if new_password != confirm_password:
            raise serializers.ValidationError(
                "Sorry, password and confirm password not matched"
            )
        user.set_password(new_password)
        user.save()
        return attrs
        
class SendPasswordResetLinkEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    class Meta:
        model = User
        fields = ["email"]
    
    def validate(self, attrs):
        email = attrs.get("email")
        print("========= email ===========", email)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = f"http://127.0.0.1:8000/accounts/reset-password/{uid}/{token}/"
            try:
                Util.send_email(
                    subject="Reset Password",
                    recipient=email,
                    message=f"Click here to reset password {reset_link}",
                )
            except Exception as e:
                raise serializers.ValidationError(repr(e))
            return attrs
        raise serializers.ValidationError("Sorry, entered email address is wrong")
            
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={"input_type": "password"}, min_length=3, max_length=50
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, min_length=3, max_length=50
    )
    
    class Meta:
        model = User
        fields = ["password", "confirm_password"]
        
    def validate(self, attrs):
        try:
            password = attrs.get("password")
            confirm_password = attrs.get("confirm_password")
            if password != confirm_password:
                raise serializers.ValidationError("Sorry, password and confirm password not matched")
            user_id = smart_str(urlsafe_base64_decode(self.context.get("uid")))
            token = self.context.get("token")
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                raise serializers.ValidationError("Token is Invalid or expired")
            user.set_password(password)
            user.save()
            return attrs
        
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError("Token is Invalid or expired")