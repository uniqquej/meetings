from django.urls import path

from group import views

urlpatterns = [
    path('', views.GroupView.as_view(), name="group"),
    path('<int:group_id>', views.GroupDetailView.as_view(), name="group_detail"),
    path('meeting/<int:meeting_id>', views.MeetingDetailView.as_view(), name="meeting"),
]
