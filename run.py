#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import yaml
import firebase.firebase as f


def main():
    config_data = yaml.load(open("config.yaml", "r"), yaml.CLoader)

    config_firebase = config_data.get("firebase")
    config_connection = config_data.get("connection")

    firebase = f.FirebaseApplication(config_firebase["url"], None)

    def on_connect(mqttc, obj, flags, rc):
        print("Connected")
        mqttc.subscribe("node/#", 0)

    def on_message(mqttc, obj, msg):
        str_payload = str(msg.payload, "utf-8")
        split_topic = msg.topic.split("/")
        print("Topic: {0}\nPayload: {1}\n".
              format(msg.topic, str_payload))
        firebase.patch('sensors/{0}'.format(split_topic[1]),
                       {split_topic[4]: str_payload})

    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.connect(config_connection["host"], int(config_connection["port"]))

    mqttc.loop_forever()


if __name__ == "__main__":
    main()
