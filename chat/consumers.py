import json

from django.shortcuts import get_object_or_404

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from user.models import User
from chat.models import Chat
from group.models import Group

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope["url_route"]["kwargs"]["group_id"]
        self.room_group_name = "chat_%s" % self.group_id
        self.user = self.scope["user"]

        chat_room = await self.get_chat_room(self.group_id)
        if chat_room is not None:
            self.chat_room = chat_room
        else:
            await self.close()
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print('disconnect')

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]
        # Send message to room group
        await self.send_message(sender, message)
        await self.save_chat(sender, message)

    async def send_message(self, sender, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender":sender
            }
        )
            
    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            {
                "message": message,
                "sender":self.user.nickname
                }
            )
        )
    
    @database_sync_to_async
    def get_chat_room(self, chat_room_num):
        try:
            group = Group.objects.get(id = chat_room_num)
            if self.user not in group.member.all():
                return None
            return group
        
        except Group.DoesNotExist:
            return None
        
    
    @database_sync_to_async
    def save_chat(self, chatter, message):
        try:
            user = get_object_or_404(User, nickname = chatter)

            Chat.objects.create(
                chat_room = self.chat_room,
                chatter = user,
                message = message
            )
            return True
        except Exception as e:    # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
            return {"error": e}