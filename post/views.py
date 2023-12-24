from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination 
from django.shortcuts import get_object_or_404
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema, no_body

from user.models import User
from post.swaggers import (get_post_params, request_body_post, request_body_comment)
from post.models import Post, Comment, PostImage, Category
from post.pagination import PaginationHandlerMixin, set_pagination
from post.serializers import (CategorySerializer,PostSerializer, 
                              PostCreateSerializer, CommentSerializer)

from recruitment.serializers import RecruitmentSerializer


class BasicPagination(PageNumberPagination):
    page_size = 10

class CommentPagination(PageNumberPagination):
    page_size = 5

class CategoryView(APIView):
    """
    게시글 카테고리 조회
    """
    @swagger_auto_schema(
        responses={"200":CategorySerializer}
        )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfilePostView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated]
    pagination_class = BasicPagination
    
    def get(self,request,user_id):
        params = request.GET.get('option',None)
        current_user = User.objects.prefetch_related('liked_post','application','post_set','recruitment_set').get(id=user_id)
        
        if params=="apply" or params =="recruitment":
            print('current_user',current_user)
            if params=="apply":
                recruitments = current_user.application.all()
                
            else: 
                recruitments = current_user.recruitment_set.all()
            
            serializer = set_pagination(self, recruitments, RecruitmentSerializer)
            return Response(serializer.data, status = status.HTTP_200_OK)    
        
        elif params=="like":
            posts = current_user.liked_post.all()
        else:
            print('current_user',current_user)
            posts = current_user.post_set.all()
            
        serializer = set_pagination(self, posts, PostSerializer)
        return Response(serializer.data, status = status.HTTP_200_OK)

class PostView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BasicPagination
    
    @swagger_auto_schema(
        manual_parameters=get_post_params,
        responses={"200":PostSerializer(many=True)}
        )
    def get(self, request):
        """
        카테고리, 키워드에 해당하는 게시글 리스트 반환
        """
        params = request.GET.get('search',None)
        category = request.GET.get('category',None)
        q = Q()
        
        if category:
            q &= Q(category=category)
        
        if params:
            q &= Q(title__icontains=params) | Q(content__icontains=params)
            
        posts = Post.objects.filter(q).select_related("author")
        serializer = set_pagination(self, posts, PostSerializer)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=request_body_post,
        responses={"201":PostSerializer}
        )
    def post(self, request):
        """
        게시글 작성
        """
        images = request.FILES.getlist('images')
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author = request.user)
            for img in images:
                PostImage.objects.create(post=serializer,image=img)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(
        responses={"200":PostSerializer}
        )
    def get(self, request, post_id):
        """
        post_id에 해당하는 게시글 반환
        """
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=request_body_post,
        responses={"202":PostSerializer}
        )
    def put(self, request, post_id):
        """
        post_id에 해당하는 게시글 수정
        """
        post = get_object_or_404(Post, id=post_id)
        if post.author != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        responses={"204":"삭제 완료", "403":"권한 없음"}
        )
    def delete(self, request, post_id):
        """
        post_id에 해당하는 게시글 삭제
        """
        post = get_object_or_404(Post, id=post_id)
        if post.author != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"detail":"삭제 완료"}, status = status.HTTP_204_NO_CONTENT)

class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=no_body,
        responses={"201":"좋아요", "204":"좋아요 취소"}
        )
    def post(self, request, post_id):
        """
        게시글 좋아요
        """
        post = Post.objects.get(id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({"detail":"좋아요 취소"},status=status.HTTP_204_NO_CONTENT)
        else:
            post.likes.add(request.user)
            return Response({"detail":"좋아요 완료"},status=status.HTTP_201_CREATED)

class CommentView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CommentPagination
    
    @swagger_auto_schema(
        responses={"200":CommentSerializer(many=True)}
        )
    def get(self, request, post_id):
        """
        댓글리스트 조회
        """
        post = Post.objects.prefetch_related("comment_set").get(id=post_id)
        comments = post.comment_set.all()
        serializer = set_pagination(self, comments, CommentSerializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=request_body_comment,
        responses={"201":CommentSerializer}
        )
    def post(self, request, post_id):
        """
        댓글 작성
        """
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author = request.user, post=post)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=request_body_comment,
        responses={"202":CommentSerializer}
        )
    def put(self, request, comment_id):
        """
        댓글 수정
        """
        comment = get_object_or_404 (Comment, id=comment_id)
        
        if comment.author != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        responses={"204":"삭제 완료"}
        )
    def delete(self, request, comment_id):
        """
        댓글 삭제
        """
        comment = get_object_or_404 (Comment, id=comment_id)
        if comment.author != request.user:
            return Response({"detail":"권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response({"detail":"삭제 완료"}, status = status.HTTP_204_NO_CONTENT)

