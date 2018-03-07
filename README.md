# waterino
Plant watering system controlled by Arduino and monitored using RPi and python

This project depends on a Influxdb database named "db_grafana" running without auth on localhost.

## Install InfluxDB
```
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt-get update && sudo apt-get install influxdb
sudo systemctl start influxdb
influx -execute 'CREATE DATABASE db_grafana'
```

## Install grafana
```
https://github.com/fg2it/grafana-on-raspberry/wiki
```
## Installation 
### Install Requirements:
```
pip3 install plotly pyserial numpy pandas
```
### Setup the config file:
```
cp /home/pi/waterino/conf/config.json.example /home/pi/waterino/conf/config.json
Edit the file with your 46elks.com info. Also identify your Arduino serial device name and add that as well.
```

### Create a systemd service using the unit file provided.
```
cp /home/pi/waterino/conf/systemd/waterino.service /etc/systemd/system/waterino.service
```
### Enable and start waterino
```
systemctl enable waterino
systemctl start waterino
```

### Go to http://localhost:3000 and setup the grafana instance