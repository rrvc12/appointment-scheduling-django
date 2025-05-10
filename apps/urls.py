from django.urls import path, include


urlpatterns = [
    path("account/", include("apps.account.urls")),
    path("", include("apps.doctor.urls")),
    path("appointment/", include("apps.appointment.urls")),
]
