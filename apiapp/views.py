from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .models import FirmwareUpdate
from django.views.decorators.csrf import csrf_exempt

class UpdateSensorDataView(APIView):
    def get(self, request, device_id, *args, **kwargs):
        try:
            version = request.query_params.get('version')
            spvValue = int(request.query_params.get('spvValue'))
            batteryValue = int(request.query_params.get('batteryValue'))
        except (ValueError, TypeError):
            return Response(
                {
                'error': 'Invalid input data'
                },
                status=400
                )

        try:
            firmware_update = FirmwareUpdate.objects.get(device_id=device_id)
        except FirmwareUpdate.DoesNotExist:
            return Response(
                {
                'error': 'Device not found'
                },
                status=404
                )
        firmware_update.version = version
        firmware_update.spvValue = spvValue
        firmware_update.batteryValue = batteryValue
        firmware_update.save()
        to_show = FirmwareUpdate.objects.filter(device_id=device_id)
        return Response(
            {
                'message': 'Data updated successfully',
                'data': list(to_show.values())
                },
                status=200
                )
