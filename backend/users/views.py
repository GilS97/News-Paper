from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .models import Interest, UserInterest
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    InterestSerializer,
    UserInterestSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing and updating user profile.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserUpdateSerializer
        return UserSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    API endpoint for changing user password.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Mot de passe incorrect."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Set new password
            user.set_password(serializer.data.get("new_password"))
            user.save()

            return Response(
                {"detail": "Mot de passe changé avec succès."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InterestListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating interests.
    """
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [IsAuthenticated]


class InterestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating and deleting interests.
    """
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [IsAuthenticated]


class UserInterestListView(generics.ListAPIView):
    """
    API endpoint for listing user interests.
    """
    serializer_class = UserInterestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserInterest.objects.filter(user=self.request.user)


class UserInterestCreateView(generics.CreateAPIView):
    """
    API endpoint for adding user interest.
    """
    serializer_class = UserInterestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserInterestDeleteView(generics.DestroyAPIView):
    """
    API endpoint for removing user interest.
    """
    serializer_class = UserInterestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserInterest.objects.filter(user=self.request.user)
