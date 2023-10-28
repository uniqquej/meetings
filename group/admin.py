from django.contrib import admin

from group.models import Group, Meeting, Notice

admin.site.register(Group)
admin.site.register(Meeting)
admin.site.register(Notice)
