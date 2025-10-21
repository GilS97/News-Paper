"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet, UserProfileViewSet
from core.views import (
    InterestViewSet, UserInterestViewSet, SourceViewSet,
    ArticleViewSet, UserArticleViewSet
)

# Create a router and register our viewsets
router = DefaultRouter()

# Accounts
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')

# Core
router.register(r'interests', InterestViewSet, basename='interest')
router.register(r'user-interests', UserInterestViewSet, basename='user-interest')
router.register(r'sources', SourceViewSet, basename='source')
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'user-articles', UserArticleViewSet, basename='user-article')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include('rest_framework.urls')),
]
