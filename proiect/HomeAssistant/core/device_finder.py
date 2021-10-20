import threading

import paho.mqtt.client as mqtt

from queue import Queue
import json


class DeviceFinder(object):
    def __init__(self):
        try:
            self.data = {}
            self.BROKER_IP = "192.168.100.152"
            self.client = mqtt.Client("P1")
            self.client.on_connect = self.on_connect_finder
            self.client.on_message = self.on_message_finder
            self.client.connect(self.BROKER_IP, 1883, 60)
            self.client.loop_forever()


        except Exception as e:
            print(e)

    def on_connect_finder(self, client, userdata, flags, rc):
        self.client.subscribe("zigbee2mqtt/bridge/devices")
        print("connected! finder")

    def on_message_finder(self, client, userdata, message):
        # global messages
        # Start creating the json format with {devices:[]}
        q = Queue()
        first = "{\"devices\":"
        last = "}"
        # Get the payload and save it
        payload = str(message.payload.decode("utf-8"))
        # Build the payload to have a json format so its easier to access
        payload = first + payload + last
        # Save the payload so we can work with it
        q.put(payload)

        while not q.empty():
            message = q.get()
            self.data = json.loads(message)

        print(self.data)
        self.data = self.humanize_device_data(self.data)
        self.client.disconnect()




    def get_devices_from_data(self, raw_data):
        data = []
        device_list = raw_data['devices']
        for i in range(0, len(device_list)):
            data.append(device_list[i])
        return data

    def humanize_device_data(self, data):
        data_list = self.get_devices_from_data(data)
        output_data = []
        for device in range(0, len(data_list)):
            if data_list[device]['definition'] != None:
                output_data.append(data_list[device])

        return output_data

