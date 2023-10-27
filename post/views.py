from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.db.models import Q

from post.models import Post, Comment, PostImage, Recruitment, Category
from group.models import Group
from post.serializers import (CategorySerializer,PostSerializer, CommentSerializer, 
                              RecruitmentSerializer, RecruitmentDetailSerializer)

class CategoryView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        params = request.GET.get('search',None)
        category = request.GET.get('category',None)
        q = Q()
        
        if category:
            q &= Q(category=category)
        
        if params:
            q &= Q(title__icontains=params) | Q(content__icontains=params)
            
        posts = Post.objects.filter(q).select_related("author")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author = request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.author != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.author != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"detail":"삭제 완료"}, status = status.HTTP_204_NO_CONTENT)

class PostLikeView(APIView):
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({"detail":"좋아요 취소"},status=status.HTTP_204_NO_CONTENT)
        else:
            post.likes.add(request.user)
            return Response({"detail":"좋아요 완료"},status=status.HTTP_201_CREATED)

class RecruitmentView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        params = request.GET.get('search',None)
        category = request.GET.get('category',None)
        q = Q()
        
        if category:
            q &= Q(category=category)
        if params:
            q &= Q(title__icontains=params) | Q(content__icontains=params)
            
        recruitments =Recruitment.objects.filter(q).select_related("author")
        serializer = RecruitmentSerializer(recruitments, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = RecruitmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author = request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class RecruitmentDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, recruitment_id):
        recruitment = Recruitment.objects.select_related("author","group").get(id=recruitment_id)
        serializer = RecruitmentDetailSerializer(recruitment)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, recruitment_id):
        recruitment = get_object_or_404(Recruitment, id=recruitment_id)
        if recruitment.author != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = RecruitmentDetailSerializer(recruitment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, recruitment_id):
        recruitment = get_object_or_404(Recruitment, id=recruitment_id)
        if recruitment.author != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        recruitment.delete()
        return Response({"detail":"삭제 완료"}, status = status.HTTP_204_NO_CONTENT)

class ApplicantView(APIView):
    def post(self, request, recruitment_id):
        recruitment = Recruitment.objects.get(id=recruitment_id)
        if request.user not in recruitment.applicant.all():
            recruitment.applicant.add(request.user)
            return Response({"detail":"지원 완료"},status=status.HTTP_201_CREATED)
        else:
            recruitment.applicant.remove(request.user)
            return Response({"detail":"지원 취소"},status=status.HTTP_204_NO_CONTENT)

class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, post_id):
        post = Post.objects.prefetch_related("comment_set").get(id=post_id)
        comment = post.comment_set
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author = request.user, post=post)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, comment_id):
        comment = get_object_or_404 (Comment, id=comment_id)
        
        if comment.author != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, comment_id):
        comment = get_object_or_404 (Comment, id=comment_id)
        if comment.author != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response({"detail":"삭제 완료"}, status = status.HTTP_204_NO_CONTENT)

