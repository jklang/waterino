#!/usr/bin/env python3

import json
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
import pandas as pd
import plotly.graph_objs as go

moisture_csv_file = './data/moisture.csv'
water_level_csv_file = './data/water_level.csv'

def update_graph(csv_file, title):
    headers = ['DateTime','Sensor']
    df = pd.read_csv(csv_file, names=headers)
    with open('./conf/config.json') as config_file:
        plotly_user_config = json.load(config_file)
        py.sign_in(plotly_user_config["plotly_username"], plotly_user_config["plotly_api_key"])
    trace = go.Scatter(x = df['DateTime'], y = df['Sensor'],
        name='JoakimTest')
    layout = go.Layout(title=title)
    fig = go.Figure(data=[trace], layout=layout)
    p = py.plot(fig, filename=title)
    return p

update_graph(moisture_csv_file, 'Soil Moisture Reading')
update_graph(water_level_csv_file, "Water Level Reading")
