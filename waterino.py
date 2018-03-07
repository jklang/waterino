#!/usr/bin/env python3

import datetime
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


def write_to_csv(filename, moisture):
    with open(filename, 'a') as datafile:
        datafile.write('{}, {}\n'.format(datetime.datetime.now(), moisture))


def write_to_db(client, measurement, value, host):
    json_body = [
        {
            "tags": {
                "host": host,
            },
            "measurement": measurement,
            "fields": {
                "soil_moisture_value": value,
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
    moisture = 0
    water_level = 0
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
        moisture_stats_file = './data/moisture.csv'
        water_level_stats_file = './data/water_level.csv'
        annotations_file = './data/annotations.csv'
        value = get_serial_output(ser).strip('\n').strip('\r')

        # Separate soil moisture (m) and water level(w) values into two vars:
        if 'm:' in value:
            moisture = float(value.split(':')[1])
        if 'w:' in value:
            water_level = float(value.split(':')[1])
    #   if water_level <= 20:
    #        send_notification(config, 'Water level at {} Fill the water tank.'.format(water_level))
        if 'Watering' in value:
            annotation = value
            write_to_csv(annotations_file, annotation)
            write_annotation_to_db(db_client, 'events', annotation, 'Watering', 'waterino')
            send_notification(config, value)
        # Write graph data.
        if count == 10:
            write_to_db(db_client, 'soilmoisture', moisture, 'pi')
            write_to_db(db_client, 'waterlevel', water_level, 'pi')
            print(moisture)
            time.sleep(0.25)
            count = 0
        count += 1


if __name__ == "__main__":
    main()
