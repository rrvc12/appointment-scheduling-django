from django.urls import path
from apps.doctor import views

app_name = "doctor"

urlpatterns = [
    path("doctor/create/", views.DoctorCreateView.as_view(), name="doctor_create"),
    path("doctor/<int:pk>/", views.DoctorDetailView.as_view(), name="doctor_detail"),
    path(
        "doctor/update/<int:pk>/",
        views.DoctorUpdateView.as_view(),
        name="doctor_update",
    ),
    path(
        "speciality/create/",
        views.SpecialityCreateView.as_view(),
        name="speciality_create",
    ),
    path("delete/<int:pk>/", views.DoctorDeleteView.as_view(), name="doctor_delete"),
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
    path(
        "speciality/delete/<int:pk>/",
        views.SpecialityDeleteView.as_view(),
        name="speciality_delete",
    ),
]
