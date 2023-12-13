from django.db import models

from post.models import Category
from user.models import User
from group.models import Group

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
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f'{self.title}'
