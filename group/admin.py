from django.contrib import admin

from group.models import Group, Calender, Meeting, Notice, ToDo, ToDoList

admin.site.register(Group)
admin.site.register(Meeting)
admin.site.register(Calender)
admin.site.register(Notice)
admin.site.register(ToDo)
admin.site.register(ToDoList)
