from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from .models import FirmwareUpdate, Device, Firmware

class UpdateSensorDataView(APIView):
    def get(self, request, device_id, *args, **kwargs):
        try:
            spvValue = int(request.query_params.get('spvValue'))
        except (ValueError, TypeError):
            return Response(
                {
                    'error': 'Invalid input data'
                },
                status=400
            )

        try:
            device = Device.objects.get(pk=device_id)
        except Device.DoesNotExist:
            return Response(
                {
                    'error': 'Device not found'
                },
                status=404
            )

        # Get the latest firmware update for the device
        try:
            firmware_update = FirmwareUpdate.objects.filter(device_name=device).latest('uploaded_at')
        except FirmwareUpdate.DoesNotExist:
            return Response(
                {
                    'error': 'Firmware update not found for this device'
                },
                status=404
            )

        # Update the spvValue
        firmware_update.spvValue = spvValue
        firmware_update.save()

        # Return details of the device and a link to download the firmware file
        data = {
            'device_id': device.id,
            'device_name': device.device_name,
            'channel_id': device.channel_id,
            'firmware_version': firmware_update.firmware.firmware_version,
            'file_download_link': request.build_absolute_uri(firmware_update.firmware.firmware_version_file.url)
        }

        return Response(
            {
                'message': 'SPV value updated successfully',
                'data': data
            },
            status=200
        )
