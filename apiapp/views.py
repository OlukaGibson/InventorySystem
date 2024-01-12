from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FirmwareUpdate, Device, Firmware, Fields, FirmwareUpdateField, FirmwareUpdateHistory
import json


class UpdateSensorDataView(APIView):
    def get(self, request, id, *args, **kwargs):
        # Get the device with the channel_id
        try:
            device = Device.objects.get(channel_id=id)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=404)


        # Get the latest firmware update for the device
        firmware_updates = FirmwareUpdate.objects.filter(device_name=device)
        firmware_update_data = []
        for firmware_update in firmware_updates:
            device_name = firmware_update.device_name.device_name
            channel_id = firmware_update.device_name.channel_id
            firmware_version = firmware_update.firmware.firmware_version
            firmware_update_data.append({
                'device_name': device_name,
                'channel_id': channel_id,
                'firmware_version': firmware_version,
                'fields': [] 
            })
            
            firmware_update_fields = FirmwareUpdateField.objects.filter(firmware_update=firmware_update)

            for firmware_update_field in firmware_update_fields:
                field_name = firmware_update_field.field.field_name
                field_value = firmware_update_field.value
                # Check if the field is not editable before appending
                if not firmware_update_field.field.edit:
                    firmware_update_data[-1]['fields'].append({
                        'field_name': field_name,
                        'value': field_value
                    })

        firmware_update_json = json.dumps(firmware_update_data)
        return Response(firmware_update_json, status=200)
