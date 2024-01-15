
import csv
import xlwt
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Stock, Casing, Production,StockHistory
from .forms import InventoryForm, EditForm, CasingForm, THTForm,  MyForm, TheForm, NewStockForm, DispenseForm, UploadFileForm, NewField, NewDevice, NewFirmwareUpdate
from django.contrib.auth.models import User
from user.models import Profile
from django.db.models import Avg
from datetime import datetime, timedelta
from apiapp.models import FirmwareUpdate, FirmwareUpdateHistory, Device, Firmware, FirmwareUpdateField, Fields
from django.http import FileResponse


# Create your views here.

@login_required
def index(request):
    items = Production.objects.all()
    if request.method == 'POST' :
        form = MyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = MyForm()

    
    context = {
        'items' : items,
        'form' : form,
    }
    return render(request,'dashboard/index.html', context)

@login_required
def staff(request):
    items = User.objects.all()
    # profile_items = Profile.objects.all()
    # user_items = User.objects.all()
    context = {
        'items' : items
    }
    return render(request,'dashboard/staff.html',context)

@login_required
def reports_pcb(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() + timedelta(days=1)  # Add 1 day to include the end date
            data = Production.objects.filter(phase='tunning',date_end__range=(start_date, end_date)).values('date_end__week').annotate(average=Avg('quantity_out'))
            weekly_averages = []

            for entry in data:
                week = entry['date_end__week']
                average = entry['average']
                weekly_averages.append({'week': week, 'average': average})
        else:
            weekly_averages = []
    else:
        weekly_averages = []

    context = {
        'weekly_averages': weekly_averages,
    }
    return render(request, 'dashboard/reports_pcb.html', context)

@login_required
def reports_communication_config(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() + timedelta(days=1)  # Add 1 day to include the end date
            data = Production.objects.filter(phase='communication config',date_end__range=(start_date, end_date)).values('date_end__week').annotate(average=Avg('quantity_out'))
            weekly_averages = []

            for entry in data:
                week = entry['date_end__week']
                average = entry['average']
                weekly_averages.append({'week': week, 'average': average})
        else:
            weekly_averages = []
    else:
        weekly_averages = []

    context = {
        'weekly_averages': weekly_averages,
    }
    return render(request, 'dashboard/reports_communication_config.html', context)

@login_required
def reports_correction(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() + timedelta(days=1)  # Add 1 day to include the end date
            data = Production.objects.filter(phase='correction',date_end__range=(start_date, end_date)).values('date_end__week').annotate(average=Avg('quantity_out'))
            weekly_averages = []

            for entry in data:
                week = entry['date_end__week']
                average = entry['average']
                weekly_averages.append({'week': week, 'average': average})
        else:
            weekly_averages = []
    else:
        weekly_averages = []

    context = {
        'weekly_averages': weekly_averages,
    }
    return render(request, 'dashboard/reports_correction.html', context)

@login_required
def products(request):
    items = Stock.objects.all().order_by('-stock_out_date')
    invetory = []
    available = []

    for item in items:
        result = round(item.stock_in - item.stock_out, 0)  # Perform the computation for each item
        invetory.append(result)
        if item.stock_in == 0:
            avail = 0.0
        else:
            avail = round((result / item.stock_in) * 100, 0)
        available.append(avail) 
    #if request.method == 'POST' :
    
    form = InventoryForm(request.POST or None)
    if form.is_valid():
    #editted here
        form.save()
        return redirect('products')
    
    final = zip(items, invetory, available)

    
    context = {
        'items' : items,
        'form' : form,
        'invetory': invetory,
        'available': available,
        'final' : final
    }
    return render(request,'dashboard/products.html', context)

@login_required
def metadata(request):
    return render(request,'dashboard/metadata.html')


@login_required
def details(request,pk):
    item = Stock.objects.get(id=pk)
    if request.method == 'POST':
        newStockForm = NewStockForm(request.POST, instance=item)
        dispenseForm = DispenseForm(request.POST, instance=item)
        if newStockForm.is_valid():
            history = StockHistory.objects.create(item_name=item.item_name,
                                  stock_in=item.stock_in,
                                  stock_out=item.stock_out,
                                  stock_in_date=item.stock_in_date,
                                  stock_out_date=item.stock_out_date)
            history.save()
            newStockForm.save()
            return redirect('products')
        
        if dispenseForm.is_valid():
            history = StockHistory.objects.create(item_name=item.item_name,
                                  stock_in=item.stock_in,
                                  stock_out=item.stock_out,
                                  stock_in_date=item.stock_in_date,
                                  stock_out_date=item.stock_out_date)
            history.save()
            dispenseForm.save()
            return redirect('products')
        
    else:
        newStockForm = NewStockForm(instance=item)
        dispenseForm = DispenseForm(instance=item)
    context = {
        'newStockForm' : newStockForm,
        'dispenseForm' : dispenseForm,
        'item' : item
    }
    return render(request,'dashboard/details.html',context)

@login_required
def edit_inventory(request,pk):
    item = Stock.objects.get(id=pk)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = EditForm(instance=item)
    context = {
        'form' : form,
        'item' : item
    }
    return render(request,'dashboard/edit_inventory.html',context)

@login_required
def edit_casing(request,pk):
    item = Casing.objects.get(id=pk)
    if request.method == 'POST':
        form = CasingForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('casing')
    else:
        form = CasingForm(instance=item)
    context = {
        'form' : form,
        'item' : item,
    }
    return render(request,'dashboard/edit_casing.html',context)

@login_required
def casing(request):
    items = Casing.objects.all()
    if request.method == 'POST' :
        form = CasingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('casing')
    else:
        form = CasingForm()

    context = {
        'items' : items,
        'form' : form,
    }
    return render(request,'dashboard/casing.html', context)


@login_required
def phase1_tht(request):
    phase = "THT"
    items = Production.objects.raw('SELECT * FROM dashboard_production WHERE phase = %s',[phase])
    #items = Production.objects.all()
    if request.method == 'POST' :
        form = THTForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('phase1_tht')
    else:
        form = THTForm()

    context = {
        'items' : items,
        'form' : form,
    }
    return render(request,'dashboard/phase1_tht.html', context)

@login_required
def phase2_smt(request):
    phase = "SMT"
    items = Production.objects.raw('SELECT * FROM dashboard_production WHERE phase = %s',[phase])
    #items = Production.objects.all()
    if request.method == 'POST' :
        form = TheForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('phase2_smt')
    else:
        form = THTForm()

    context = {
        'items' : items,
        'form' : form,
    }
    return render(request,'dashboard/phase2_smt.html', context)


@login_required
def edit_phase2_smt(request,pk):
    item = Production.objects.get(id=pk)
    if request.method == 'POST':
        form = THTForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            if item.phase == 'SMT':
                return redirect('phase2_smt')
            elif item.phase == 'THT':
                return redirect('phase1_tht')
            elif item.phase == 'tunning':
                return redirect('phase3_tunning')
            elif item.phase == 'monitor assembly':
                return redirect('monitor_assembly')
            elif item.phase == 'communication config':
                return redirect('communication_config')
            elif item.phase == 'analysis':
                return redirect('analysis')
            elif item.phase == 'correction':
                return redirect('correction')
            else:
                return redirect('index')
    else:
        form = THTForm(instance=item)
    context = {
        'form' : form,
        'item' : item,
    }
    return render(request,'dashboard/edit_phase2_smt.html',context)

@login_required
def phase3_tunning(request):
    phase = "tunning"
    items = Production.objects.raw('SELECT * FROM dashboard_production WHERE phase = %s',[phase])
    # items = Production.objects.all()
    if request.method == 'POST' :
        form = THTForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('phase3_tunning')
    else:
        form = THTForm()

    context = {
        'items' : items,
        'form' : form,
    }
    return render(request,'dashboard/phase3_tunning.html', context)

@login_required
def monitor_assembly(request):
    phase = "monitor assembly"
    items = Production.objects.raw('SELECT * FROM dashboard_production WHERE phase = %s',[phase])
    # items = Production.objects.all()
    if request.method == 'POST' :
        form = THTForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('monitor_assembly')
    else:
        form = THTForm()

    context = {
        'items' : items,
        'form' : form,
    }
    return render(request,'dashboard/monitor_assembly.html', context)

@login_required
def communication_config(request):
    phase = "communication config"
    items = Production.objects.raw('SELECT * FROM dashboard_production WHERE phase = %s',[phase])
    # items = Production.objects.all()
    if request.method == 'POST' :
        form = THTForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('communication_config')
    else:
        form = THTForm()

    context = {
        'items' : items,
        'form' : form,
    }
    return render(request,'dashboard/communication_config.html', context)

@login_required
def analysis(request):
    phase = "analysis"
    items = Production.objects.raw('SELECT * FROM dashboard_production WHERE phase = %s',[phase])
    # items = Production.objects.all()
    if request.method == 'POST' :
        form = THTForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('analysis')
    else:
        form = THTForm()

    context = {
        'items' : items,
        'form' : form,
    }
    return render(request,'dashboard/analysis.html', context)

@login_required
def correction(request):
    phase = "correction"
    items = Production.objects.raw('SELECT * FROM dashboard_production WHERE phase = %s',[phase])
    # items = Production.objects.all()
    if request.method == 'POST' :
        form = THTForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('correction')
    else:
        form = THTForm()

    context = {
        'items' : items,
        'form' : form,
    }
    return render(request,'dashboard/correction.html', context)

@login_required
def phases(request, option):
    context = {'option': option}
    return render(request, 'phases.html', context)

@login_required
def export_stock_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock.csv"'

    writer = csv.writer(response)
    writer.writerow(['Item Name', 'Stock In', 'Stock Out', 'Inventory', 'Available(%)', 'Units', 'Stock In Date', 'Last Edit', 'Duration(Days)'])

    stocks = Stock.objects.all()

    for stock in stocks:
        if stock.stock_in ==0:
            writer.writerow([stock.item_name, stock.stock_in, stock.stock_out, (stock.stock_in - stock.stock_out) , 0, stock.units, stock.stock_in_date,stock.stock_out_date, ((stock.stock_out_date - stock.stock_in_date).days)])
        else:
            writer.writerow([stock.item_name, stock.stock_in, stock.stock_out, (stock.stock_in - stock.stock_out) ,(((stock.stock_in - stock.stock_out)/stock.stock_in) * 100),stock.units, stock.stock_in_date, stock.stock_out_date, ((stock.stock_out_date - stock.stock_in_date).days)])

    return response

@login_required
def history(request,pk):
    item = Stock.objects.get(id=pk)
    history = StockHistory.objects.filter(item_name=item.item_name).order_by('-history_date')
    context = {
        'history' : history,
    }
    # return HttpResponse(history)
    # return HttpResponse(item.item_name)
    return render(request, 'dashboard/history.html', context)

@login_required
def display_firmware_updates(request):
    firmware_updates = FirmwareUpdate.objects.all()
    fields = Fields.objects.all()

    group_by = request.GET.get('group_by')
    
    # Define the firmware_update_data as an empty list
    firmware_update_data = []

    if group_by == 'editable':
        fields = Fields.objects.filter(edit=True)  # Filter fields with edit=True

    elif group_by == 'noneditable':
        fields = Fields.objects.filter(edit=False)  # Filter fields with edit=False

    else:
        fields = Fields.objects.all()


    #Forms
    if request.method == 'POST':
        newDevice = NewDevice(request.POST)
        fileForm = UploadFileForm(request.POST, request.FILES)
        fieldForm = NewField(request.POST)
        firmwareForm = NewFirmwareUpdate(request.POST)
        if fileForm.is_valid():
            firmware_version_ = request.POST['firmware_version']
            firmware_version_file_ = request.FILES['firmware_version_file']
            firwareFile = Firmware.objects.create(firmware_version=firmware_version_, firmware_version_file=firmware_version_file_)
            firwareFile.save()
            # print(request.FILES) 
            fileForm.save()
            return redirect('display_firmware_updates')
        
        if fieldForm.is_valid():
            fieldForm.save()
            return redirect('display_firmware_updates')
        
        if newDevice.is_valid():
            newDevice.save()
            return redirect('display_firmware_updates')
        
        if firmwareForm.is_valid():
            firmwareForm.save()
            return redirect('display_firmware_updates')
        
    else:
        fileForm = UploadFileForm()
        fieldForm = NewField()
        newDevice = NewDevice()
        firmwareForm = NewFirmwareUpdate()
        
    # Create a list to store the data for each entry
    firmware_update_data = []

    for firmware_update in firmware_updates:
        device_name = firmware_update.device_name.device_name
        channel_id = firmware_update.device_name.channel_id
        fileDownload = firmware_update.device_name.fileDownload
        firmware_version = firmware_update.firmware.firmware_version

        field_data = []

        # Filter only the fields with edit=True
        for field in fields:
            firmware_update_field = FirmwareUpdateField.objects.get(
                firmware_update=firmware_update, field=field)
            field_data.append({
                'field_name': field.field_name,
                'value': firmware_update_field.value
            })

        firmware_update_data.append({
            'device_name': device_name,
            'channel_id': channel_id,
            'fileDownload': fileDownload,
            'firmware_version': firmware_version,
            'fields': field_data,
        })

    context = {
        'firmware_update_data': firmware_update_data,
        'fields': fields,
        'fileForm': fileForm,
        'fieldForm': fieldForm,
        'newDevice': newDevice,
        'firmwareForm': firmwareForm,
    }

    return render(request, 'dashboard/firmware_update.html', context)



# @login_required
# def display_firmware_updates(request):
#     firmware_updates = FirmwareUpdate.objects.all()
#     fields = Fields.objects.all()

#     group_by = request.GET.get('group_by')
    
#     # Define the firmware_update_data as an empty list
#     firmware_update_data = []

#     if group_by == 'editable':
#         fields = Fields.objects.filter(edit=True)  # Filter fields with edit=True

#     elif group_by == 'noneditable':
#         fields = Fields.objects.filter(edit=False)  # Filter fields with edit=False

#     else:
#         fields = Fields.objects.all()


#     #Forms
#     if request.method == 'POST':
#         newDevice = NewDevice(request.POST)
#         fileForm = UploadFileForm(request.POST, request.FILES)
#         fieldForm = NewField(request.POST)
#         firmwareForm = NewFirmwareUpdate(request.POST)
#         if fileForm.is_valid():
#             fileForm.save()
#             return redirect('display_firmware_updates')
        
#         if fieldForm.is_valid():
#             fieldForm.save()
#             return redirect('display_firmware_updates')
        
#         if newDevice.is_valid():
#             newDevice.save()
#             return redirect('display_firmware_updates')
        
#         if firmwareForm.is_valid():
#             firmwareForm.save()
#             return redirect('display_firmware_updates')
        
#     else:
#         fileForm = UploadFileForm()
#         fieldForm = NewField()
#         newDevice = NewDevice()
#         firmwareForm = NewFirmwareUpdate()
        
#     # Create a list to store the data for each entry
#     firmware_update_data = []

#     for firmware_update in firmware_updates:
#         device_name = firmware_update.device_name.device_name
#         channel_id = firmware_update.device_name.channel_id
#         fileDownload = firmware_update.device_name.fileDownload
#         firmware_version = firmware_update.firmware.firmware_version

#         field_data = []

#         # Filter only the fields with edit=True
#         for field in fields:
#             firmware_update_field = FirmwareUpdateField.objects.get(
#                 firmware_update=firmware_update, field=field)
#             field_data.append({
#                 'field_name': field.field_name,
#                 'value': firmware_update_field.value
#             })

#         firmware_update_data.append({
#             'device_name': device_name,
#             'channel_id': channel_id,
#             'fileDownload': fileDownload,
#             'firmware_version': firmware_version,
#             'fields': field_data,
#         })

#     context = {
#         'firmware_update_data': firmware_update_data,
#         'fields': fields,
#         'fileForm': fileForm,
#         'fieldForm': fieldForm,
#         'newDevice': newDevice,
#         'firmwareForm': firmwareForm,
#     }

#     return render(request, 'dashboard/firmware_update.html', context)

