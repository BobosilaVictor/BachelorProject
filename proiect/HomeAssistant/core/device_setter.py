import paho.mqtt.client as mqtt
from queue import Queue
import json
import threading

from .models import ZigbeeDevice
from .device_finder import DeviceFinder

#from .models import ZigbeeDevice
class DeviceSetter(object):
    def __init__(self):
        try:
            self.data = DeviceFinder().data
            self.status = None
            self.BROKER_IP = "192.168.100.152"
            self.client = mqtt.Client("P3")

            self.client.connect(self.BROKER_IP, 1883, 60)
            self.client.loop_start()



        except Exception as e:
            print(e)


    def on_publish_setter(self,client, userdata, mid):
        print("Message has been published")
        self.client.disconnect()

    def publishCustom(self, device, topic_raw, message):
        topic = topic_raw.split("/")[1]
        print(topic)
        print(message)
        self.client.publish(f"zigbee2mqtt/{device}/set/{topic}", message)

    def publishCustomGroup(self, topic, group, device):
        message_sent = {
            'group': group,
            'device': device
        }
        #MQTT only acknowledges strings, ints, floats, or bytes as messages, so we have to convert the dictionary
        #to a string
        message_sent_string = json.dumps(message_sent)
        self.client.publish(f"zigbee2mqtt/bridge/request/group/members/{topic}", message_sent_string)

    def publishCustomNewGroup(self, topic_raw, message):
        message_sent = {
            'friendly_name': message,
        }
        #MQTT only acknowledges strings, ints, floats, or bytes as messages, so we have to convert the dictionary
        #to a string
        message_sent_string = json.dumps(message_sent)
        self.client.publish(f"zigbee2mqtt/bridge/request/group/{topic_raw}", message_sent_string)

    def publishRename(self, device_to_change, message):
        message_sent = {
            'from': str(device_to_change),
            'to': message
        }
        #MQTT only acknowledges strings, ints, floats, or bytes as messages, so we have to convert the dictionary
        #to a string
        message_sent_string = json.dumps(message_sent)
        self.client.publish("zigbee2mqtt/bridge/request/device/rename", message_sent_string)

    def publishGroupSet(self, topic_raw, message):
        topic = topic_raw.split("/")[0]
        group_name = topic_raw.split("/")[1]
        message_sent = {
            'state': message,
        }
        # MQTT only acknowledges strings, ints, floats, or bytes as messages, so we have to convert the dictionary
        # to a string
        message_sent_string = json.dumps(message_sent)
        self.client.publish(f"zigbee2mqtt/{group_name}/{topic}", message_sent_string)





