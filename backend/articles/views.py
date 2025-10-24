from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from .models import Source, Article, UserArticleInteraction
from .serializers import (
    SourceSerializer,
    ArticleSerializer,
    ArticleListSerializer,
    UserArticleInteractionSerializer
)


class SourceListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating sources.
    """
    queryset = Source.objects.filter(is_active=True)
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


class SourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating and deleting sources.
    """
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [IsAdminUser]


class ArticleListView(generics.ListAPIView):
    """
    API endpoint for listing articles.
    Filters articles based on user interests.
    """
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'author']
    ordering_fields = ['published_at', 'created_at']
    ordering = ['-published_at']

    def get_queryset(self):
        user = self.request.user
        queryset = Article.objects.all()

        # Filter by user interests if the user has any
        user_interests = user.user_interests.values_list('interest_id', flat=True)
        if user_interests:
            queryset = queryset.filter(interests__in=user_interests).distinct()

        # Filter by interest ID if provided
        interest_id = self.request.query_params.get('interest_id')
        if interest_id:
            queryset = queryset.filter(interests__id=interest_id)

        # Filter by source ID if provided
        source_id = self.request.query_params.get('source_id')
        if source_id:
            queryset = queryset.filter(source_id=source_id)

        return queryset


class ArticleDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving article details.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Automatically mark as read
        UserArticleInteraction.objects.get_or_create(
            user=request.user,
            article=instance,
            interaction_type='read'
        )

        return Response(serializer.data)


class UserSavedArticlesView(generics.ListAPIView):
    """
    API endpoint for listing user's saved articles.
    """
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-created_at']

    def get_queryset(self):
        saved_article_ids = UserArticleInteraction.objects.filter(
            user=self.request.user,
            interaction_type='saved'
        ).values_list('article_id', flat=True)

        return Article.objects.filter(id__in=saved_article_ids)


class UserLikedArticlesView(generics.ListAPIView):
    """
    API endpoint for listing user's liked articles.
    """
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-created_at']

    def get_queryset(self):
        liked_article_ids = UserArticleInteraction.objects.filter(
            user=self.request.user,
            interaction_type='liked'
        ).values_list('article_id', flat=True)

        return Article.objects.filter(id__in=liked_article_ids)


@api_view(['POST'])
def save_article(request, pk):
    """
    API endpoint for saving an article.
    """
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(
            {"detail": "Article non trouvé."},
            status=status.HTTP_404_NOT_FOUND
        )

    interaction, created = UserArticleInteraction.objects.get_or_create(
        user=request.user,
        article=article,
        interaction_type='saved'
    )

    if created:
        return Response(
            {"detail": "Article sauvegardé."},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail": "Article déjà sauvegardé."},
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
def unsave_article(request, pk):
    """
    API endpoint for removing an article from saved.
    """
    try:
        interaction = UserArticleInteraction.objects.get(
            user=request.user,
            article_id=pk,
            interaction_type='saved'
        )
        interaction.delete()
        return Response(
            {"detail": "Article retiré des favoris."},
            status=status.HTTP_200_OK
        )
    except UserArticleInteraction.DoesNotExist:
        return Response(
            {"detail": "Article non trouvé dans les favoris."},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def like_article(request, pk):
    """
    API endpoint for liking an article.
    """
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(
            {"detail": "Article non trouvé."},
            status=status.HTTP_404_NOT_FOUND
        )

    interaction, created = UserArticleInteraction.objects.get_or_create(
        user=request.user,
        article=article,
        interaction_type='liked'
    )

    if created:
        return Response(
            {"detail": "Article aimé."},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail": "Article déjà aimé."},
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
def unlike_article(request, pk):
    """
    API endpoint for unliking an article.
    """
    try:
        interaction = UserArticleInteraction.objects.get(
            user=request.user,
            article_id=pk,
            interaction_type='liked'
        )
        interaction.delete()
        return Response(
            {"detail": "Like retiré."},
            status=status.HTTP_200_OK
        )
    except UserArticleInteraction.DoesNotExist:
        return Response(
            {"detail": "Article non trouvé dans les likes."},
            status=status.HTTP_404_NOT_FOUND
        )
