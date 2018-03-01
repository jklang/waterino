#!/usr/bin/env python
import serial
import time
import plotly.plotly as py
import plotly.graph_objs as go
import requests
import json
import datetime

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
    v = ser.readline()
    return v

def send_notification(config, message):
    # Make a request to the 46elks API
    response = requests.post(
        "https://api.46elks.com/a1/sms",
        auth = (config["sms_gateway_username"], config["sms_gateway_password"]),
        data = {
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
    ser = serial.Serial('/dev/tty.wchusbserial1410', 9600)
    config_file = '/Users/joakim/waterino/waterino/conf/config.json'

    with open(config_file) as conf:
        config = json.load(conf)

    p = Plotly(config)
    while True:
        moisture_stats_file = './data/moisture.csv'
        water_level_stats_file = './data/water_level.csv'
        value = get_serial_output(ser).strip('\n').strip('\r')
        # Separate soil moisture (m) and water level(w) values into two seperate variables:
        if 'm:' in value:
            moisture = value.split(':')[1]
        if 'w:' in value:
            water_level = value.split(':')[1]
    #   if water_level <= 20:
    #        send_notification(config, 'Water level at {} Fill the water tank.'.format(water_level))
        #if 'Watering' in value:
        #    send_notification(config, value)
	# Write graph data:
        p.write_to_streaming_graph(config, datetime.datetime.now(), moisture)
	write_to_csv(moisture_stats_file, moisture)
	write_to_csv(water_level_stats_file, water_level)
        print(moisture)

if __name__ == "__main__":
    main()