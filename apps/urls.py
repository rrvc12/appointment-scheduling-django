from django.urls import path, include


urlpatterns = [
    path("account/", include("apps.account.urls")),
    path("appointment/", include("apps.appointment.urls")),
]
