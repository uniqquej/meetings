from django.urls import path

from recruitment import views

urlpatterns = [
    path('', views.RecruitmentView.as_view(), name="recruitment"),
    path('<int:recruitment_id>', views.RecruitmentDetailView.as_view(), name="recruitment_detail"),
    path('<int:recruitment_id>/applicate', views.ApplicantView.as_view(), name="applicate"),
]
