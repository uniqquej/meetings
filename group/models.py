from django.db import models
from django.utils.timezone import now

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
    time_to_meet = models.DateTimeField()
    
    class Meta:
        db_table = "meeting"
        ordering = ['-time_to_meet']
    
    def __str__(self) -> str:
        return f'{self.title}'

class Notice(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "notice"
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f'{self.title}'

class ToDoList(models.Model):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    date = models.DateField(default=now())
    
    class Meta:
        db_table = "todolist"
        ordering = ['-date']
    
    def __str__(self) -> str:
        return f'{self.task}'