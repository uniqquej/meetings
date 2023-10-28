from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q

from group.models import Group, Meeting, Notice
from group.serializers import GroupSerializer, MeetingSerializer,NoticeSerializer

class GroupView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        groups = Group.objects.filter(Q(leader=request.user) | Q(member=request.user))
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, group_id):
        group = Group.objects.prefetch_related("meeting_set","notice_set").get(id=group_id)
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, group_id):
        serializer = MeetingSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(group_id=group_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        
        if group.leader != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupNoticeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, group_id):
        group = Group.objects.filter(id=group_id).select_related("notice_set")
        serializer = NoticeSerializer(group.notice_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, group_id):
        serializer = NoticeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(group=group_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MeetingDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def put(self, request, meeting_id):
        meeting = get_object_or_404(Meeting, id=meeting_id)
        serializer = MeetingSerializer(meeting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, meeting_id):
        meeting = Meeting.objects.select_related("group").get(id=meeting_id)
        
        if meeting.group.leader != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        
        meeting.delete()
        return Response({"detail":"삭제 완료"}, status=status.HTTP_204_NO_CONTENT)
