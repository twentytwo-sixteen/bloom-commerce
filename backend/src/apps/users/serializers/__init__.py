"""Users serializers."""
from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Профиль пользователя."""

    class Meta:
        model = User
        fields = [
            'id',
            'telegram_id',
            'first_name',
            'last_name',
            'username',
        ]
        read_only_fields = fields


class TelegramAuthSerializer(serializers.Serializer):
    """Авторизация через Telegram Mini App."""
    init_data = serializers.CharField(
        help_text='Telegram WebApp.initData'
    )
