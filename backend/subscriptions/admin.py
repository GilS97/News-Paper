from django.contrib import admin
from .models import EmailSubscription, EmailLog


@admin.register(EmailSubscription)
class EmailSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'frequency', 'is_active', 'last_sent_at', 'created_at']
    list_filter = ['frequency', 'is_active', 'created_at']
    search_fields = ['user__email', 'user__username']
    ordering = ['-created_at']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['subscription', 'status', 'subject', 'article_count', 'sent_at']
    list_filter = ['status', 'sent_at']
    search_fields = ['subscription__user__email', 'subject']
    ordering = ['-sent_at']
