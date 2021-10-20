from django.db import models


class ZigbeeDevice(models.Model):
    ieee_address = models.CharField(primary_key=True, max_length=30)
    type = models.CharField(max_length=30)
    supported = models.BooleanField()
    friendly_name = models.CharField(max_length=30)
    model_name = models.CharField(max_length=30)
    vendor = models.CharField(max_length=30)
    power_source = models.CharField(max_length=30)


class ZigbeeExposes(models.Model):
    device = models.OneToOneField(ZigbeeDevice, primary_key=True, blank=True, on_delete=models.CASCADE)
    exposes = models.JSONField()
    state = models.JSONField()


class ZigbeeGroups(models.Model):
    group_id = models.IntegerField(primary_key=True)
    friendly_name = models.CharField(max_length=50)
    members = models.JSONField()
