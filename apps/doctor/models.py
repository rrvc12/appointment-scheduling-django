from django.db import models

# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(
        "account.UserAccount",
        blank=True,
        related_name="doctor",
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    bio = models.TextField(
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    specialities = models.ManyToManyField(
        "doctor.Speciality",
        blank=True,
        related_name="doctors",
    )

    class Meta:
        verbose_name = "Doctor Profile"
        verbose_name_plural = "Doctor Profiles"

    def __str__(self):
        return f"{self.title} {self.user.last_name}"


class Speciality(models.Model):
    name = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Speciality"
        verbose_name_plural = "Specialities"

    def __str__(self):
        return self.name
