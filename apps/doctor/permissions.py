from rest_framework.permissions import BasePermission

doctor_perms = {
    "create": "doctor.add_doctor",
    "read": "doctor.view_doctor",
    "update": "doctor.change_doctor",
    "delete": "doctor.delete_doctor",
}


class CreateDoctorPermission(BasePermission):
    """ """

    def has_permission(self, request, view):
        return request.user.has_perm(doctor_perms["create"])


class ReadDoctorPermission(BasePermission):
    """ """

    def has_permission(self, request, view):
        return request.user.has_perm(doctor_perms["read"])


class UpdateDoctorPermission(BasePermission):
    """ """

    def has_permission(self, request, view):
        return request.user.has_perm(doctor_perms["update"])


class DeleteDoctorPermission(BasePermission):
    """ """

    def has_permission(self, request, view):
        return request.user.has_perm(doctor_perms["delete"])
