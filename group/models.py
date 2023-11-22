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

class Calender(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    
    class Meta:
        db_table = "calender"
        ordering = ['-date']
    
    def __str__(self) -> str:
        return f'{self.date}'

class Meeting(models.Model):
    title = models.CharField(max_length=100)
    date = models.ForeignKey(Calender, on_delete=models.CASCADE)
    time = models.TimeField(null=False)
    
    class Meta:
        db_table = "meeting"
        ordering = ['-time']
    
    def __str__(self) -> str:
        return f'{self.title}'

class Notice(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "notice"
        ordering = ['-updated_at']
    
    def __str__(self) -> str:
        return f'{self.title}'

class ToDoList(models.Model):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    
    class Meta:
        db_table = "todolist"
        ordering = ['-date']
    
    def __str__(self) -> str:
        return f'{self.date}'

class ToDo(models.Model):
    to_do_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    
    class Meta:
        db_table = "todo"

    def __str__(self) -> str:
        return f'{self.task}'