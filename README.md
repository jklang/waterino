# waterino
Plant watering system controlled by Arduino and monitored using RPi and python

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

