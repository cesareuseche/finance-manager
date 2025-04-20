from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

"""
URL patterns for authentication
This includes the signup view for new users
The signup view allows new users to register for an account
It uses Django's built-in UserCreationForm for user registration
The success URL redirects to the login page after successful signup
This view can be extended to include additional functionality in the future
"""
class SignUpView(CreateView):
    form_class    = UserCreationForm
    template_name = "registration/signup.html"
    success_url   = reverse_lazy("login")
