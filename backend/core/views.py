from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from .models import Interest, UserInterest, Source, Article, UserArticle
from .serializers import (
    InterestSerializer, UserInterestSerializer, SourceSerializer,
    ArticleListSerializer, ArticleDetailSerializer, UserArticleSerializer
)


class InterestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing interests/categories
    """
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class UserInterestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user interests
    """
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserInterest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_interests(self, request):
        """Get all interests for the current user"""
        interests = UserInterest.objects.filter(user=request.user)
        serializer = UserInterestSerializer(interests, many=True)
        return Response(serializer.data)


class SourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing sources (read-only for users)
    """
    queryset = Source.objects.filter(is_active=True)
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing articles
    """
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleListSerializer

    def get_queryset(self):
        queryset = Article.objects.all()

        # Filter by interest
        interest_slug = self.request.query_params.get('interest', None)
        if interest_slug:
            queryset = queryset.filter(interests__slug=interest_slug)

        # Filter by source
        source_id = self.request.query_params.get('source', None)
        if source_id:
            queryset = queryset.filter(source_id=source_id)

        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(summary__icontains=search) |
                Q(author__icontains=search)
            )

        return queryset.distinct()

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Get recommended articles based on user interests"""
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Get user interests
        user_interests = request.user.interests.values_list('interest_id', flat=True)

        if not user_interests:
            # If user has no interests, return recent articles
            articles = Article.objects.all()[:20]
        else:
            # Get articles matching user interests
            articles = Article.objects.filter(
                interests__id__in=user_interests
            ).distinct()[:20]

        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)


class UserArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user-article interactions
    """
    queryset = UserArticle.objects.all()
    serializer_class = UserArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserArticle.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def bookmarked(self, request):
        """Get all bookmarked articles"""
        bookmarked = UserArticle.objects.filter(
            user=request.user,
            is_bookmarked=True
        )
        serializer = UserArticleSerializer(bookmarked, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def read(self, request):
        """Get all read articles"""
        read_articles = UserArticle.objects.filter(
            user=request.user,
            is_read=True
        )
        serializer = UserArticleSerializer(read_articles, many=True)
        return Response(serializer.data)
