from rest_framework import serializers
from .models import EmailSubscription, EmailLog


class EmailSubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for EmailSubscription model.
    """
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = EmailSubscription
        fields = ['id', 'user_email', 'frequency', 'is_active', 'last_sent_at',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'last_sent_at', 'created_at', 'updated_at']


class EmailLogSerializer(serializers.ModelSerializer):
    """
    Serializer for EmailLog model.
    """
    user_email = serializers.EmailField(source='subscription.user.email', read_only=True)

    class Meta:
        model = EmailLog
        fields = ['id', 'user_email', 'status', 'subject', 'article_count',
                  'error_message', 'sent_at']
        read_only_fields = ['id', 'sent_at']
