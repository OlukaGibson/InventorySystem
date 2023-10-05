
import csv
import xlwt
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Stock, Casing, Production,StockHistory
from .forms import InventoryForm, EditForm, CasingForm, THTForm,  MyForm, TheForm, NewStockForm, DispenseForm, UploadFileForm
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
#            item = Production.objects.all()

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
#        'item' :item,
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
#            item = Production.objects.all()

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
#        'item' :item,
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
#            item = Production.objects.all()

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
#        'item' :item,
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
    # Fetch the data you need from your models
    devices = Device.objects.all()
    firmware_updates = FirmwareUpdate.objects.filter(device_name__in=devices)
    fields_data = FirmwareUpdateField.objects.filter(firmware_update__in=firmware_updates)

    # Create a list of dictionaries to hold device data along with associated fields
    device_data = []
    for device in devices:
        device_info = {
            'device_name': device.device_name,
            'channel_id': device.channel_id,
            'firmware_version': '',
        }
        fields = fields_data.filter(firmware_update__device_name=device)
        for field in fields:
            device_info[field.field.field_name] = field.value
        device_data.append(device_info)    

    # Filter out the fields you want to display in the template
    fields_to_display = [field_name for field_name in device_data[0].keys() if field_name not in ['device_name', 'channel_id', 'firmware_version']]

    context = {
        'device_data': device_data,
        'fields_to_display': fields_to_display,
    }

    return render(request, 'dashboard/this.html', context)


# @login_required
# def display_firmware_updates(request):
#     fields = Fields.objects.all()
#     firmware_update_fields = FirmwareUpdateField.objects.select_related('firmware_update__device_name', 
#                                                                         'firmware_update__firmware', 'field'
#                                                                         )

    
    
#     context = {
#         'fields': fields,
#         'firmware_update_fields': firmware_update_fields,
#     }
    
#     return render(request, 'dashboard/firmware_update.html', context)


# @login_required
# def display_firmware_updates(request):
#     firmware_updates = FirmwareUpdate.objects.select_related('device_name','firmware').all().order_by('-device_name')

#     group_by = request.GET.get('group_by')

#     if group_by == 'firmware_version':
#         firmware_updates = firmware_updates.order_by('firmware__firmware_version') 
#     elif group_by == 'fileDownload':
#         firmware_updates = firmware_updates.order_by('fileDownload')
#     elif group_by == 'spvValue':
#         firmware_updates = firmware_updates.order_by('spvValue')
#     elif group_by == 'syncState':
#         firmware_updates = firmware_updates.order_by('syncState')
#     elif group_by == 'confrigDownload':
#         firmware_updates = firmware_updates.order_by('confrigDownload')

#     if request.method == 'POST':
#         fileForm = UploadFileForm(request.POST, request.FILES)
#         if fileForm.is_valid():
#             fileForm.save()
#             return redirect('display_firmware_updates')
        
#         selected_ids = request.POST.getlist('selected_firmware_updates')
#         edit_feature = request.POST.get('edit_feature')
#         new_value = request.POST.get('new_value')

#         # Update the selected entries based on the chosen feature
#         if edit_feature == 'firmware_version':
#             FirmwareUpdate.objects.filter(pk__in=selected_ids).update(firmware_version=new_value)
#         elif edit_feature == 'fileDownload':
#             FirmwareUpdate.objects.filter(pk__in=selected_ids).update(fileDownload=new_value)
#         elif edit_feature == 'spvValue':
#             FirmwareUpdate.objects.filter(pk__in=selected_ids).update(spvValue=new_value)
#         elif edit_feature == 'syncState':
#             FirmwareUpdate.objects.filter(pk__in=selected_ids).update(syncState=new_value)
#         elif edit_feature == 'confrigDownload':
#             FirmwareUpdate.objects.filter(pk__in=selected_ids).update(confrigDownload=new_value)
        

#     context = {
#         'firmware_updates': firmware_updates,
#         'group_by': group_by,
#         'fileForm': UploadFileForm(),
#     }

#     return render(request, 'dashboard/firmware_update.html', context)

