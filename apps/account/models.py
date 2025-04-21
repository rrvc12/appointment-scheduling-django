from django.db import models
import uuid
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from apps.models import TimestampedModel

# Create your models here.


class UserAccountManager(BaseUserManager):

    RESTRICTED_USERNAMES = ["admin", "undefined", "null", "superuser", "root", "system"]

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        first_name = extra_fields.get("first_name", None)
        last_name = extra_fields.get("last_name", None)

        if not first_name or not last_name:
            raise ValueError("Users must have a first name and last name")

        user.first_name = first_name
        user.last_name = last_name

        username = extra_fields.get("username", None)

        if username and username.lower() in self.RESTRICTED_USERNAMES:
            raise ValueError(f"The username {username} is not allowed")

        user.username = username

        user.save(using=self._db)

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
    )

    last_name = models.CharField(
        max_length=100,
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

    def __str__(self):
        return self.email
