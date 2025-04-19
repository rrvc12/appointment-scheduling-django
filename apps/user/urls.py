from django.urls import path
from apps.user.views import UserCreateView

app_name = "user"

urlpatterns = [
    path("create_user/", UserCreateView.as_view(), name="create_user")
]