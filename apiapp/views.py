from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FirmwareUpdate, Device, Firmware, Fields, FirmwareUpdateField
import json
import boto3
from botocore.exceptions import NoCredentialsError
import os

class UpdateSensorDataView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            device = Device.objects.get(channel_id=id)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=404)

        firmware_updates = FirmwareUpdate.objects.filter(device_name=device)
        firmware_update_data = []

        for firmware_update in firmware_updates:
            device_name = firmware_update.device_name.device_name
            channel_id = firmware_update.device_name.channel_id
            firmware_version = firmware_update.firmware.firmware_version
            file_download_status = device.fileDownload

            # Check if fileDownload is 0, download firmware_version_file, and update fileDownload to 1
            if file_download_status == 0:
                try:
                    # Replace 'YOUR_S3_ACCESS_KEY_ID', 'YOUR_S3_SECRET_ACCESS_KEY', and 'YOUR_S3_BUCKET_NAME'
                    # with your actual AWS S3 credentials and bucket name
                    s3 = boto3.client('s3', aws_access_key_id='AKIA6NMN75IGSRMXX5PQ',
                                      aws_secret_access_key='mHq/SXo07OfzDPrIDrSLKFK57t0+YXTgZHGYB9Ra')

                    firmware_file_key = str(firmware_update.firmware.firmware_version_file)
                    firmware_file_path = 'firmwares/' + firmware_file_key
                    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
                    local_file_path = os.path.join(downloads_folder, firmware_file_key)

                    s3.download_file('fota-updates1', firmware_file_path, local_file_path)

                    # Update fileDownload status in the Device model
                    device.fileDownload = 1
                    device.save()

                except NoCredentialsError:
                    return Response({'error': 'AWS credentials not available'}, status=500)

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
