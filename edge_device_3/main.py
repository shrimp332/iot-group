import paho.mqtt.client as mqtt
import serial
import time
import json

BROKER = "54.159.242.170" #Ipv4 of the Thingsboard Cloud
PORT = 1883
USERNAME = "CongQuyenPham"
TOPIC_TELEMETRY = "v1/devices/me/telemetry"
TOPIC_ATTRIBUTES = "v1/devices/me/attributes"

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

def on_connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))
    client.subscribe(TOPIC_ATTRIBUTES)
    
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received attribute update on topic {msg.topic}: {payload}")
    try:
        data = json.loads(payload)
        if 'servo_angle' in data:
            angle = data['servo_angle']
            print(f"Command to set servo angle: {angle}")
            #Send command to Arduino via serial, add newline to mark end
            ser.write(f"ANGLE: {angle}\n".encode())
        else:
            print("No 'servo_angle' key found in the message.")
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
                print(f"Received from Arduino: {line}")
                #Convert "RAIN" or "NO_RAIN" to JSON telemetry
                if line == "RAIN":
                    payload = json.dumps({"rain": True})
                elif line == "NO_RAIN":
                    payload = json.dumps({"rain": False})
                else:
                    #Ignore unexpected messages
                    continue

                print(f"Publishing telemetry: {payload}")
                client.publish(TOPIC_TELEMETRY, payload)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Program interrupted by user.")
    
finally:
    ser.close()
    client.loop_stop()
    client.disconnect()