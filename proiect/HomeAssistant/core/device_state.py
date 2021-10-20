import paho.mqtt.client as mqtt
from queue import Queue
import json


from .models import ZigbeeDevice,ZigbeeExposes
from .device_finder import DeviceFinder


class DeviceState(object):
    def __init__(self):
        try:
            self.data = DeviceFinder().data
            self.status = None
            self.BROKER_IP = "192.168.100.152"
            self.client = mqtt.Client("P2")

            self.client.on_message = self.on_message_state
            self.client.on_connect = self.on_connect_state

            self.client.connect(self.BROKER_IP, 1883, 60)
            self.client.loop_start()


        except Exception as e:
            print(e)

    def on_connect_state(self, client, userdata, flags, rc):
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.subscribe_to_device_status(self.data)


    def on_message_state(self, client, userdata, message):
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
        self.load_models(self.data)
        print(self.status)



    def subscribe_to_device_status(self, data):
        for device in data:
            device_name = str(device['friendly_name'])
            self.client.subscribe(f"zigbee2mqtt/{device_name}")

    def append_new_states_to_data(self, status, data):
        for device in data:
            device_name = str(device['friendly_name'])
            if device_name in status:
                device['status'] = status[device_name]

    def load_models(self, data):
        for i in data:
            if 'status' in i :
                model_data = ZigbeeDevice(
                    ieee_address=i['ieee_address'],
                    type=i['type'],
                    supported=i['supported'],
                    friendly_name=i['friendly_name'],
                    model_name=i['definition']['model'],
                    vendor=i['definition']['vendor'],
                    power_source=i['power_source'],
                )
                model_data.save()
                model_data_exposes = ZigbeeExposes(
                    device=model_data,
                    exposes=i['definition']['exposes'],
                    state=i['status']
                )
                model_data_exposes.save()

