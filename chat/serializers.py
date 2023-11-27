from rest_framework import serializers

from chat.models import Chat
from user.models import User

class NicknameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["nickname"]

class ChatSerializer(serializers.ModelSerializer):
    chatter = NicknameSerializer(read_only=True)
    class Meta:
        model = Chat
        fields = "__all__"
        