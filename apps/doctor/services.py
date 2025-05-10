from django.db import transaction
from apps.account.models import UserAccount
from apps.doctor.models import Doctor, Speciality
from apps.utils import update_object, delete_object


# == DOCTOR PROFILE ==


@transaction.atomic
def create_doctor_profile(
    user: UserAccount, title: str, bio: str, phone: str, specialities: Speciality
) -> Doctor:
    """
    Creates the doctor profile for a specific user
    """

    doctor = Doctor(user=user, title=title, bio=bio, phone=phone)
    doctor.full_clean()
    doctor.save()
    doctor.specialities.set(specialities)

    return doctor


@transaction.atomic
def update_doctor_profile(doctor: Doctor, data) -> Doctor:

    doctor = update_object(doctor, data)

    return doctor


@transaction.atomic
def delete_doctor_profile(doctor: Doctor) -> None:
    """
    Deletes the doctor profile
    """
    delete_object(doctor)


# == SPECIALITY ==


@transaction.atomic
def create_speciality(name: str, description: str) -> Speciality:
    speciality = Speciality(name=name, description=description)

    speciality.full_clean()
    speciality.save()

    return speciality


@transaction.atomic
def update_speciality(speciality: Speciality, data) -> Speciality:

    speciality = update_object(speciality, data)

    return speciality


def delete_speciality(speciality: Speciality) -> None:
    """
    Deletes the speciality
    """
    delete_object(speciality)
