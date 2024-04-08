from django.urls import path
from .views import ContactFormView, ContactSuccessView, NoticeView

app_name = 'contacts'

urlpatterns = [
    path('', ContactFormView.as_view(), name='contact'),
    path('success/', ContactSuccessView.as_view(), name='success'),
    path('notice/', NoticeView.as_view(), name='notice'),
]
