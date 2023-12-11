from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema, no_body

from user.models import User
from post.swaggers import (get_post_params, request_body_post,
                                 request_body_recruitment, request_body_comment)
from post.models import Post, Comment, PostImage, Recruitment, Category
from group.models import Group
from post.serializers import (CategorySerializer,PostSerializer, CommentSerializer, 
                              RecruitmentSerializer, RecruitmentDetailSerializer,RecruitmentWriteSerializer)

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

class ProfilePostView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self,request,user_id):
        params = request.GET.get('option',None)
        current_user = User.objects.prefetch_related('liked_post','application','post_set','recruitment_set').get(id=user_id)
        
        if params=="like":
            posts = current_user.liked_post
        elif params=="apply":
            posts = current_user.application
            serializer = RecruitmentSerializer(posts,many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        elif params=="recruit":
            posts = current_user.recruitment_set
            serializer = RecruitmentSerializer(posts,many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            posts = current_user.post_set
            
        
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class PostView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
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
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=request_body_post,
        responses={"201":PostSerializer}
        )
    def post(self, request):
        """
        게시글 작성
        """
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author = request.user)
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

class RecruitmentView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
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
        serializer = RecruitmentSerializer(recruitments, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=request_body_recruitment,
        responses={"201":PostSerializer}
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
        responses={"200":RecruitmentSerializer(many=True)}
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

class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        responses={"200":CommentSerializer(many=True)}
        )
    def get(self, request, post_id):
        """
        댓글리스트 조회
        """
        post = Post.objects.prefetch_related("comment_set").get(id=post_id)
        comment = post.comment_set
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
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

