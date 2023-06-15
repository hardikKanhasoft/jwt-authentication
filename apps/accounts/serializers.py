from rest_framework import serializers
from apps.accounts.models import User
from django.contrib.auth import authenticate

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
        