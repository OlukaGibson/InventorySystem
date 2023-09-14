from django.urls import path
from .views import UpdateSensorDataView
from . import views

urlpatterns = [
    path('update-sensor-data/<str:device_id>', UpdateSensorDataView.as_view(), name='update-sensor-data'),
    path('api_url/', views.api_url,name='api_url'),
    path('display_firmware_update/', views.display_firmware_update, name='display_firmware_update'),
    path('update_selected_values/', views.update_selected_values, name='update_selected_values'),
    #path('add-firmware-update/', views.add_firmware_update, name='add-firmware-update'),
]
