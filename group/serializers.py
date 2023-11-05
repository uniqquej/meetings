from rest_framework import serializers

from group.models import Group, Meeting, Notice, ToDoList, ToDo

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"
        
class NoticeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notice
        fields = "__all__"
        read_only_fields = ["group",]
        
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'
        read_only_fields=['writer']

class ToDoListSerializer(serializers.ModelSerializer):
    todo_set = TaskSerializer(read_only=True, many=True) 
    class Meta:
        model = ToDoList
        fields = "__all__"
        read_only = ['writer',]

class GroupSerializer(serializers.ModelSerializer):
    meeting_set = MeetingSerializer(read_only=True, many=True)
    notice_set = NoticeSerializer(read_only=True, many=True)
    todolist_set = ToDoListSerializer(read_only=True, many=True)
    
    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ['leader',]