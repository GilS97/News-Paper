from django.urls import path
from .views import (
    EmailSubscriptionView,
    EmailLogListView,
    unsubscribe,
    resubscribe,
)

app_name = 'subscriptions'

urlpatterns = [
    path('', EmailSubscriptionView.as_view(), name='subscription'),
    path('logs/', EmailLogListView.as_view(), name='email_logs'),
    path('unsubscribe/', unsubscribe, name='unsubscribe'),
    path('resubscribe/', resubscribe, name='resubscribe'),
]
