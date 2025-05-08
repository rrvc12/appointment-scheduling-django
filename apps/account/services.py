from django.db import transaction
from apps.account.models import UserAccount
from rest_framework.exceptions import ValidationError


@transaction.atomic
def user_create(
    email: str,
    username: str,
    first_name: str,
    last_name: str,
    password: str,
) -> UserAccount:
    """
    Create a user account.
    """
    user = UserAccount.objects.create_user(
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        save_model=False,
    )
    # Validate the user data
    user.full_clean()
    user.save()
    return user
