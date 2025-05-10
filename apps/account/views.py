from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from apps.account.services import user_create
from apps.account.selectors import get_useraccount
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateView(APIView):
    """
    View to create a user account.
    """

    default_error_messages = {}

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(
            required=True,
            validators=[
                UniqueValidator(
                    queryset=User.objects.all(), message=("Email already exists.")
                )
            ],
        )
        username = serializers.CharField(
            min_length=3,
            max_length=150,
            required=True,
            validators=[
                UniqueValidator(
                    queryset=User.objects.all(), message=("Username already exists.")
                )
            ],
        )
        first_name = serializers.CharField(max_length=30, required=True)
        last_name = serializers.CharField(max_length=30, required=True)
        password = serializers.CharField(write_only=True, required=True)

        def validate_username(self, value):
            RESTRICTED_USERNAMES = [
                "admin",
                "undefined",
                "null",
                "superuser",
                "root",
                "system",
            ]
            if value in RESTRICTED_USERNAMES:
                raise serializers.ValidationError(
                    {"username": f"Username '{value}' is not allowed."}
                )
            return value

    def post(self, request, *args, **kwargs):
        # Create the user account
        serializer = self.InputSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = user_create(**serializer.validated_data)
            except Exception as e:
                return Response(
                    {"detail": "User creation failed.", "error": str(e)}, status=400
                )
            # We use the detail serializer to return the user data
            serializer = UserDetailView.OutputSerializer(user)

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class UserDetailView(APIView):
    """
    View to get public details of a specific user account.
    """

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        email = serializers.EmailField()
        username = serializers.CharField(max_length=150)
        first_name = serializers.CharField(max_length=30)
        last_name = serializers.CharField(max_length=30)

    def get(self, request, username, *args, **kwargs):
        # Get the user account details
        user = get_useraccount(username=username)
        if user is None:
            return Response({"detail": "User not found."}, status=404)
        serializer = self.OutputSerializer(user)
        return Response(serializer.data, status=200)
