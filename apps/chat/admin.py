from django.contrib import admin

from apps.chat.models import Group, Message, Event

admin.site.register(Group)
admin.site.register(Message)
admin.site.register(Event)

