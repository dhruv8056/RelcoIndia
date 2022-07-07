# import email
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):

    # FCM = serializers.CharField(required=False)
    # email = serializers.EmailField(required=False)

    class Meta:
        model = CustomUser
        fields = ("id",'mobile_number', "email")

    def create(self, validated_data):
        user = CustomUser.objects.create(
            mobile_number=validated_data['mobile_number'],
            email=validated_data['email'],
        )
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(
        max_length=128, write_only=True,  required=False)
   
    otp = serializers.IntegerField( required=False)
    token = serializers.CharField(max_length=255, read_only=True)
