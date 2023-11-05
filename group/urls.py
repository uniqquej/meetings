from django.urls import path

from group import views

urlpatterns = [
    path('', views.GroupView.as_view(), name="group"),
    path('<int:group_id>', views.GroupDetailView.as_view(), name="group_detail"),
    path('<int:group_id>/notice', views.GroupNoticeView.as_view(), name="group_notice"),
    path('<int:group_id>/to-do-list', views.ToDoListView.as_view(), name='to_do_list'),
    path('<int:group_id>/to-do', views.ToDoView.as_view(), name='to_do'),
    path('to-do/<int:to_do_id>', views.ToDoDetailView.as_view(), name='to_do_list_detail'),
    path('meeting/<int:meeting_id>', views.MeetingDetailView.as_view(), name="meeting"),
]
