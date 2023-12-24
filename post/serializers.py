from rest_framework import serializers

from post.models import Post, Comment, PostImage, Category
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

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image']
               
class PostCreateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ["author","title","content","created_at","images","category"]
        read_only_fields = ["author",]

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author","post",]