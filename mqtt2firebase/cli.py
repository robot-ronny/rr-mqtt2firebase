#!/usr/bin/python
# -*- coding: utf-8 -*-

import click
import paho.mqtt.client as mqtt
import firebase.firebase as f
import schedule
import time


@click.command()
@click.option("--firebase", "-f", help="Firebase url", required=True)
@click.option("--host", "-h", help="MQTT broker host", required=False, default="localhost")
@click.option("--port", "-p", help="MQTT broker port", required=False, default=1883)
@click.option("--delay", "-d", help="Delay between reporting data to firebase", required=False, default=10)
def main(firebase, host, port, delay):
    values = {}

    firebase = f.FirebaseApplication(firebase, None)

    def patch_to_firebase():
        print("\n=== Firebase patch ===\n")
        firebase.patch("sensors/ronny/", values)

    def on_connect(mqttc, obj, flags, rc):
        print("Connected")
        mqttc.subscribe("node/#", 0)

    def on_message(mqttc, obj, msg):
        str_payload = str(msg.payload, "utf-8")
        split_topic = msg.topic.split("/")
        quantitie = split_topic[4]

        print("Now came:\n  Topic: {0}\n  Payload: {1}\n".
              format(msg.topic, str_payload))

        values[quantitie] = str_payload

        print(values)

    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.connect(host, port)
    mqttc.loop_start()

    schedule.every(delay).seconds.do(patch_to_firebase)

    while True:
        schedule.run_pending()
        time.sleep(1)
