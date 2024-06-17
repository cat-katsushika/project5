from django.urls import path

from .views import UserAnalyticsView

app_name = "analytics"

urlpatterns = [
    path("user/<uuid:pk>", UserAnalyticsView.as_view(), name="user_analytics"),
]
