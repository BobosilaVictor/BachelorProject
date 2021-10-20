from django.contrib import admin

from .models import ZigbeeDevice, ZigbeeExposes, ZigbeeGroups


admin.site.register(ZigbeeDevice)
admin.site.register(ZigbeeExposes)
admin.site.register(ZigbeeGroups)
# Register your models here.
