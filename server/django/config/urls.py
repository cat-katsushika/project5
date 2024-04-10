from django.contrib import admin
from django.urls import include, path
from users.views import custom_admin_auth_view

urlpatterns = [
    path("admin/KOgEdTnMXbsDJa8jK347oaVqVzbshgIfhOWBjim9uEA5RfsEpl/", admin.site.urls),
    path("custom-admin-auth/", custom_admin_auth_view, name="custom-admin-auth"),
    path("", include("users.urls")),
    path("tasks/", include("tasks.urls")),
    path("contacts/", include("contacts.urls")),
    path("payments/", include("payments.urls")),
    path("terms-and-conditions/", include("terms_and_conditions.urls")),
]
