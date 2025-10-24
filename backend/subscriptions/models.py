from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailSubscription(models.Model):
    """
    Model to manage user email subscription preferences.
    """
    FREQUENCY_CHOICES = [
        ('none', 'Aucun'),
        ('daily', 'Tous les jours'),
        ('weekly_1', 'Une fois par semaine'),
        ('weekly_2', 'Deux fois par semaine'),
        ('weekly_3', 'Trois fois par semaine'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_subscription')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='weekly_1')
    is_active = models.BooleanField(default=True)
    last_sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'email_subscriptions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.get_frequency_display()}"


class EmailLog(models.Model):
    """
    Model to track sent emails.
    """
    STATUS_CHOICES = [
        ('sent', 'Envoyé'),
        ('failed', 'Échoué'),
    ]

    subscription = models.ForeignKey(EmailSubscription, on_delete=models.CASCADE, related_name='email_logs')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    subject = models.CharField(max_length=200)
    article_count = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'email_logs'
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.subscription.user.email} - {self.status} - {self.sent_at}"
