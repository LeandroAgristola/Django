from django.contrib import admin
from .models import User, Email

class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sender', 'subject', 'timestamp', 'read', 'archived')
    actions = ['delete_selected']

admin.site.register(User)
admin.site.register(Email, EmailAdmin)