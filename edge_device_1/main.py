#!/usr/bin/env python

import serial
import json
import time
import mariadb

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=10)


db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '1234',
    'database': 'bmpDB'
}


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
        print(temp, pressure)


if __name__ == '__main__':
    main()
