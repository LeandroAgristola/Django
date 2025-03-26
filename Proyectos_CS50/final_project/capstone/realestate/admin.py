from django.contrib import admin
from .models import development

# Register your models here.

class developmentAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated') 

admin.site.register(development, developmentAdmin)
