import paho.mqtt.client as mqtt
from queue import Queue
import json

from .device_finder import DeviceFinder


class DeviceState(object):
    def __init__(self):
        try:
            self.data = DeviceFinder().data
            self.status = None
            self.BROKER_IP = "192.168.100.152"
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.connect(self.BROKER_IP, 1883, 60)

            self.client.loop_forever()
        except Exception as e:
            print(e)

    def on_connect(self, client, userdata, flags, rc):
        print("connected!")
        self.subscribe_to_device_status(self.data)

    def on_message(self, client, userdata, message):
        # global messages
        # Start creating the json format with {devices:[]}
        q = Queue()
        name = message.topic.split("/")[1]
        first = "{"
        topic = f"\"{name}\":"
        last = "}"
        # Get the payload and save it
        payload = str(message.payload.decode("utf-8"))
        # Build the payload to have a json format so its easier to access
        payload = first + topic + payload + last

        # Save the payload so we can work with it
        q.put(payload)
        while not q.empty():
            message = q.get()
            self.status = json.loads(message)
        self.append_new_states_to_data(self.status, self.data)
        self.client.disconnect()


    def subscribe_to_device_status(self, data):
        for device in data:
            device_name = str(device['friendly_name'])
            self.client.subscribe(f"zigbee2mqtt/{device_name}")

    def append_new_states_to_data(self, status, data):
        for device in data:
            device_name = str(device['friendly_name'])
            if device_name in status:
                device['status'] = status[device_name]

