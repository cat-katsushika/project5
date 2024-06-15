from django.urls import path

from .views import HomePageView, UserDeactivateConfirmView, UsernameChangeView, UserProfileView, deactivate_account_view

app_name = "users"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("profile/<uuid:pk>/", UserProfileView.as_view(), name="profile"),
    path("profile/change_username/", UsernameChangeView.as_view(), name="change_username"),
    path("users/deactivate/", deactivate_account_view, name="deactivate"),
    path(
        "users/deactivate/confirm/",
        UserDeactivateConfirmView.as_view(),
        name="deactivate_confirm",
    ),
]
