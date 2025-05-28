#!/usr/bin/env python

import serial
import json
import time
import mariadb
import paho.mqtt.client as mqtt

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=10)

db_config = {
    'host': '127.0.0.1',
    'user': 'admin',
    'password': 'admin',
    'database': 'groupdb'
}

# MQTT
def on_connect(client, userdata, flags, rc):
    client.subscribe("v1/devices/me/attributes")
    print("Connected with result code", rc)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        if 'buzzer' in data:
            command = json.dumps({"buzzer": data['buzzer']}) + '\n'
            ser.write(command.encode('utf-8'))
    except Exception as e:
        print(f"Command error: {e}")

# Get ThingsBoard token
THING_TOKEN = "DEVICE_ID"
if not THING_TOKEN:
    print("Error. Please check THING_TOKEN.")
    exit(1)

# Setup MQTT client
client = mqtt.Client()
client.username_pw_set(THING_TOKEN)
client.on_connect = on_connect
client.on_message = on_message
client.connect('mqtt.thingsboard.cloud', 1883, 60)
client.loop_start()

# Database connection
try:
    conn = mariadb.connect(**db_config)
    cursor = conn.cursor()
except Exception as e:
    print(f"Database connection failed: {e}")
    exit(1)

def insert_data(ldr_value):
    if ldr_value < 0:  # Skip invalid readings
        return
    try:
        cursor.execute(
            "INSERT INTO LdrRecords (ldr_value) VALUES (?)",
            (ldr_value,)
        )
        conn.commit()
    except Exception as e:
        print(f"Database insert error: {e}")

def read_serial():
    try:
        line = ser.readline().decode('utf-8').strip()
        try:
            data = json.loads(line)
            return data.get('ldr', -999)
        except json.JSONDecodeError:
            print(f"Invalid JSON: {line}")
            return -999
    except Exception as e:
        print(f"Serial read error: {e}")
        return -999

def main():
    while True:
        time.sleep(0.1)
        ldr_value = read_serial()
        if ldr_value >= 0:
            insert_data(ldr_value)
            client.publish('v1/devices/me/telemetry', json.dumps({"ldr": ldr_value}))
            print(f"LDR: {ldr_value}")

if __name__ == '__main__':
    main()