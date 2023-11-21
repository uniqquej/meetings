from rest_framework import serializers

from user.models import User
from group.models import Group, Meeting, Notice, ToDoList, ToDo
    
class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"
        
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"

class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id','nickname']
               
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'
        read_only_fields=['writer','to_do_list']

class ToDoListSerializer(serializers.ModelSerializer):
    writer = WriterSerializer(read_only=True)
    todo_set = TaskSerializer(read_only=True, many=True) 
    class Meta:
        model = ToDoList
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
    meeting_set = MeetingSerializer(read_only=True, many=True)
    notice_set = NoticeSerializer(read_only=True, many=True)
    todolist_set = ToDoListSerializer(read_only=True, many=True)
    
    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ['leader',]