from rest_framework import serializers
from .models import Source, Article, UserArticleInteraction
from users.serializers import InterestSerializer


class SourceSerializer(serializers.ModelSerializer):
    """
    Serializer for Source model.
    """
    interests = InterestSerializer(many=True, read_only=True)
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = Source
        fields = ['id', 'name', 'url', 'source_type', 'description', 'is_active',
                  'interests', 'article_count', 'created_at', 'updated_at', 'last_fetched_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_fetched_at']

    def get_article_count(self, obj):
        return obj.articles.count()


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for Article model.
    """
    source_name = serializers.CharField(source='source.name', read_only=True)
    interests = InterestSerializer(many=True, read_only=True)
    is_read = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'url', 'description', 'content', 'author',
                  'published_at', 'source', 'source_name', 'interests', 'image_url',
                  'is_read', 'is_saved', 'is_liked', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_is_read(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserArticleInteraction.objects.filter(
                user=request.user,
                article=obj,
                interaction_type='read'
            ).exists()
        return False

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserArticleInteraction.objects.filter(
                user=request.user,
                article=obj,
                interaction_type='saved'
            ).exists()
        return False

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserArticleInteraction.objects.filter(
                user=request.user,
                article=obj,
                interaction_type='liked'
            ).exists()
        return False


class ArticleListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for article lists.
    """
    source_name = serializers.CharField(source='source.name', read_only=True)
    interest_names = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'url', 'description', 'author', 'published_at',
                  'source_name', 'interest_names', 'image_url', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_interest_names(self, obj):
        return [interest.name for interest in obj.interests.all()]


class UserArticleInteractionSerializer(serializers.ModelSerializer):
    """
    Serializer for UserArticleInteraction model.
    """
    article = ArticleListSerializer(read_only=True)
    article_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserArticleInteraction
        fields = ['id', 'article', 'article_id', 'interaction_type', 'created_at']
        read_only_fields = ['id', 'created_at']
