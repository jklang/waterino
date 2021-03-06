#!/usr/bin/env python3

import json
import requests
import serial
import time

from influxdb import InfluxDBClient

def get_serial_output(ser):
    v = ser.readline().decode()
    return v


def send_notification(config, message):
    # Make a request to the 46elks API
    response = requests.post(
        "https://api.46elks.com/a1/sms",
        auth=(config["sms_gateway_username"], config["sms_gateway_password"]),
        data={
            "from": "Waterino",
            "to": config["sms_gateway_destination_phone_number"],
            "message": message
        }
    )

    # Check that the request was succesful
    if response.status_code == 200:
        return True
    else:
        # Log error?
        return False


def write_to_db(client, measurement, value):
    json_body = [
        {
            "measurement": measurement,
            "fields": {
                measurement: value,
            }
        }
    ]
    client.write_points(json_body)


def write_annotation_to_db(client, name, text, title, tags):
    json_body = [
        {
            "measurement": name,
            "fields": {
                "title": title,
                "text": text,
                "tags": tags
            }
        }
    ]
    client.write_points(json_body)


def main():
    wl_notification_sent = False
    failure_notification_sent = False
    annotation = ""
    count = 0
    config_file = './conf/config.json'
    with open(config_file) as conf:
        config = json.load(conf)
    influx_host = 'localhost'
    influx_port = '8086'
    influx_dbname = 'db_grafana'
    db_client = InfluxDBClient(host=influx_host, port=influx_port, database=influx_dbname)
    ser = serial.Serial(config["serial_device_path"], 9600)

    while True:
        value = get_serial_output(ser).strip('\n').strip('\r')

        # Separate soil moisture (m) and water level(w) values into two vars:
        if 'm:' in value:
            moisture = float(value.split(':')[1])
        if 'w:' in value:
            water_level = float(value.split(':')[1])
        if 't:' in value:
            temperature = float(value.split(':')[1])
        if 'h:' in value:
            humidity = float(value.split(':')[1])
        if 'l:' in value:
            light = float(value.split(':')[1])
        if water_level <= 20:
            if not wl_notification_sent:
                send_notification(config, 'Water level at {}%! Refill the water tank.'.format(int(water_level)))
                wl_notification_sent = True
        if 'Watering' in value:
            annotation = value
            write_annotation_to_db(db_client, 'events', annotation, 'Watering', 'waterino')
        if 'FAILURE' in value:
            if not failure_notification_sent:
                send_notification(config, 'Something is wrong! Arduino needs hard reset')
                failure_notification_sent = True
        # Write graph data.
        if count == 10:
            write_to_db(db_client, 'soil_moisture', moisture)
            write_to_db(db_client, 'water_level', water_level)
            write_to_db(db_client, 'temperature', temperature)
            write_to_db(db_client, 'humidity', humidity)
            write_to_db(db_client, 'light', light)

            print(moisture)
            print(water_level)
            print(temperature)
            print(humidity)
            print(light)
            time.sleep(0.25)
            count = 0
        count += 1


if __name__ == "__main__":
    main()
