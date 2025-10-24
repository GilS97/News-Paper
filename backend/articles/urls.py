from django.urls import path
from .views import (
    SourceListCreateView,
    SourceDetailView,
    ArticleListView,
    ArticleDetailView,
    UserSavedArticlesView,
    UserLikedArticlesView,
    save_article,
    unsave_article,
    like_article,
    unlike_article,
)

app_name = 'articles'

urlpatterns = [
    # Sources
    path('sources/', SourceListCreateView.as_view(), name='source_list_create'),
    path('sources/<int:pk>/', SourceDetailView.as_view(), name='source_detail'),

    # Articles
    path('', ArticleListView.as_view(), name='article_list'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),

    # User interactions
    path('saved/', UserSavedArticlesView.as_view(), name='saved_articles'),
    path('liked/', UserLikedArticlesView.as_view(), name='liked_articles'),
    path('<int:pk>/save/', save_article, name='save_article'),
    path('<int:pk>/unsave/', unsave_article, name='unsave_article'),
    path('<int:pk>/like/', like_article, name='like_article'),
    path('<int:pk>/unlike/', unlike_article, name='unlike_article'),
]
