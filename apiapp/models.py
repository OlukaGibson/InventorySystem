
from django.db import models

class Device(models.Model):
    device_name = models.CharField(max_length=50)
    channel_id = models.CharField(max_length=50)
    created_at = models.DateTimeField()

    def __str__(self):  
        return self.device_name

class Firmware(models.Model):
    firmware_version = models.CharField(max_length=20)
    firmware_version_file = models.FileField(upload_to='firmware/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firmware_version

class FirmwareUpdate(models.Model):
    device_name = models.ForeignKey(Device, on_delete=models.CASCADE)
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    fileDownload = models.IntegerField()
    spvValue = models.PositiveIntegerField()
    syncState = models.IntegerField()
    confrigDownload = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device_name
    
class FirmwareUpdateHistory(models.Model):
    device_name = models.ForeignKey(Device, on_delete=models.CASCADE)
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    fileDownload = models.IntegerField()
    spvValue = models.PositiveIntegerField()
    syncState = models.IntegerField()
    confrigDownload = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=False)
    history_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.device_name
    
