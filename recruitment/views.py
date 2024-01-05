from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination 
from django.shortcuts import get_object_or_404
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema, no_body

from post.swaggers import get_post_params
from recruitment.swaggers import request_body_recruitment
from recruitment.models import Recruitment
from recruitment.serializers import (RecruitmentSerializer, RecruitmentDetailSerializer,RecruitmentWriteSerializer)
from post.pagination import PaginationHandlerMixin, set_pagination


class BasicPagination(PageNumberPagination):
    page_size = 10

class RecruitmentView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated]
    pagination_class = BasicPagination
    serializer_calss = RecruitmentSerializer
    
    @swagger_auto_schema(
        manual_parameters=get_post_params,
        responses={"200":RecruitmentSerializer(many=True)}
        )
    def get(self, request):
        """
        멤버 모집 글 리스트 반환
        """
        params = request.GET.get('search',None)
        category = request.GET.get('category',None)
        q = Q()
        
        if category:
            q &= Q(category=category)
        if params:
            q &= Q(title__icontains=params) | Q(content__icontains=params)
            
        recruitments =Recruitment.objects.filter(q).select_related("author")
        serializer = set_pagination(self,recruitments,RecruitmentSerializer)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=request_body_recruitment,
        responses={"201":RecruitmentWriteSerializer}
        )
    def post(self, request):
        """
        멤버 모집 글 작성
        """
        serializer = RecruitmentWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author = request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class RecruitmentDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(
        responses={"200":RecruitmentDetailSerializer(many=True)}
        )
    def get(self, request, recruitment_id):
        """
        recruitment_id에 해당하는 모집글 반환
        """
        recruitment = get_object_or_404(Recruitment.objects.select_related("author","group"),id=recruitment_id)
        serializer = RecruitmentDetailSerializer(recruitment)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=request_body_recruitment,
        responses={"202":RecruitmentDetailSerializer}
        )
    def put(self, request, recruitment_id):
        """
        recruitment_id에 해당하는 모집글 수정
        """
        recruitment = get_object_or_404(Recruitment, id=recruitment_id)
        if recruitment.author != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = RecruitmentWriteSerializer(recruitment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        responses={"204":"삭제 완료"}
        )
    def delete(self, request, recruitment_id):
        """
        recruitment_id에 해당하는 모집글 삭제
        """
        recruitment = get_object_or_404(Recruitment, id=recruitment_id)
        if recruitment.author != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        recruitment.delete()
        return Response({"detail":"삭제 완료"}, status = status.HTTP_204_NO_CONTENT)

class ApplicantView(APIView):
    @swagger_auto_schema(
        request_body=no_body,
        responses={"201":"지원 완료","204":"지원 취소"}
        )
    def post(self, request, recruitment_id):
        """
        멤버 모집글 지원
        """
        recruitment = Recruitment.objects.get(id=recruitment_id)
        if request.user not in recruitment.applicant.all():
            recruitment.applicant.add(request.user)
            return Response({"detail":"지원 완료"},status=status.HTTP_201_CREATED)
        else:
            recruitment.applicant.remove(request.user)
            return Response({"detail":"지원 취소"},status=status.HTTP_204_NO_CONTENT)
