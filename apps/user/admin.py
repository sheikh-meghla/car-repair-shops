from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomAdminClass(ModelAdmin):
      list_display = ('id', 'email')
      list_display_links = ('id', 'email')
      fieldsets = (
        ('User Info', {
            'fields': ('email','password',),
        }),


         ('Permissions', {
            'fields': ('is_staff',),
        }),
    )