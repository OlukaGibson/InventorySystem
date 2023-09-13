from django.urls import path
from .views import UpdateSensorDataView

urlpatterns = [
    path('update-sensor-data/<str:device_id>', UpdateSensorDataView.as_view(), name='update-sensor-data'),
]
