from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_frequency', 'receive_emails', 'created_at']
    list_filter = ['email_frequency', 'receive_emails']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
