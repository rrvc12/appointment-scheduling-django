from django.urls import path
from apps.account import views

app_name = "account"

urlpatterns = [
    path("create/", views.UserCreateView.as_view(), name="user_create"),
    path("<str:username>/", views.UserDetailView.as_view(), name="user_detail"),
]
