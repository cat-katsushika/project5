from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("tasks/", include("tasks.urls")),
    path("contacts/", include("contacts.urls")),
    path("payments/", include("payments.urls")),
    path("terms-and-conditions/", include("terms_and_conditions.urls")),
]
