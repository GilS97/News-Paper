from django.db import models
from django.contrib.auth import get_user_model
from users.models import Interest

User = get_user_model()


class Source(models.Model):
    """
    Model to store article sources (websites, blogs, RSS feeds, etc.)
    """
    SOURCE_TYPE_CHOICES = [
        ('rss', 'RSS Feed'),
        ('web', 'Website'),
        ('blog', 'Blog'),
        ('scientific', 'Scientific Publication'),
    ]

    name = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPE_CHOICES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    interests = models.ManyToManyField(Interest, related_name='sources', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_fetched_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'sources'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Model to store discovered articles.
    """
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    author = models.CharField(max_length=200, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='articles')
    interests = models.ManyToManyField(Interest, related_name='articles', blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'articles'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['source', '-published_at']),
        ]

    def __str__(self):
        return self.title


class UserArticleInteraction(models.Model):
    """
    Model to track user interactions with articles (read, saved, liked).
    """
    INTERACTION_CHOICES = [
        ('read', 'Read'),
        ('saved', 'Saved'),
        ('liked', 'Liked'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_interactions')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='user_interactions')
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_article_interactions'
        unique_together = ['user', 'article', 'interaction_type']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.interaction_type} - {self.article.title[:50]}"
