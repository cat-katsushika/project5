from django.urls import path

from . import views

app_name = "terms_and_conditions"

urlpatterns = [
    path("terms-of-service/", views.terms_of_service, name="terms_of_service"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("specified-commercial-transaction-act/", views.specified_commercial_transaction_act, name="specified_commercial_transaction_act"),
]