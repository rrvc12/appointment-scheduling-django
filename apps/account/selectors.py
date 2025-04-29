from django.contrib.auth import get_user_model
from apps.utils import get_object

User = get_user_model()


def get_user_by_username(username: str):
    """
    Get specific user by username.
    """

    return get_object(User, username=username)
