from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile with email preferences"""

    FREQUENCY_CHOICES = [
        ('daily', 'Tous les jours'),
        ('twice_week', 'Deux fois par semaine'),
        ('thrice_week', 'Trois fois par semaine'),
        ('weekly', 'Une fois par semaine'),
        ('never', 'Jamais'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email_frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='weekly',
        verbose_name='Fréquence des emails'
    )
    receive_emails = models.BooleanField(
        default=True,
        verbose_name='Recevoir des emails'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateurs'

    def __str__(self):
        return f"{self.user.username} - {self.get_email_frequency_display()}"
