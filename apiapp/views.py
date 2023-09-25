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

        # Prepare the response data
        data = {
            'device_id': device.id,
            'device_name': device.device_name,
            'channel_id': device.channel_id,
            'firmware_version': firmware_update.firmware.firmware_version,
        }

        # Create a file response for the firmware version file
        file_response = FileResponse(open(firmware_update.firmware.firmware_version_file.path, 'rb'))

        # Set the Content-Disposition header to specify the filename for download
        file_response['Content-Disposition'] = f'attachment; filename="{firmware_update.firmware.firmware_version_file.name}"'

        # Return the file response along with the data
        return file_response

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

#         # Create a file response for the firmware file
#         file_response = FileResponse(open(firmware_update.firmware.firmware_version_file.path, 'rb'))

#         # Set the Content-Disposition header to specify the filename for download
#         file_response['Content-Disposition'] = f'attachment; filename="{firmware_update.firmware.firmware_version_file.name}"'

#         # Return the data and the file response in a single response
#         response_data = {
#             'message': 'SPV value updated successfully',
#             'data': data,
#             'file': file_response
#         }

#         return response_data


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.http import JsonResponse
# from .models import FirmwareUpdate
# from django.views.decorators.csrf import csrf_exempt

# class UpdateSensorDataView(APIView):
#     def get(self, request, device_id, *args, **kwargs):
#         try:
#             version = request.query_params.get('version')
#             spvValue = int(request.query_params.get('spvValue'))
#             batteryValue = int(request.query_params.get('batteryValue'))
#         except (ValueError, TypeError):
#             return Response(
#                 {
#                 'error': 'Invalid input data'
#                 },
#                 status=400
#                 )

#         try:
#             firmware_update = FirmwareUpdate.objects.get(device_id=device_id)
#         except FirmwareUpdate.DoesNotExist:
#             return Response(
#                 {
#                 'error': 'Device not found'
#                 },
#                 status=404
#                 )
#         firmware_update.version = version
#         firmware_update.spvValue = spvValue
#         firmware_update.batteryValue = batteryValue
#         firmware_update.save()
#         to_show = FirmwareUpdate.objects.filter(device_id=device_id)
#         return Response(
#             {
#                 'message': 'Data updated successfully',
#                 'data': list(to_show.values())
#                 },
#                 status=200
#                 )
