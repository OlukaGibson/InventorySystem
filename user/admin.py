from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Profile
from . import models
# Register your models here.

class profileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...

admin.site.register(models.Profile, profileAdmin)