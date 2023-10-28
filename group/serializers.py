from rest_framework import serializers

from group.models import Group, Meeting, Notice

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"
        
class NoticeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notice
        fields = "__all__"
        read_only_fields = ["group",]
        
class GroupSerializer(serializers.ModelSerializer):
    meeting_set = MeetingSerializer(read_only=True, many=True)
    notice_set = NoticeSerializer(read_only=True, many=True)
    
    class Meta:
        model = Group
        fields = "__all__"

      