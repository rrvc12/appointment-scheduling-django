from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Speciality
from .services import (
    create_doctor_profile,
    update_doctor_profile,
    create_speciality,
    update_speciality,
)
from .selectors import get_doctor_profile, get_speciality
from .permissions import CreateDoctorPermission

# Create your views here.


class SpecialityCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

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
    permission_classes = [IsAuthenticated, IsAdminUser]

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


class DoctorCreateView(APIView):
    permission_classes = [IsAuthenticated, CreateDoctorPermission]

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
                create_doctor_profile(user, **serializer.validated_data)
            except Exception as e:
                return Response(
                    {"detail": "Doctor profile creation failed.", "error": str(e)},
                    status=400,
                )

            data = DoctorDetailView.OutputSerializer(user.doctor).data
            return Response(data, status=201)
        return Response(serializer.errors, status=400)


class DoctorDetailView(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
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

        try:
            updated_doctor = update_doctor_profile(doctor, serializer.validated_data)
        except Exception as e:
            return Response(
                {"detail": "Doctor update failed.", "error": str(e)},
                status=400,
            )

        data = DoctorDetailView.OutputSerializer(updated_doctor).data
        return Response(data)
