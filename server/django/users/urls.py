from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CustomLoginView, HomePageView, SignUpView, UserProfileView

app_name = "users"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path(
        "login/",
        CustomLoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", HomePageView.as_view(), name="home"),
    path("profile/<uuid:pk>/", UserProfileView.as_view(), name="profile"),
]
