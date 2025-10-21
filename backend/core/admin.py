from django.contrib import admin
from .models import Interest, UserInterest, Source, Article, UserArticle


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ['user', 'interest', 'added_at']
    list_filter = ['interest', 'added_at']
    search_fields = ['user__username', 'interest__name']


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type', 'is_active', 'last_scraped', 'created_at']
    list_filter = ['source_type', 'is_active']
    search_fields = ['name', 'url']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'author', 'published_date', 'scraped_at']
    list_filter = ['source', 'interests', 'published_date', 'scraped_at']
    search_fields = ['title', 'author', 'summary']
    filter_horizontal = ['interests']
    readonly_fields = ['scraped_at', 'updated_at']


@admin.register(UserArticle)
class UserArticleAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'is_read', 'is_bookmarked', 'is_recommended', 'created_at']
    list_filter = ['is_read', 'is_bookmarked', 'is_recommended']
    search_fields = ['user__username', 'article__title']
    readonly_fields = ['created_at', 'updated_at']
