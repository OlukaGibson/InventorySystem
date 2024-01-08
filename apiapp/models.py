from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Device(models.Model):
    device_name = models.CharField(max_length=50,default='Device Name', null=True)
    channel_id = models.CharField(max_length=50,default='Channel ID', null=True)
    fileDownload = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):  
        return self.device_name

class Firmware(models.Model):
    firmware_version = models.CharField(max_length=20, null=True)
    firmware_version_file = models.FileField(upload_to='', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firmware_version

class Fields(models.Model):
    field_name = models.CharField(max_length=50, null=True)
    edit = models.BooleanField(default=False)
    

    def __str__(self):
        return self.field_name

class FirmwareUpdate(models.Model):
    device_name = models.ForeignKey(Device, on_delete=models.CASCADE)
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Firmware: {self.firmware.firmware_version} for Device: {self.device_name.device_name}"

    def save(self, *args, **kwargs):
        super(FirmwareUpdate, self).save(*args, **kwargs)

        # Create a FirmwareUpdateField for each field with an initial value of '0'
        fields = Fields.objects.all()
        for field in fields:
            FirmwareUpdateField.objects.get_or_create(firmware_update=self, field=field, value='0')

            
class FirmwareUpdateField(models.Model):
    firmware_update = models.ForeignKey(FirmwareUpdate, on_delete=models.CASCADE)
    field = models.ForeignKey(Fields, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, default='0')

    def __str__(self):
        return f"{self.field.field_name} - {self.firmware_update.id}"

# Use the post_save signal to create a new FirmwareUpdateField when a new Fields instance is created
@receiver(post_save, sender=Fields)
def create_firmware_update_field(sender, instance, created, **kwargs):
    if created:
        firmware_updates = FirmwareUpdate.objects.all()
        for update in firmware_updates:
            FirmwareUpdateField.objects.create(firmware_update=update, field=instance, value='0')

# Connect the signal
post_save.connect(create_firmware_update_field, sender=Fields)


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
    
