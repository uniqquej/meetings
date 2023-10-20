from django.db import models

from user.models import User

class Group(models.Model):
    group_name = models.CharField(max_length=100)
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    member = models.ManyToManyField(User, related_name="joined_group", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "group"
    
    def __str__(self) -> str:
        return f'{self.group_name}'

class Meeting(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    detail = models.TextField(null=True, blank=True)
    time_to_meet = models.DateTimeField()
    
    class Meta:
        db_table = "meeting"
    
    def __str__(self) -> str:
        return f'{self.title}'