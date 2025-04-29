from django.db import models
import uuid
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from apps.models import TimestampedModel
from django.core.exceptions import ValidationError

# Create your models here.


class UserAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):
        """
        Check if everything is ok with the user data and create a user
        """
        save_model = extra_fields.pop("save_model", True)
        # Check if the email and username are provided
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email.lower())
        if not username:
            raise ValueError("Users must have a username")
        username = username.lower()
        user = self.model(email=email, username=username, **extra_fields)
        # Set the password
        user.set_password(password)

        # Set the first and last name if provided
        first_name = extra_fields.get("first_name", None)
        last_name = extra_fields.get("last_name", None)
        user.first_name = first_name
        user.last_name = last_name

        # Save the user if save_model is True
        if save_model:
            user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractBaseUser, TimestampedModel, PermissionsMixin):
    """
    Entity that can access the system
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
    )

    email = models.EmailField(
        unique=True,
    )

    username = models.CharField(
        max_length=100,
        unique=True,
    )

    first_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = UserAccountManager()

    class Meta:
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"

    def __str__(self):
        return self.email
