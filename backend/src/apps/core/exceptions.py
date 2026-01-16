"""Custom exception handling placeholder."""
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler.

    TODO: Implement custom error response format.
    """
    return exception_handler(exc, context)
