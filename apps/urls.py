from django.urls import path, include


urlpatterns = [
    path('', include('apps.user.urls')),
    path('appointment/', include('apps.appointment.urls')),
]