from django.urls import path

from post import views

urlpatterns = [
    path('', views.PostView.as_view(), name="post"),
    path('<int:post_id>', views.PostDetailView.as_view(), name="post_detail"),
    path('<int:post_id>/like', views.PostLikeView.as_view(), name="post_like"),
    path('recruit', views.RecruitmentView.as_view(), name="recruitment"),
    path('recruit/<int:recruitment_id>', views.RecruitmentDetailView.as_view(), name="recruitment_detail"),
    path('recruit/<int:recruitment_id>/applicate', views.ApplicantView.as_view(), name="applicate"),
    path('<int:post_id>/comment', views.CommentView.as_view(), name="comment"),
    path('comment_detail/<int:comment_id>', views.CommentDetailView.as_view(), name="comment_detail"),
    path('category', views.CategoryView.as_view(), name="category"),
]
