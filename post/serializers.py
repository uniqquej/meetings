from rest_framework import serializers
from rest_framework.serializers import ValidationError

from post.models import Post, Comment, PostImage, Recruitment, Category
from user.serializers import UserSerializer
from group.serializers import GroupSerializer
from group.models import Group

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["author","likes",]

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author","post",]

class RecruitmentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    applicant_count = serializers.SerializerMethodField(read_only=True)
    
    def get_applicant_count(self,obj):
        return obj.applicant.count()
    
    class Meta:
        model = Recruitment
        fields = "__all__"
        
    def validate(self, data):
        group = Group.objects.filter(id=data['group'])
        
        if not group.exists:
            raise ValidationError("해당 그룹이 존재하지 않습니다.")
        return data
        

class RecruitmentDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    applicant_count = serializers.SerializerMethodField(read_only=True)
    group = GroupSerializer(read_only=True)
    
    def get_applicant_count(self,obj):
        return obj.applicant.count()
    
    class Meta:
        model = Recruitment
        fields = "__all__"