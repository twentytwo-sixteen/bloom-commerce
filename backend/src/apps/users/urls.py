"""User URLs."""
from django.urls import path

from apps.users.views import MeView, TelegramAuthView, TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('telegram/', TelegramAuthView.as_view(), name='telegram-auth'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', MeView.as_view(), name='me'),
]
