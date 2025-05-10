from rest_framework import permissions

doctor_perms = {
    "create": "doctor.add_doctor",
    "read": "doctor.view_doctor",
    "update": "doctor.change_doctor",
    "delete": "doctor.delete_doctor",
}


class CreateDoctorPermission(permissions.IsAuthenticated):
    """
    Check if is authenticated and has permission to create a doctor
    """

    def has_permission(self, request, view):
        res = super().has_permission(request, view)
        return res and request.user.has_perm(doctor_perms["create"])


class UpdateDoctorPermission(permissions.IsAuthenticated):
    """
    Check if is authenticated and has permission to update a doctor
    Check the object permission if the user is the owner or is staff
    """

    def has_permission(self, request, view):
        res = super().has_permission(request, view)
        return res and request.user.has_perm(doctor_perms["update"])

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_staff or obj.user.pk == user.pk


class DeleteDoctorPermission(permissions.IsAuthenticated):
    """
    Check if is authenticated and has permission to delete a doctor
    Check the object permission if the user is the owner or is staff
    """

    def has_permission(self, request, view):
        res = super().has_permission(request, view)
        return res and request.user.has_perm(doctor_perms["delete"])

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_staff or obj.user.pk == user.pk
