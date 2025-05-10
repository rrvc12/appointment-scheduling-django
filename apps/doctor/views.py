from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.permissions import IsAdminUser
from apps.account.views import UserDetailView
from .models import Speciality
from .services import (
    create_doctor_profile,
    update_doctor_profile,
    delete_doctor_profile,
    create_speciality,
    update_speciality,
    delete_speciality,
)
from .selectors import get_doctor_profile, get_speciality
from .permissions import (
    CreateDoctorPermission,
    UpdateDoctorPermission,
    DeleteDoctorPermission,
)

# Create your views here.


class SpecialityCreateView(APIView):
    permission_classes = [IsAdminUser]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=30, required=True)
        description = serializers.CharField(allow_blank=True)

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        if serializer.is_valid():
            try:
                speciality = create_speciality(**serializer.validated_data)
            except Exception as e:
                return Response(
                    {"detail": "Speciality creation failed.", "error": str(e)},
                    status=400,
                )

            data = SpecialityDetailView.OutputSerializer(speciality).data
            return Response(data, status=201)
        return Response(serializer.errors, status=400)


class SpecialityDetailView(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        description = serializers.CharField()

    def get(self, request, pk, *args, **kwargs):
        # Get the speciality
        speciality = get_speciality(pk=pk)
        if speciality is None:
            return Response({"detail": "Speciality not found."}, status=404)
        serializer = self.OutputSerializer(speciality)
        return Response(serializer.data, status=200)


class SpecialityUpdateView(APIView):
    permission_classes = [IsAdminUser]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=30, required=False)
        description = serializers.CharField(allow_blank=True, required=False)

    def put(self, request, pk, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        speciality = get_speciality(pk=pk)
        if speciality is None:
            return Response({"detail": "Speciality not found."}, status=404)

        try:
            updated_speciality = update_speciality(
                speciality, serializer.validated_data
            )
        except Exception as e:
            return Response(
                {"detail": "Speciality update failed.", "error": str(e)},
                status=400,
            )

        data = SpecialityDetailView.OutputSerializer(updated_speciality).data
        return Response(data)


class SpecialityDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk, *args, **kwargs):
        speciality = get_speciality(pk=pk)
        if speciality is None:
            return Response({"detail": "Speciality not found."}, status=404)
        try:
            delete_speciality(speciality)
        except Exception as e:
            return Response(
                {"detail": "Speciality deletion failed.", "error": str(e)},
                status=400,
            )
        return Response({"detail": "Speciality deleted."}, status=200)


class DoctorCreateView(APIView):
    permission_classes = [CreateDoctorPermission]

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=30, required=True)
        bio = serializers.CharField(allow_blank=True)
        phone = serializers.CharField(max_length=30, required=True)
        specialities = serializers.PrimaryKeyRelatedField(
            queryset=Speciality.objects.all(),
            many=True,
            write_only=True,
            required=True,
            error_messages={
                "does_not_exist": "A speciality that does not exist has entered"
            },
        )

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        if serializer.is_valid():
            try:
                doctor = create_doctor_profile(user, **serializer.validated_data)
            except Exception as e:
                return Response(
                    {"detail": "Doctor profile creation failed.", "error": str(e)},
                    status=400,
                )

            data = DoctorDetailView.OutputSerializer(doctor).data
            return Response(data, status=201)
        return Response(serializer.errors, status=400)


class DoctorDetailView(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        user = UserDetailView.OutputSerializer()
        title = serializers.CharField()
        bio = serializers.CharField()
        phone = serializers.CharField()
        specialities = SpecialityDetailView.OutputSerializer(many=True)

    def get(self, request, pk, *args, **kwargs):
        # Get the doctor profile
        doctor = get_doctor_profile(pk=pk)
        if doctor is None:
            return Response({"detail": "Doctor profile not found."}, status=404)
        serializer = self.OutputSerializer(doctor)
        return Response(serializer.data, status=200)


class DoctorUpdateView(APIView):
    permission_classes = [UpdateDoctorPermission]

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=30, required=False)
        bio = serializers.CharField(allow_blank=True, required=False)
        phone = serializers.CharField(max_length=30, required=False)
        specialities = serializers.PrimaryKeyRelatedField(
            queryset=Speciality.objects.all(),
            many=True,
            write_only=True,
            required=False,
            error_messages={
                "does_not_exist": "A speciality that does not exist has entered"
            },
        )

    def put(self, request, pk, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor = get_doctor_profile(pk=pk)
        if doctor is None:
            return Response({"detail": "Doctor profile not found."}, status=404)
        # Only the owner or admin can update the doctor profile
        self.check_object_permissions(self.request, doctor)
        try:
            updated_doctor = update_doctor_profile(doctor, serializer.validated_data)
        except Exception as e:
            return Response(
                {"detail": "Doctor update failed.", "error": str(e)},
                status=400,
            )

        data = DoctorDetailView.OutputSerializer(updated_doctor).data
        return Response(data)


class DoctorDeleteView(APIView):
    permission_classes = [DeleteDoctorPermission]

    def post(self, request, pk, *args, **kwargs):
        doctor = get_doctor_profile(pk=pk)
        if doctor is None:
            return Response({"detail": "Doctor profile not found."}, status=404)
        # Only the owner or admin can delete the doctor pro
        self.check_object_permissions(self.request, doctor)
        try:
            delete_doctor_profile(doctor)
        except Exception as e:
            return Response(
                {"detail": "Doctor profile deletion failed.", "error": str(e)},
                status=400,
            )
        return Response({"detail": "Doctor profile deleted."}, status=200)
