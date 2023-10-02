
from django.db import models

class Device(models.Model):
    device_name = models.CharField(max_length=50,default='Device Name', null=True)
    channel_id = models.CharField(max_length=50,default='Channel ID', null=True)
    created_at = models.DateTimeField(auto_created=True, null=True)

    def __str__(self):  
        return self.device_name

class Firmware(models.Model):
    firmware_version = models.CharField(max_length=20, default='Firmware Version', null=True)
    firmware_version_file = models.FileField(upload_to='firmware/', null=True)
    uploaded_at = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.firmware_version

class Fields(models.Model):
    field_name = models.CharField(max_length=50, default='Field Name', null=True)
    field_value = models.CharField(max_length=50, default='Field Value', null=True)

    def __str__(self):
        return self.field_name

class FirmwareUpdate(models.Model):
    device_name = models.ForeignKey(Device, on_delete=models.CASCADE)
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    field = models.ManyToManyField(Fields)
    
    # fileDownload = models.IntegerField(default=0, null=True)
    # spvValue = models.PositiveIntegerField(default=0, null=True)
    # syncState = models.IntegerField(default=0, null=True)
    # confrigDownload = models.IntegerField(default=0, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Firmware: {self.firmware.firmware_version} for Device: {self.device_name.device_name}"

class FirmwareUpdateHistory(models.Model):
    device_name = models.ForeignKey(Device, on_delete=models.CASCADE)
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    fileDownload = models.IntegerField(default=0, null=True)
    spvValue = models.PositiveIntegerField(default=0, null=True)
    syncState = models.IntegerField(default=0, null=True)
    confrigDownload = models.IntegerField(default=0, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    history_date = models.DateTimeField(auto_created=True, null=True)

    def __str__(self):
        return f"History for Device: {self.device_name.device_name}, Firmware: {self.firmware.firmware_version}"
    
