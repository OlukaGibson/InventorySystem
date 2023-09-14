from django import forms
from .models import FirmwareUpdate

class FirmwareUpdateForm(forms.ModelForm):
    class Meta:
        model = FirmwareUpdate
        fields = ['version', 'description', 'spvValue', 'batteryValue', 'device_id']
