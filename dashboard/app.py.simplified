"""
Energy Policy Dashboard - Andrew Baker
"""

import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime

# Initialize the app
app = dash.Dash(__name__)

# Simple layout
app.layout = html.Div([
    html.H1("Energy Policy Dashboard", 
            style={'textAlign': 'center', 'color': '#2E86AB'}),
    
    html.Div([
        html.Div([
            html.H3("Fuel Excise Revenue"),
            html.H2("$15.7B"),
            html.P("Annual 2023-24")
        ], style={'width': '23%', 'display': 'inline-block', 
                  'textAlign': 'center', 'padding': '20px'}),
        
        html.Div([
            html.H3("Economic Multiplier"),
            html.H2("4.35x"),
            html.P("Per subsidy dollar")
        ], style={'width': '23%', 'display': 'inline-block', 
                  'textAlign': 'center', 'padding': '20px'}),
        
        html.Div([
            html.H3("Jobs Created"),
            html.H2("100,000"),
            html.P("By 2030")
        ], style={'width': '23%', 'display': 'inline-block', 
                  'textAlign': 'center', 'padding': '20px'}),
        
        html.Div([
            html.H3("Energy Reduction"),
            html.H2("35-45%"),
            html.P("Potential")
        ], style={'width': '23%', 'display': 'inline-block', 
                  'textAlign': 'center', 'padding': '20px'}),
    ]),
    
    html.Footer([
        html.Hr(),
        html.P("Andrew Baker - March 2026", 
               style={'textAlign': 'center'})
    ])
    
], style={'fontFamily': 'Arial', 'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
