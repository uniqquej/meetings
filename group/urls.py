from django.urls import path

from group import views

urlpatterns = [
    path('', views.GroupView.as_view(), name="group"),
    path('leader',views.LeaderGroupView.as_view(), name='group_leader'),
    path('<int:group_id>', views.GroupDetailView.as_view(), name="group_detail"),
    path('<int:group_id>/notice', views.GroupNoticeView.as_view(), name="group_notice"),
    path('accept/<int:group_id>/<int:user_id>', views.AcceptApplicant.as_view(), name='accept_applicant'),
    path('notice/<int:notice_id>', views.NoticeDetailView.as_view(), name="notice_detail"),
    path('<int:group_id>/to-do-list', views.ToDoListView.as_view(), name='to_do_list'),
    path('<int:group_id>/my-to-do', views.MyToDoListView.as_view(), name='my_to_do'),
    path('<int:group_id>/to-do', views.ToDoView.as_view(), name='to_do'),
    path('to-do/<int:to_do_id>', views.ToDoDetailView.as_view(), name='to_do_list_detail'),
    path('to-do/<int:to_do_id>/check', views.ToDoCheckView.as_view(), name='to_do_check'),
    path('meeting/<int:meeting_id>', views.MeetingDetailView.as_view(), name="meeting"),
]
