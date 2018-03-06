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
Edit the file with your plotly and 46elks.com info. Also identify your Arduino serial device name and add that as well.
```
### Install crontab file in /etc/cron.d. This will update the plotly graphs every 3 minutes.
```
cp /home/pi/waterino/conf/cron.d/update_plotly_graphs /etc/cron.d/update_plotly_graphs
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
### Make sure your graphs show up in Plotly
https://plot.ly/organize/YOURUSERNAME:home

