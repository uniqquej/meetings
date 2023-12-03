from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema

from group.swaggers import (request_body_group, request_body_meeting,
                            request_body_to_do, request_body_notice, request_body_put_group)
from group.models import Group, Meeting, ToDoList, ToDo, Notice, Calender
from group.serializers import (GroupSerializer, MeetingSerializer,NoticeSerializer,
                               ToDoListSerializer, TaskSerializer)

class GroupView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    @swagger_auto_schema(
        responses={"200":GroupSerializer(many=True)}
    )
    def get(self, request):
        """
        유저가 member로 포함되어 있는 그룹 리스트 조회
        """
        groups = Group.objects.filter(Q(member=request.user))
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=request_body_group,
        responses={"200":GroupSerializer}
    )
    def post(self, request):
        """
        그룹 생성(생성자 = leader)
        """
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(leader=request.user, member=[request.user])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(
        responses={"200":GroupSerializer}
    )
    def get(self, request, group_id):
        """
        group_id에 해당하는 그룹의 세부사항 조회(일정, 공지, 멤버의 to do list)
        """
        group = Group.objects.prefetch_related("calender_set","notice_set").get(id=group_id)
        if (request.user not in group.member.all()):
            return Response({"detail":"권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=request_body_meeting,
        responses={"200":GroupSerializer}
    )
    def post(self, request, group_id):
        """
        그룹 일정 생성
        """
        group = Group.objects.prefetch_related('calender_set').get(id=group_id)
        calender = group.calender_set.filter(date=request.data['calender_date'])
        if not calender.exists():
            Calender.objects.create(group=group, date=request.data['calender_date'])
            
        serializer = MeetingSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(date=calender[0])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        request_body=request_body_put_group,
        responses={"200":GroupSerializer}
    )
    def put(self, request, group_id):
        """
        그룹 이름, leader 수정
        """
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
    
    @swagger_auto_schema(
        responses={"200":NoticeSerializer}
    )
    def get(self, request, group_id):
        """
        그룹의 공지 리스트 조회
        """
        group = get_object_or_404(Group.objects.filter(id=group_id))
        serializer = NoticeSerializer(group.notice_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=request_body_notice,
        responses={"201":NoticeSerializer}
    )
    def post(self, request, group_id):
        """
        그룹의 공지 작성
        """
        serializer = NoticeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoticeDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=request_body_notice,
        responses={"202":NoticeSerializer}
    )
    def put(self, request, notice_id):
        """
        공지 수정
        """
        notice = get_object_or_404(Notice.objects.select_related('group'), id=notice_id)
        if notice.group.leader != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = NoticeSerializer(notice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        responses={"204":"삭제 완료"}
    )
    def delete(self, request, notice_id):
        """
        공지 삭제
        """
        notice = get_object_or_404(Notice.objects.select_related('group'), id=notice_id)
        if notice.group.leader != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
        notice.delete()
        return Response({"detail":"삭제 완료"}, status=status.HTTP_204_NO_CONTENT)   

class MeetingDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=request_body_meeting,
        responses={"202":MeetingSerializer}
    )
    def put(self, request, meeting_id):
        """
        일정 수정
        """
        meeting = get_object_or_404(Meeting.objects.select_related('date'), id=meeting_id)
        group = meeting.date.group
        if ('calender_date' in request.data) & (meeting.date.date != request.data['calender_date']):
            calender, is_created = Calender.objects.get_or_create(date=request.data['calender_date'], group=group)
            
        serializer = MeetingSerializer(meeting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(date=calender)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        responses={"204":"삭제 완료"}
    )
    def delete(self, request, meeting_id):
        """
        일정 삭제
        """
        meeting = get_object_or_404(Meeting, id=meeting_id)
        
        meeting.delete()
        return Response({"detail":"삭제 완료"}, status=status.HTTP_204_NO_CONTENT)

class ToDoListView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={"200":ToDoListSerializer(many=True)}
    )
    def get(self, request, group_id):
        """
        그룹 멤버의 to do list
        """
        to_do_list = ToDoList.objects.filter(group=group_id)
        serializer = ToDoListSerializer(to_do_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ToDoView(APIView):
    # permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=request_body_to_do,
        responses={"200":TaskSerializer(many=True)}
    )
    def post(self, request, group_id):
        """
        유저 할일 생성
        """
        try:
            print(request.user)
            group = Group.objects.prefetch_related('todolist_set').get(id=group_id)
            to_do_list = group.todolist_set.filter(writer = request.user, date=request.data['date'])
            if not to_do_list.exists():
                ToDoList.objects.create(group=group, writer = request.user, date=request.data['date'])
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(to_do_list=to_do_list[0], writer=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'detail':'not found'},status=status.HTTP_400_BAD_REQUEST)
    

class ToDoDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=request_body_to_do,
        responses={"200":TaskSerializer(many=True)}
    )
    def put(self, request, to_do_id):
        """
        유저 할일 수정
        """
        to_do = get_object_or_404(ToDo,id=to_do_id)
        if to_do.writer != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = TaskSerializer(to_do, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        responses={"204":"삭제 완료"}
    )
    def delete(self, request, to_do_id):
        to_do = get_object_or_404(ToDoList,id=to_do_id)
        if to_do.writer != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
        to_do.delete()
        return Response({"detail":"삭제 완료"}, status=status.HTTP_204_NO_CONTENT)

class MyToDoListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, group_id):
        to_do_lists = ToDoList.objects.filter(writer = request.user, group_id=group_id)
        serializer = ToDoListSerializer(to_do_lists, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    