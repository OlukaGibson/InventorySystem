from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FirmwareUpdate, Device, Firmware, Fields, FirmwareUpdateField, FirmwareUpdateHistory
import json

class UpdateSensorDataView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            device = Device.objects.get(channel_id=id)
        except Device.DoesNotExist:
            return Response(
                {
                    'error': 'Device not found'
                },
                status=404
            )

        # Get the latest firmware updates for the device
        firmware_updates = FirmwareUpdate.objects.filter(device_name=device)


        for firmware_update in firmware_updates:
            if firmware_update.device_name.channel_id == id:
                device_name = firmware_update.device_name.device_name
                channel_id = firmware_update.device_name.channel_id
                firmware_version = firmware_update.firmware.firmware_version
                fields = firmware_update.fields.all()
                field_data = []

                for field in fields:
                    firmware_update_field = FirmwareUpdateField.objects.get(
                        firmware_update=firmware_update, field=field)
                    field_data.append({
                        'field_name': field.field_name,
                        'value': firmware_update_field.value
                    })

                firmware_update_data = {
                    'device_name': device_name,
                    'channel_id': channel_id,
                    'firmware_version': firmware_version,
                    'fields': field_data
                }

        # Convert the data to JSON
        firmware_update_json = json.dumps(firmware_update_data)

        return Response(firmware_update_json, status=200)
