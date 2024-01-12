from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FirmwareUpdate, Device, Firmware, Fields, FirmwareUpdateField, FirmwareUpdateHistory
import json
from django.http import HttpResponse
import mimetypes
import os

class UpdateSensorDataView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            device = Device.objects.get(channel_id=id)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=404)

        # Check if fileDownload is 0 for the device
        if device.fileDownload == 0:
            firmware_update = FirmwareUpdate.objects.filter(device_name=device).first()

            # Check if a firmware update is associated with the device
            if firmware_update:
                firmware = firmware_update.firmware

                # Download the firmware_version_file
                firmware_file_path = firmware.firmware_version_file.path
                with open(firmware_file_path, 'rb') as firmware_file:
                    response = HttpResponse(firmware_file.read(), content_type=mimetypes.guess_type(firmware_file_path)[0])
                    response['Content-Disposition'] = f'attachment; filename={os.path.basename(firmware_file_path)}'

                # Update the fileDownload field to 1
                device.fileDownload = 1
                device.save()

                return response

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
                'fields': []  # Initialize an empty list for fields
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