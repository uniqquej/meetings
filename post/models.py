from django.db import models

from user.models import User
from group.models import Group

class Category(models.Model):
    category_name = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'category'
    
    def __str__(self) -> str:
        return f'{self.category_name}'

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_post', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'post'
    
    def __str__(self) -> str:
        return f'{self.title}'
    
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post/images")
    
    class Meta:
        db_table = 'post_image'
    
class Recruitment(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    number_of_recruits = models.IntegerField()
    applicant = models.ManyToManyField(User, related_name='application', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'recruitment'
    
    def __str__(self) -> str:
        return f'{self.title}'

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    
    class Meta:
        db_table = 'comment'
    
    def __str__(self) -> str:
        return f'{self.comment}'