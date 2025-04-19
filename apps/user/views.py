from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from apps.user.serializers import UserCreateSerializer
# Create your views here.

class UserCreateView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer


