from rest_framework import serializers
from django.utils import timezone

from user.models import User
from group.models import Group, Calender, Meeting, Notice, ToDoList, ToDo
    
class MeetingSerializer(serializers.ModelSerializer):
    calender_date = serializers.DateField(write_only=True)
    class Meta:
        model = Meeting
        fields = "__all__"
        read_only_fields = ['date']
    
    def validate(self, data):
        data.pop('calender_date') 
        return data
        
class CalenderSerializer(serializers.ModelSerializer):
    meeting_set = MeetingSerializer(read_only=True, many=True)
    meetings_cnt = serializers.SerializerMethodField()
    
    def get_meetings_cnt(self,obj):
        return obj.meeting_set.count()
    
    class Meta:
        model = Calender
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
    calender_set = CalenderSerializer(read_only=True, many=True)
    notice_set = NoticeSerializer(read_only=True, many=True)
    todolist_set = serializers.SerializerMethodField()
    
    def get_todolist_set(self,obj):
        filtered_list = obj.todolist_set.filter(date = timezone.now())
        serializers = ToDoListSerializer(filtered_list, many=True)
        return serializers.data
   
    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ['leader',]