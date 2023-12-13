from django.contrib import admin

from post.models import Post, Comment, Category

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)


