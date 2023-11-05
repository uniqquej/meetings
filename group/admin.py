from django.contrib import admin

from group.models import Group, Meeting, Notice, ToDo, ToDoList

admin.site.register(Group)
admin.site.register(Meeting)
admin.site.register(Notice)
admin.site.register(ToDo)
admin.site.register(ToDoList)
