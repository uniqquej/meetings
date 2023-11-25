from rest_framework import serializers

from user.models import User

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

class UserAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255)
    input_number = serializers.CharField(max_length = 4)
    