# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.http import FileResponse
# from .models import FirmwareUpdate, Device, Firmware

# class UpdateSensorDataView(APIView):
#     def get(self, request, device_id, *args, **kwargs):
#         try:
#             spvValue = int(request.query_params.get('spvValue'))
#         except (ValueError, TypeError):
#             return Response(
#                 {
#                     'error': 'Invalid input data'
#                 },
#                 status=400
#             )

#         try:
#             device = Device.objects.get(pk=device_id)
#         except Device.DoesNotExist:
#             return Response(
#                 {
#                     'error': 'Device not found'
#                 },
#                 status=404
#             )

#         # Get the latest firmware update for the device
#         try:
#             firmware_update = FirmwareUpdate.objects.filter(device_name=device).latest('uploaded_at')
#         except FirmwareUpdate.DoesNotExist:
#             return Response(
#                 {
#                     'error': 'Firmware update not found for this device'
#                 },
#                 status=404
#             )

#         # Update the spvValue
#         firmware_update.spvValue = spvValue
#         firmware_update.save()

#         # Prepare the response data
#         data = {
#             'device_id': device.id,
#             'device_name': device.device_name,
#             'channel_id': device.channel_id,
#             'firmware_version': firmware_update.firmware.firmware_version,
#         }

#         # Create a file response for the firmware version file
#         file_response = FileResponse(open(firmware_update.firmware.firmware_version_file.path, 'rb'))

#         # Set the Content-Disposition header to specify the filename for download
#         file_response['Content-Disposition'] = f'attachment; filename="{firmware_update.firmware.firmware_version_file.name}"'

#         # Return the file response along with the data
#         return file_response


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
        

        if firmware_update.fileDownload == 1:
            firmware_update.fileDownload = 0
            firmware_update.save()
            # Prepare the response data
            data = {
                'device_name': device.device_name,
                'channel_id': device.channel_id,
                'firmware_version': firmware_update.firmware.firmware_version,
                'fileDownload': firmware_update.fileDownload,
                'spvValue': firmware_update.spvValue,
                'syncState': firmware_update.syncState,
                'confrigDownload': firmware_update.confrigDownload,
            }
            return Response(
                {
                    'message': 'SPV value updated successfully',
                    'data': data,
                },
                status=200
            )
        else:
            firmware_update.save()
            # Create a file response for the firmware version file
            file_response = FileResponse(open(firmware_update.firmware.firmware_version_file.path, 'rb'))

            # Set the Content-Disposition header to specify the filename for download
            file_response['Content-Disposition'] = f'attachment; filename="{firmware_update.firmware.firmware_version_file.name}"'

            # Return the file response along with the data
            return file_response
