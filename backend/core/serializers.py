from rest_framework import serializers
from .models import Interest, UserInterest, Source, Article, UserArticle


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name', 'slug', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserInterestSerializer(serializers.ModelSerializer):
    interest = InterestSerializer(read_only=True)
    interest_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserInterest
        fields = ['id', 'interest', 'interest_id', 'added_at']
        read_only_fields = ['id', 'added_at']


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name', 'url', 'source_type', 'is_active', 'last_scraped', 'created_at']
        read_only_fields = ['id', 'last_scraped', 'created_at']


class ArticleListSerializer(serializers.ModelSerializer):
    """Lighter serializer for article lists"""
    source_name = serializers.CharField(source='source.name', read_only=True)
    interest_names = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'url', 'summary', 'author',
            'published_date', 'source_name', 'interest_names',
            'image_url', 'scraped_at'
        ]
        read_only_fields = ['id', 'scraped_at']

    def get_interest_names(self, obj):
        return [interest.name for interest in obj.interests.all()]


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Full serializer with all details"""
    source = SourceSerializer(read_only=True)
    interests = InterestSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'url', 'summary', 'content', 'author',
            'published_date', 'source', 'interests', 'image_url',
            'scraped_at', 'updated_at'
        ]
        read_only_fields = ['id', 'scraped_at', 'updated_at']


class UserArticleSerializer(serializers.ModelSerializer):
    article = ArticleListSerializer(read_only=True)
    article_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = UserArticle
        fields = [
            'id', 'article', 'article_id', 'is_read',
            'is_bookmarked', 'is_recommended', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
