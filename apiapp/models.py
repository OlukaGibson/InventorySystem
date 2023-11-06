from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

class Device(models.Model):
    device_name = models.CharField(max_length=50, default='Device Name', null=True)
    channel_id = models.CharField(max_length=50, default='Channel ID', null=True)
    fileDownload = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.device_name

class Fields(models.Model):
    field_name = models.CharField(max_length=50, null=True)
    edit = models.BooleanField(default=False)

    def __str__(self):
        return self.field_name

class Firmware(models.Model):
    firmware_version = models.CharField(max_length=20, default='Firmware Version', null=True)
    firmware_version_file = models.FileField(upload_to='firmware/', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firmware_version

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

@receiver(post_save, sender=Fields)
def create_firmware_update_field(sender, instance, created, **kwargs):
    if created:
        firmware_updates = FirmwareUpdate.objects.all()
        for update in firmware_updates:
            FirmwareUpdateField.objects.get_or_create(firmware_update=update, field=instance, value='0')

@receiver(post_save, sender=Device)
def create_firmware_update_fields_for_device(sender, instance, created, **kwargs):
    if created:
        latest_firmware = Firmware.objects.latest('uploaded_at')
        firmware_updates = FirmwareUpdate.objects.filter(device_name=instance)
        for update in firmware_updates:
            fields = Fields.objects.all()
            for field in fields:
                FirmwareUpdateField.objects.get_or_create(firmware_update=update, field=field, value='0')
                update.firmware = latest_firmware
                update.save()

@receiver(pre_save, sender=Fields)
def update_firmware_update_fields_for_fields(sender, instance, **kwargs):
    firmware_updates = FirmwareUpdate.objects.all()
    for update in firmware_updates:
        if update.device_name:
            latest_firmware = Firmware.objects.latest('uploaded_at')
            for field in Fields.objects.all():
                if not FirmwareUpdateField.objects.filter(firmware_update=update, field=field).exists():
                    FirmwareUpdateField.objects.create(firmware_update=update, field=field, value='0')
            update.firmware = latest_firmware
            update.save()

# Connect the signals
post_save.connect(create_firmware_update_field, sender=Fields)
post_save.connect(create_firmware_update_fields_for_device, sender=Device)
pre_save.connect(update_firmware_update_fields_for_fields, sender=Fields)

class FirmwareUpdateField(models.Model):
    firmware_update = models.ForeignKey(FirmwareUpdate, on_delete=models.CASCADE)
    field = models.ForeignKey(Fields, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, default='0')

    def __str__(self):
        return f"{self.field.field_name} - {self.firmware_update.id}"

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
