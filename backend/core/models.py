from django.db import models
from django.contrib.auth.models import User


class Interest(models.Model):
    """Categories of user interests"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Nom')
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Centre d\'intérêt'
        verbose_name_plural = 'Centres d\'intérêt'
        ordering = ['name']

    def __str__(self):
        return self.name


class UserInterest(models.Model):
    """Many-to-many relationship between users and interests"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests')
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='users')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Intérêt utilisateur'
        verbose_name_plural = 'Intérêts utilisateurs'
        unique_together = ['user', 'interest']

    def __str__(self):
        return f"{self.user.username} - {self.interest.name}"


class Source(models.Model):
    """Source of articles (scientific journals, blogs, etc.)"""

    SOURCE_TYPES = [
        ('scientific', 'Publication scientifique'),
        ('journal', 'Revue'),
        ('blog', 'Blog'),
        ('news', 'Actualités'),
    ]

    name = models.CharField(max_length=200, verbose_name='Nom')
    url = models.URLField(verbose_name='URL')
    source_type = models.CharField(
        max_length=20,
        choices=SOURCE_TYPES,
        verbose_name='Type de source'
    )
    is_active = models.BooleanField(default=True, verbose_name='Active')
    last_scraped = models.DateTimeField(null=True, blank=True, verbose_name='Dernier scraping')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"


class Article(models.Model):
    """Articles collected from various sources"""
    title = models.CharField(max_length=500, verbose_name='Titre')
    url = models.URLField(unique=True, verbose_name='URL')
    summary = models.TextField(blank=True, verbose_name='Résumé')
    content = models.TextField(blank=True, verbose_name='Contenu')
    author = models.CharField(max_length=200, blank=True, verbose_name='Auteur')
    published_date = models.DateTimeField(null=True, blank=True, verbose_name='Date de publication')
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Source'
    )
    interests = models.ManyToManyField(
        Interest,
        related_name='articles',
        blank=True,
        verbose_name='Centres d\'intérêt'
    )
    image_url = models.URLField(blank=True, verbose_name='Image URL')
    scraped_at = models.DateTimeField(auto_now_add=True, verbose_name='Scrapé le')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-published_date', '-scraped_at']

    def __str__(self):
        return self.title[:100]


class UserArticle(models.Model):
    """Track user interactions with articles"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_articles')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='user_interactions')
    is_read = models.BooleanField(default=False, verbose_name='Lu')
    is_bookmarked = models.BooleanField(default=False, verbose_name='Favori')
    is_recommended = models.BooleanField(default=False, verbose_name='Recommandé')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Article utilisateur'
        verbose_name_plural = 'Articles utilisateurs'
        unique_together = ['user', 'article']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.article.title[:50]}"
