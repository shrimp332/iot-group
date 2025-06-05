import paho.mqtt.client as mqtt
import serial
import time
import json

BROKER = "54.159.242.170"
PORT = 1883
USERNAME = "QuangLamNguyen"
TOPIC = "v1/devices/me/telemetry"
TOPIC_ATTRIBUTES = "v1/devices/me/attributes"

SERIAL_PORT = "/dev/ttyS0"
BAUD_RATE = 9600

def on_connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))
    client.subscribe(TOPIC_ATTRIBUTES)
    
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Raw message received on topic {msg.topic}: {payload}")
    try:
        data = json.loads(payload)
        if 'message' in data:
            warning_flag = data['message']
            print(f"Warning flag received: {warning_flag}")
            ser.write((warning_flag + '\n').encode())
        else:
            print("No 'message' key found in the message.")
    except json.JSONDecodeError:
        print("Failed to decode JSON message.")

client = mqtt.Client()
client.username_pw_set(USERNAME)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_start()


ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode().strip()
            if line:
                payload = '{' + line + '}'
                client.publish(TOPIC, payload)
except KeyboardInterrupt:
    print("Program interrupted by user.")
    
finally:
    ser.close()
    client.loop_stop()
    client.disconnect()