from allauth.account.views import logout
from allauth.socialaccount.providers.google.views import oauth2_callback, oauth2_login

from django.conf import settings
from django.conf.urls.static import static
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
    path("accounts/logout/", logout, name="account_logout"),
    path("accounts/google/login/", oauth2_login, name="google_login"),
    path("accounts/google/login/callback/", oauth2_callback, name="google_callback"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
