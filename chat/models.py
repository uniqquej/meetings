from django.db import models

from group.models import Group
from user.models import User

class Chat(models.Model):
    chat_room = models.ForeignKey(Group, on_delete=models.CASCADE)
    chatter = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    sended_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "chat"
    
    def __str__(self) -> str:
        return f'[{self.sended_at}] {self.message}'

