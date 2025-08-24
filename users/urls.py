from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegistrationView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("user/update/", views.UserUpdateView.as_view()),
    path("user/profile/", views.UserProfileView.as_view()),
]