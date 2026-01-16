"""
Telegram Mini App authentication service.

Validates initData according to Telegram documentation:
https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
"""
import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Optional
from urllib.parse import parse_qsl

from django.conf import settings


class TelegramAuthError(Exception):
    """Base exception for Telegram auth errors."""
    pass


class InvalidInitDataError(TelegramAuthError):
    """Raised when initData format is invalid."""
    pass


class HashValidationError(TelegramAuthError):
    """Raised when hash validation fails."""
    pass


class AuthDateExpiredError(TelegramAuthError):
    """Raised when auth_date is too old."""
    pass


class MissingUserDataError(TelegramAuthError):
    """Raised when user data is missing from initData."""
    pass


@dataclass(frozen=True)
class TelegramUser:
    """Validated Telegram user data."""
    id: int
    first_name: str
    last_name: str
    username: str
    language_code: str
    is_premium: bool
    photo_url: str

    @classmethod
    def from_dict(cls, data: dict) -> 'TelegramUser':
        """Create TelegramUser from dictionary."""
        return cls(
            id=data.get('id', 0),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            username=data.get('username', ''),
            language_code=data.get('language_code', ''),
            is_premium=data.get('is_premium', False),
            photo_url=data.get('photo_url', ''),
        )


@dataclass(frozen=True)
class ValidatedInitData:
    """Result of successful initData validation."""
    user: TelegramUser
    auth_date: int
    query_id: str
    hash: str
    raw_data: dict


class TelegramAuthService:
    """
    Service for validating Telegram Mini App initData.

    Usage:
        service = TelegramAuthService()
        validated = service.validate(init_data_string)
        user = validated.user
    """

    def __init__(
        self,
        bot_token: Optional[str] = None,
        auth_timeout: Optional[int] = None,
    ):
        """
        Initialize the service.

        Args:
            bot_token: Telegram bot token. Defaults to settings.TELEGRAM_BOT_TOKEN
            auth_timeout: Max age of auth_date in seconds. Defaults to settings.TELEGRAM_AUTH_TIMEOUT
        """
        self.bot_token = bot_token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        self.auth_timeout = auth_timeout or getattr(settings, 'TELEGRAM_AUTH_TIMEOUT', 86400)

    def validate(self, init_data: str) -> ValidatedInitData:
        """
        Validate Telegram Mini App initData.

        Args:
            init_data: Raw initData string from Telegram WebApp

        Returns:
            ValidatedInitData with user information

        Raises:
            InvalidInitDataError: If initData format is invalid
            HashValidationError: If hash validation fails
            AuthDateExpiredError: If auth_date is expired
            MissingUserDataError: If user data is missing
        """
        if not init_data:
            raise InvalidInitDataError("Empty initData")

        if not self.bot_token:
            raise TelegramAuthError("TELEGRAM_BOT_TOKEN is not configured")

        # Parse initData
        try:
            parsed = dict(parse_qsl(init_data, strict_parsing=True))
        except ValueError as e:
            raise InvalidInitDataError(f"Failed to parse initData: {e}")

        # Extract and validate hash
        received_hash = parsed.pop('hash', None)
        if not received_hash:
            raise InvalidInitDataError("Missing hash in initData")

        # Validate hash
        if not self._validate_hash(parsed, received_hash):
            raise HashValidationError("Invalid hash")

        # Validate auth_date
        auth_date = self._validate_auth_date(parsed.get('auth_date'))

        # Parse and validate user data
        user = self._parse_user(parsed.get('user'))

        return ValidatedInitData(
            user=user,
            auth_date=auth_date,
            query_id=parsed.get('query_id', ''),
            hash=received_hash,
            raw_data=parsed,
        )

    def _validate_hash(self, data: dict, received_hash: str) -> bool:
        """
        Validate initData hash using HMAC-SHA256.

        Algorithm:
        1. Sort data alphabetically by key
        2. Create data_check_string: "key1=value1\nkey2=value2\n..."
        3. secret_key = HMAC-SHA256("WebAppData", bot_token)
        4. hash = HMAC-SHA256(secret_key, data_check_string)
        5. Compare with received hash
        """
        # Create data check string (sorted alphabetically)
        data_check_string = '\n'.join(
            f'{key}={value}'
            for key, value in sorted(data.items())
        )

        # Create secret key: HMAC-SHA256 of bot token with "WebAppData" as key
        secret_key = hmac.new(
            key=b'WebAppData',
            msg=self.bot_token.encode('utf-8'),
            digestmod=hashlib.sha256,
        ).digest()

        # Calculate hash
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode('utf-8'),
            digestmod=hashlib.sha256,
        ).hexdigest()

        # Constant-time comparison to prevent timing attacks
        return hmac.compare_digest(calculated_hash, received_hash)

    def _validate_auth_date(self, auth_date_str: Optional[str]) -> int:
        """Validate auth_date is not expired."""
        if not auth_date_str:
            raise InvalidInitDataError("Missing auth_date")

        try:
            auth_date = int(auth_date_str)
        except ValueError:
            raise InvalidInitDataError("Invalid auth_date format")

        current_time = int(time.time())
        age = current_time - auth_date

        if age > self.auth_timeout:
            raise AuthDateExpiredError(
                f"Auth data expired. Age: {age}s, max: {self.auth_timeout}s"
            )

        if age < -60:  # Allow 60 seconds clock skew into the future
            raise AuthDateExpiredError("Auth date is in the future")

        return auth_date

    def _parse_user(self, user_json: Optional[str]) -> TelegramUser:
        """Parse and validate user JSON."""
        if not user_json:
            raise MissingUserDataError("User data not found in initData")

        try:
            user_data = json.loads(user_json)
        except json.JSONDecodeError as e:
            raise InvalidInitDataError(f"Invalid user JSON: {e}")

        if not isinstance(user_data, dict):
            raise InvalidInitDataError("User data must be an object")

        if not user_data.get('id'):
            raise MissingUserDataError("User ID not found")

        return TelegramUser.from_dict(user_data)


# Singleton instance for convenience
_service: Optional[TelegramAuthService] = None


def get_telegram_auth_service() -> TelegramAuthService:
    """Get or create TelegramAuthService singleton."""
    global _service
    if _service is None:
        _service = TelegramAuthService()
    return _service


def validate_init_data(init_data: str) -> ValidatedInitData:
    """
    Convenience function to validate initData.

    Usage:
        from apps.users.services.telegram import validate_init_data

        validated = validate_init_data(request.data['init_data'])
        telegram_id = validated.user.id
    """
    return get_telegram_auth_service().validate(init_data)
