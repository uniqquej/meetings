from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q

from group.models import Group, Meeting, ToDoList, ToDo
from group.serializers import (GroupSerializer, MeetingSerializer,NoticeSerializer,
                               ToDoListSerializer, TaskSerializer)

class GroupView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        groups = Group.objects.filter(Q(leader=request.user) | Q(member=request.user))
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(leader=request.user, member=[request.user])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, group_id):
        group = Group.objects.prefetch_related("meeting_set","notice_set").get(id=group_id)
        if (request.user not in group.member.all()):
            return Response({"detail":"권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
        
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
            return Response({"detail":"권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
        
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
        if meeting.group.leader != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
            
        serializer = MeetingSerializer(meeting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, meeting_id):
        meeting = Meeting.objects.select_related("group").get(id=meeting_id)
        
        if meeting.group.leader != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
        
        meeting.delete()
        return Response({"detail":"삭제 완료"}, status=status.HTTP_204_NO_CONTENT)

class ToDoListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, group_id):
        to_do_list = ToDoList.objects.filter(group=group_id)
        serializer = ToDoListSerializer(to_do_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ToDoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, group_id):
        to_dos = ToDo.objects.filter(group=group_id, writer = request.user)
        serializer = TaskSerializer(to_dos)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, group_id):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(group=group_id, writer=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ToDoDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, to_do_id):
        to_do = get_object_or_404(ToDo,id=to_do_id)
        if to_do.writer != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = TaskSerializer(to_do, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, to_do_id):
        to_do = get_object_or_404(ToDoList,id=to_do_id)
        if to_do.writer != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
        to_do.delete()
        return Response({"detail":"삭제 완료"}, status=status.HTTP_204_NO_CONTENT)