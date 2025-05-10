from django.contrib.auth import get_user_model
from apps.utils import get_object

User = get_user_model()


def get_useraccount(**kwargs):
    """
    Get specific user
    """
    if "is_active" not in kwargs:
        is_active = True
        kwargs["is_active"] = is_active

    return get_object(User, **kwargs)
