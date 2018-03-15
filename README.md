# waterino
Plant watering system controlled by Arduino and monitored using RPi, python, Influxdb and Grafana.

This project depends on a Influxdb database named "db_grafana" running without auth on localhost.

There's support for soil moisture, water tank level, air humidity, temperature and light. If you just want the soil moisture and tank level sensors you can go ahead and skip the other ones. If you don't want fancy graphs with data from your sensors you can ignore all the Reaspberry pi stuff and just get the Arduino

## Installation instructions

### Hardware

You will need:

* An Arduino board
* LCD display 16x2 (https://www.kjell.com/se/sortiment/el-verktyg/elektronik/optokomponenter/led-lcd-displayer/luxorparts-lcd-display-2x16-p90215?gclid=CjwKCAjws6jVBRBZEiwAkIfZ2pYGCjAQY531Kf2TBXfbQHMwFdJyUXTJpZKnRxMThNqEpCbQ5l7XsRoCZsQQAvD_BwE)
* Capacitive Soil Moisture Sensor (https://www.tindie.com/products/pinotech/soilwatch-10-soil-moisture-sensor/)
* Ultrasonic distance sensor (HC-SR04)
* 12V DC Water pump (AD20P or something similair)
* Humidity and temperature sensor (DHT21 or DHT22)
* Photo resistor
* 2x 10K resistors
* Cabling, solder iron and heat-shrink tubing
* A transparent case to fit everything. (Like this one: https://www.clasohlson.com/se/Vattent%C3%A4t-l%C3%A5da-/31-8543)

* Raspberry Pi to run the graphing stuff. It will be connected and be recieving data via the USB port so it should probably be mounted in the same case as the Arduino.


### Install the Ardiuino libraries in your Arduino IDE
```
...
```
### Upload the waterino.ino code to the arduino

### If you don't have a Raspberry Pi and don't want fancy graphs you can stop here ###
#### Install InfluxDB
```
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt-get update && sudo apt-get install influxdb
sudo systemctl start influxdb
influx -execute 'CREATE DATABASE db_grafana'
```

#### Install grafana
```
https://github.com/fg2it/grafana-on-raspberry/wiki
```

#### Install Python dependencies:
```
pip3 install plotly pyserial numpy pandas
```
#### Setup the config file:
```
cp /home/pi/waterino/conf/config.json.example /home/pi/waterino/conf/config.json
Edit the file with your 46elks.com info. Also identify your Arduino serial device name and add that as well.
```

#### Create a systemd service using the unit file provided.
```
cp /home/pi/waterino/conf/systemd/waterino.service /etc/systemd/system/waterino.service
```
#### Enable and start waterino
```
systemctl enable waterino
systemctl start waterino
```

#### Go to http://localhost:3000 and setup the grafana instance
