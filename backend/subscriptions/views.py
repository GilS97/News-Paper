from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import EmailSubscription, EmailLog
from .serializers import EmailSubscriptionSerializer, EmailLogSerializer


class EmailSubscriptionView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing and updating user email subscription.
    """
    serializer_class = EmailSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get or create subscription for current user
        subscription, created = EmailSubscription.objects.get_or_create(
            user=self.request.user,
            defaults={'frequency': 'weekly_1', 'is_active': True}
        )
        return subscription


class EmailLogListView(generics.ListAPIView):
    """
    API endpoint for listing user's email logs.
    """
    serializer_class = EmailLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            subscription = EmailSubscription.objects.get(user=self.request.user)
            return EmailLog.objects.filter(subscription=subscription)
        except EmailSubscription.DoesNotExist:
            return EmailLog.objects.none()


@api_view(['POST'])
def unsubscribe(request):
    """
    API endpoint for unsubscribing from email notifications.
    """
    try:
        subscription = EmailSubscription.objects.get(user=request.user)
        subscription.is_active = False
        subscription.save()
        return Response(
            {"detail": "Vous avez été désabonné des notifications par email."},
            status=status.HTTP_200_OK
        )
    except EmailSubscription.DoesNotExist:
        return Response(
            {"detail": "Aucun abonnement trouvé."},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def resubscribe(request):
    """
    API endpoint for resubscribing to email notifications.
    """
    try:
        subscription = EmailSubscription.objects.get(user=request.user)
        subscription.is_active = True
        subscription.save()
        return Response(
            {"detail": "Vous avez été réabonné aux notifications par email."},
            status=status.HTTP_200_OK
        )
    except EmailSubscription.DoesNotExist:
        # Create new subscription
        subscription = EmailSubscription.objects.create(
            user=request.user,
            frequency='weekly_1',
            is_active=True
        )
        return Response(
            {"detail": "Abonnement créé avec succès."},
            status=status.HTTP_201_CREATED
        )
