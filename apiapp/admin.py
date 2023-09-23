from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.FirmwareUpdate)
admin.site.register(models.Firmware)
admin.site.register(models.Device)
admin.site.register(models.FirmwareUpdateHistory)