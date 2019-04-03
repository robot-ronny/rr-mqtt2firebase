#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import yaml
import firebase.firebase as f
import schedule
import time


def main():
    values = {}

    config_data = yaml.load(open("config.yaml", "r"), yaml.CLoader)

    config_firebase = config_data.get("firebase")
    config_connection = config_data.get("connection")

    firebase = f.FirebaseApplication(config_firebase["url"], None)

    def patch_to_firebase():
        print("\n=== Firebase patch ===")
        firebase.patch("sensors/ronny/", values)

    def on_connect(mqttc, obj, flags, rc):
        print("Connected")
        mqttc.subscribe("sensor/ronny/#", 0)

    def on_message(mqttc, obj, msg):
        str_payload = str(msg.payload, "utf-8")
        split_topic = msg.topic.split("/")
        quantitie = split_topic[2]

        print("Now came:\n  Topic: {0}\n  Payload: {1}\n".
              format(msg.topic, str_payload))

        values[quantitie] = str_payload

        print(values)

    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.connect(config_connection["host"], int(config_connection["port"]))
    mqttc.loop_start()

    schedule.every(config_firebase["reporting_frequency"]
                   ).seconds.do(patch_to_firebase)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
