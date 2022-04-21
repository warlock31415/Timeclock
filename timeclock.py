#! /usr/bin/python3
from dash import Dash, dcc, html, Input, Output, State, dash_table
import plotly.express as px
import pandas as pd

from datetime import datetime

import csv

filename= "timesheet.csv"



app = Dash(__name__)

clock_state = 0
clk_in_prev = 0
clk_out_prev = 0
clk_in_time = datetime.now()


app.layout = html.Div([
    html.Div(id='Status',children='Clock Status'),
    html.Button('Clock in', id='clk-in', n_clicks=0),
    html.Button('Clock out', id='clk-out',n_clicks=0),
    dash_table.DataTable(
        id='table',
        columns=(
            [{'id': 'ClockIn', 'name': 'Clock In time'}]+
            [{'id': 'ClockOut', 'name': 'Clock Out time'}]+
            [{'id': 'TimeLeft', 'name': 'Time Done'}]
        ),
        data = pd.read_csv(filename).to_dict('records'),
        editable=False,
    ),
])


@app.callback(
    Output('Status', 'children'),
    Output('table','data'),
    Input('clk-in', 'n_clicks'),
    Input('clk-out','n_clicks'),
)
def update_output(clkIn_clicks,clkOut_clicks):
    global clk_in_prev,clk_out_prev

    df = pd.read_csv(filename)

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


    if clkIn_clicks - clk_in_prev > 0:
        clock_state = 1
        clk_in_prev = clkIn_clicks

        df2 = pd.DataFrame({"ClockIn":[dt_string],"ClockOut":['x'],"TimeLeft":['x']})
        df = pd.concat([df,df2],axis=0)
        df.to_csv(filename,index=False)


        return "Clocked In", df.to_dict('records')

    elif clkOut_clicks - clk_out_prev > 0:
        clock_state = 0
        clk_out_prev = clkOut_clicks

        df['ClockOut'] = df['ClockOut'].replace(['x'],dt_string)

        clk_out_time = datetime.now()
        timediff = clk_out_time - clk_in_time
        timediff_h = int(timediff.seconds/3600)
        timediff_mins = int(timediff.seconds/60)

        timediff_str = "{:2}h {:2}m"
        df['TimeLeft'] = df['TimeLeft'].replace(['x'],timediff_str.format(timediff_h,timediff_mins))
        df.to_csv(filename,index=False)

        return "Clocked out",df.to_dict('records')
    else:
        return "Clock Status",df.to_dict('records')
    


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True, port=8050)
