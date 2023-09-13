from django.contrib import admin
from .models import Casing, Stock, Production, StockHistory
from import_export.admin import ImportExportModelAdmin
from . import models

# Register your models here.

class casingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...

admin.site.register(models.Casing, casingAdmin)

class stockAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...

admin.site.register(models.Stock, stockAdmin)

class productionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...

admin.site.register(models.Production, productionAdmin)

class stockHistoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...

admin.site.register(models.StockHistory, stockHistoryAdmin)

# admin.site.register(Casing)
# admin.site.register(Production)
# admin.site.register(Stock)
# admin.site.register(StockHistory)