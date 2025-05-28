#!/usr/bin/env python

import serial
import json
import time
import mariadb
import os
import paho.mqtt.client as mqtt


ser = serial.Serial('/dev/ttyACM0', 9600, timeout=10)


db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '1234',
    'database': 'iotdb'
}


def on_connect(client, userdata, flags, rc):
    client.subscribe("v1/devices/me/attributes")
    print("Connected with result code", rc)


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    if data.get('led'):
        ser.write("{\"led\": true}\n".encode('utf-8'))
    else:
        ser.write("{\"led\": false}\n".encode('utf-8'))


THING_TOKEN = os.getenv("A_THING")
if not THING_TOKEN:
    print(THING_TOKEN)
    print("Failed to get token")
    exit(1)

client = mqtt.Client()
client.username_pw_set(THING_TOKEN)
client.on_connect = on_connect
client.on_message = on_message
client.connect('mqtt.thingsboard.cloud', 1883, 60)
client.loop_start()


try:
    conn = mariadb.connect(**db_config)
    cursor = conn.cursor()
except Exception as e:
    print(e)  # Failed to connect to database
    exit(1)


def insert_data(temp, pressure):
    if temp < -998 or pressure < -998:  # If data is read wrong
        return

    cursor.execute(
        "INSERT INTO Records (temp, pressure) VALUES (?,?)",
        (temp, pressure))
    conn.commit()


def read_serial():
    try:
        line = ser.readline().decode('utf-8').strip()
        try:
            data = json.loads(line)
            temp = data['temp']
            pressure = data['pressure']
            return temp, pressure
        except Exception as e:
            print(f"\x1b[31merror={e} data={line}\x1b[0m")
            return -999, -999
    except Exception as e:
        print(f"\x1b[31merror={e}\x1b[0m")
        return -999, -999


def main():
    while True:
        time.sleep(1)
        temp, pressure = read_serial()
        insert_data(temp, pressure)
        client.publish('v1/devices/me/telemetry',
                       f"{{temp: {temp}, pressure: {pressure}}}")
        print(temp, pressure)


if __name__ == '__main__':
    main()
