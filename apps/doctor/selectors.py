from .models import Doctor, Speciality
from apps.utils import get_object


def get_doctor_profile(**kwargs):
    """
    Get specific doctor profile.
    """
    return get_object(Doctor, **kwargs)


def get_speciality(**kwargs):
    return get_object(Speciality, **kwargs)
