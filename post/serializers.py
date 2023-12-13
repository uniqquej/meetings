from rest_framework import serializers
from rest_framework.serializers import ValidationError

from post.models import Post, Comment, PostImage, Recruitment, Category
from group.serializers import GroupSerializer
from user.models import User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","nickname"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["author","likes",]

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author","post",]

class RecruitmentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    applicant_count = serializers.SerializerMethodField(read_only=True)
    
    def get_applicant_count(self,obj):
        return obj.applicant.count()
    
    class Meta:
        model = Recruitment
        fields = "__all__"
        

class RecruitmentWriteSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Recruitment
        fields = ["category","number_of_recruits","title","content","group"]

class RecruitmentDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = AuthorSerializer(read_only=True)
    applicant_count = serializers.SerializerMethodField(read_only=True)
    group = GroupSerializer(read_only=True)
    
    def get_applicant_count(self,obj):
        return obj.applicant.count()
    
    class Meta:
        model = Recruitment
        fields = "__all__"