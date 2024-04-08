from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    create_checkout_session_view,
    PaymentSuccessView,
    PaymentCancelView,
)

app_name = "payments"

urlpatterns = [
    path("create-checkout-session/<uuid:pk>/", create_checkout_session_view, name="create_checkout_session"),
    path("success/<uuid:pk>", PaymentSuccessView.as_view(), name="success"),
    path("cancel/<uuid:pk>", PaymentCancelView.as_view(), name="cancel"),

]
