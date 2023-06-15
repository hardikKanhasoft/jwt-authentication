from rest_framework import serializers
from apps.accounts.models import User


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
