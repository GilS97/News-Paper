from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    UserProfileView,
    ChangePasswordView,
    InterestListCreateView,
    InterestDetailView,
    UserInterestListView,
    UserInterestCreateView,
    UserInterestDeleteView,
)

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

    # Interests
    path('interests/', InterestListCreateView.as_view(), name='interest_list_create'),
    path('interests/<int:pk>/', InterestDetailView.as_view(), name='interest_detail'),

    # User interests
    path('my-interests/', UserInterestListView.as_view(), name='user_interest_list'),
    path('my-interests/add/', UserInterestCreateView.as_view(), name='user_interest_create'),
    path('my-interests/<int:pk>/', UserInterestDeleteView.as_view(), name='user_interest_delete'),
]
