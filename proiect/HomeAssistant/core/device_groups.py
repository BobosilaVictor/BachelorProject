import paho.mqtt.client as mqtt
from queue import Queue
import json

from .models import ZigbeeGroups




class DeviceGroup(object):
    def __init__(self):
        try:
            self.groups = None
            self.BROKER_IP = "192.168.100.152"
            self.client = mqtt.Client("P4")

            self.client.on_message = self.on_message_group
            self.client.on_connect = self.on_connect_group

            self.client.connect(self.BROKER_IP, 1883, 60)
            self.client.loop_start()


        except Exception as e:
            print(e)

    def on_connect_group(self, client, userdata, flags, rc):
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe("zigbee2mqtt/bridge/groups")

    def on_message_group(self, client, userdata, message):
        # global messages
        q = Queue()
        # Get the payload and save it
        payload = str(message.payload.decode("utf-8"))
        # Save the payload so we can work with it
        q.put(payload)
        while not q.empty():
            message = q.get()
            self.groups = json.loads(message)
        self.load_models(self.groups)
        print(self.groups)

    def load_models(self, group_data):
        for group in group_data:
            model_data = ZigbeeGroups(
                group_id=group["id"],
                friendly_name=group["friendly_name"],
                members=group["members"]
            )
            model_data.save()

