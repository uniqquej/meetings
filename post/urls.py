from django.urls import path

from post import views

urlpatterns = [
    path('', views.PostView.as_view(), name="post"),
    path('profile/<int:user_id>', views.ProfilePostView.as_view(), name="profile-post"),
    path('<int:post_id>', views.PostDetailView.as_view(), name="post_detail"),
    path('<int:post_id>/like', views.PostLikeView.as_view(), name="post_like"),
    path('<int:post_id>/comment', views.CommentView.as_view(), name="comment"),
    path('comment_detail/<int:comment_id>', views.CommentDetailView.as_view(), name="comment_detail"),
    path('category', views.CategoryView.as_view(), name="category"),
]
