from django.urls import path
from apps.doctor import views

app_name = "doctor"

urlpatterns = [
    path("create/", views.DoctorCreateView.as_view(), name="doctor_create"),
    path("<int:pk>/", views.DoctorDetailView.as_view(), name="doctor_detail"),
    path("update/<int:pk>/", views.DoctorUpdateView.as_view(), name="doctor_update"),
    path(
        "speciality/create/",
        views.SpecialityCreateView.as_view(),
        name="speciality_create",
    ),
    path(
        "speciality/<int:pk>/",
        views.SpecialityDetailView.as_view(),
        name="speciality_detail",
    ),
    path(
        "speciality/update/<int:pk>/",
        views.SpecialityUpdateView.as_view(),
        name="speciality_update",
    ),
]
