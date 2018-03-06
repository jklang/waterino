#!/usr/bin/env python3

import datetime
import json
import requests
import serial
import time

import plotly.plotly as py


class Plotly:
    def __init__(self, config):
        py.sign_in(config['plotly_username'], config['plotly_api_key'])
        py.plot([
            {
                'x': [], 'y': [], 'type': 'scatter',
                'stream': {
                    'token': config['plotly_streaming_tokens'][0],
                    'maxpoints': 20000
                }
            }], filename='Current soil moisture value')

    def write_to_streaming_graph(self, config, datetime, moisture):
        stream = py.Stream(config['plotly_streaming_tokens'][0])
        stream.open()
        stream.write({'x': datetime, 'y': moisture})


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


def main():
    moisture = 0
    water_level = 0
    annotation = ""
    count = 0
    config_file = './conf/config.json'
    with open(config_file) as conf:
        config = json.load(conf)

    ser = serial.Serial(config["serial_device_path"], 9600)
    p = Plotly(config)
    while True:
        moisture_stats_file = './data/moisture.csv'
        water_level_stats_file = './data/water_level.csv'
        annotations_file = './data/annotations.csv'
        value = get_serial_output(ser).strip('\n').strip('\r')
        # Separate soil moisture (m) and water level(w) values into two vars:
        if 'm:' in value:
            moisture = value.split(':')[1]
        if 'w:' in value:
            water_level = value.split(':')[1]
    #   if water_level <= 20:
    #        send_notification(config, 'Water level at {} Fill the water tank.'.format(water_level))
        if 'Watering' in value:
            annotation = value
            write_to_csv(annotations_file, annotation)
            send_notification(config, value)
    # Write graph data. Downsample sensor data to once every 30 iterations:
        if count == 30:
            write_to_csv(moisture_stats_file, moisture)
            write_to_csv(water_level_stats_file, water_level)
            print(moisture)
            time.sleep(0.25)
            count = 0
        count += 1


if __name__ == "__main__":
    main()
