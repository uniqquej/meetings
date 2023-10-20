from rest_framework import serializers

from group.models import Group, Meeting

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"
        
class GroupSerializer(serializers.ModelSerializer):
    meeting_set = MeetingSerializer(read_only=True, many=True)
    
    class Meta:
        model = Group
        fields = "__all__"
        