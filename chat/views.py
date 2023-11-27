from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from chat.serializers import ChatSerializer
from group.models import Group

class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, group_id):
        group = Group.objects.get(id=group_id)
        chats = group.chat_set
        serializer = ChatSerializer(chats, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        