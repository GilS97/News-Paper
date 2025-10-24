from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with additional fields for interests and preferences.
    """
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class Interest(models.Model):
    """
    Model to store user interests/topics.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'interests'
        ordering = ['name']

    def __str__(self):
        return self.name


class UserInterest(models.Model):
    """
    Many-to-many relationship between users and interests.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_interests')
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='interested_users')
    priority = models.IntegerField(default=1)  # Priority level for this interest (1-5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_interests'
        unique_together = ['user', 'interest']
        ordering = ['-priority', 'created_at']

    def __str__(self):
        return f"{self.user.email} - {self.interest.name}"
