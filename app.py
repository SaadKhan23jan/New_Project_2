from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime as dt
import pandas as pd
import yfinance as yf

css_sheet = [dbc.themes.SPACELAB]
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
app = Dash(__name__, external_stylesheets=css_sheet)
server = app.server

app.layout = html.Div([
    dbc.Button("Contact Me!", href='https://www.linkedin.com/in/saad-khan-167704163/', external_link=True),
    html.H1('Cryptocurrency Live updates', style={'textAlign': 'center'}),
    html.Div([
        html.Label('Select Cryptocurrency Pair'),
        dcc.Dropdown(id='cryptocurrency-pair', options=sorted(['ADA-EUR', 'BTC-USD', 'ETH-USD', 'ALGO-USD', 'BAT-USD',
                                                               'CAKE-USD', 'CRV-USD', 'DENT-USD', 'DOGE-USD', 'LUNA-USD',
                                                               'CRV-USD', 'FTM-USD', 'IRIS-USD', 'MANA-USD', 'NEAR-USD',
                                                               'OCEAN-USD', 'ROSE-USD', 'SLP-USD', 'SOL-USD', ]),
                     style={'width':'50%'},
                     value='BTC-USD'),

        html.Label('Select Time Frame'),
        html.Br(),
        dcc.Dropdown(id='time-frame', options=[{'label':'10 Year', 'value': '10y'},
                                               {'label':'1 Year', 'value': '1y'},
                                               {'label':'3 months', 'value': '3mo'},
                                               {'label':'1 months', 'value': '1mo'},
                                               {'label':'1 day', 'value': '1d'},
                                               {'label':'4 hours', 'value': '4h'}],
                     value='3mo', style={'width':'50%'}),
    ]),
    html.Div(
        dcc.Graph(id='my-graph-candlestick')
    ),

    html.Div(
        dcc.Graph(id='my-graph-line')
    )
], style={'backgroundColor': 'Lightgreen'})


@app.callback([Output('my-graph-candlestick', 'figure'),
               Output('my-graph-line', 'figure')],
              [Input('cryptocurrency-pair', 'value'),
               Input('time-frame', 'value')])
def update_graph(crypto, time_frame):
    if time_frame in ['10y', '1y']:
        interval = '1d'
    elif time_frame in ['6mo']:
        interval = '4h'
    elif time_frame in ['3mo']:
        interval = '1h'
    else:
        interval = '15m'

    df = yf.download(tickers=crypto, period=time_frame, interval=interval)

    fig1 = go.Figure(data=[go.Candlestick(x=df.index,
                                          open=df.Open,
                                          high=df.High,
                                          low=df.Low,
                                          close=df.Close)])
    fig1.update_layout(title=f'Candle Chart of {crypto}', xaxis_title='Time', yaxis_title=f'{crypto}')

    fig2 = px.line(data_frame=df, x=df.index, y=df['Volume'], markers='o')
    fig2.update_layout(title=f'History of Volume {crypto}', xaxis_title='Time', yaxis_title=f'Volume of {crypto}')
    return fig1, fig2



if __name__ == '__main__':
    app.run_server(debug=True)
