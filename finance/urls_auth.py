from django.urls import path
from .views_auth import SignUpView

"""
URL patterns for authentication
This includes the signup view for new users
The signup view allows new users to register for an account
It uses Django's built-in UserCreationForm for user registration
The success URL redirects to the login page after successful signup
"""
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]
