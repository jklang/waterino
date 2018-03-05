#!/usr/bin/env python3

import json
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

moisture_csv_file = './data/moisture.csv'
water_level_csv_file = './data/water_level.csv'
annotations_csv_file = './data/annotations.csv'


def update_graph(csv_file, annotations_csv_file, title):
    headers = ['DateTime', 'Sensor']
    df = pd.read_csv(csv_file, names=headers)
    df_annotations = pd.read_csv(annotations_csv_file, names=headers)
    with open('./conf/config.json') as config_file:
        plotly_user_config = json.load(config_file)
        py.sign_in(plotly_user_config["plotly_username"], plotly_user_config["plotly_api_key"])
    trace1 = go.Scatter(x=df['DateTime'], y=df['Sensor'],
        name='JoakimTest')
    trace2 = go.Scatter(x = df_annotations['DateTime'], y = df_annotations['Sensor'],
        name='JoakimTest')
    layout = go.Layout(title=title)
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    p = py.plot(fig, filename=title)
    return p

update_graph(moisture_csv_file, annotations_csv_file, 'Soil Moisture Reading')
update_graph(water_level_csv_file, annotations_csv_file, "Water Level Reading")

