from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    CustomLoginView,
    HomePageView,
    SignUpView,
    UserDeactivateConfirmView,
    UsernameChangeView,
    UserProfileRedirectView,
    UserProfileView,
    deactivate_account_view,
)

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
    path("profile/redirect/", UserProfileRedirectView.as_view(), name="profile_redirect"),
    path("profile/change_username/", UsernameChangeView.as_view(), name="change_username"),
    path("users/deactivate/", deactivate_account_view, name="deactivate"),
    path(
        "users/deactivate/confirm/",
        UserDeactivateConfirmView.as_view(),
        name="deactivate_confirm",
    ),
]
