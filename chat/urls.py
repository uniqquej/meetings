from django.urls import path

from . import views

urlpatterns = [
    path("<int:group_id>", views.ChatView.as_view(), name="chat"),
]