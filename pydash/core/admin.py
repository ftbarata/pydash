from django.contrib import admin
from .models import Group, Message


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']


class MessagesAdmin(admin.ModelAdmin):
    list_display = ['message', 'author', 'updated_at', 'created_at', 'severity']


admin.site.register(Message, MessagesAdmin)
admin.site.register(Group, GroupAdmin)


