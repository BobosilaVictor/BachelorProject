from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse
from .device_state import DeviceState
from .device_setter import DeviceSetter
from .device_groups import DeviceGroup
from .models import ZigbeeDevice, ZigbeeExposes, ZigbeeGroups


def index(request):
    context = {
        'devices': ZigbeeDevice.objects.all(),
        'state': DeviceState().status
    }
    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))

def render_items(request, item_name):
    item = get_object_or_404(ZigbeeDevice, friendly_name=item_name)
    print(list(request.POST))
    if request.method == 'POST':
        if request.POST.get('rename', None) is not None:
            message = request.POST.get('rename', None)
            DeviceSetter().publishRename(item_name, message)
        elif request.POST.get(list(request.POST)[1], None) is not None:
            message = request.POST.get(list(request.POST)[1], None)
            DeviceSetter().publishCustom(item_name, list(request.POST)[1], message)

    return render(request, 'device.html', {'device': item, 'exposes': ZigbeeExposes.objects.all()})

def groups(request):
    DeviceGroup().groups
    context = {
        'devices': ZigbeeDevice.objects.all(),
        'groups':  ZigbeeGroups.objects.all()
    }
    if request.method == 'POST':
        if request.POST.get('add', None) is not None:
            message = request.POST.get('add', None)
            DeviceSetter().publishCustomNewGroup('add', message)
    html_template = loader.get_template('groups.html')
    return HttpResponse(html_template.render(context, request))

def render_groups(request, group_name):
    item = get_object_or_404(ZigbeeGroups, friendly_name=group_name)
    if request.method == 'POST':
        if request.POST.get(list(request.POST)[1], None) is not None:
            message = request.POST.get(list(request.POST)[1], None)
            DeviceSetter().publishCustomGroup(list(request.POST)[1].split("/")[0], list(request.POST)[1].split("/")[1], list(request.POST)[1].split("/")[2])

    return render(request, 'group.html', {'group': item, 'devices': ZigbeeDevice.objects.all()})