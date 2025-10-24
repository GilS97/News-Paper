from django.contrib import admin
from .models import Source, Article, UserArticleInteraction


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type', 'is_active', 'created_at', 'last_fetched_at']
    list_filter = ['source_type', 'is_active', 'created_at']
    search_fields = ['name', 'url', 'description']
    filter_horizontal = ['interests']
    ordering = ['-created_at']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'source', 'published_at', 'created_at']
    list_filter = ['source', 'published_at', 'created_at']
    search_fields = ['title', 'description', 'author']
    filter_horizontal = ['interests']
    ordering = ['-published_at']
    date_hierarchy = 'published_at'


@admin.register(UserArticleInteraction)
class UserArticleInteractionAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'interaction_type', 'created_at']
    list_filter = ['interaction_type', 'created_at']
    search_fields = ['user__email', 'article__title']
    ordering = ['-created_at']
