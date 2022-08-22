import pandas as pd
from dash import dcc, html, Dash, Input, Output
import plotly.express as px
from flask import Flask

from app.config import current_file 

server = Flask(__name__)
app=Dash(server=server)
#app=Dash(__name__)
app.title='Dashboard'

df=pd.read_csv(current_file)

#get dropdowns
house_type_dropdown=list(set(df['type']))

#basic layout
app.layout = html.Div(children=[
    html.H1(children='Manchester House Price Dashboard'),

    html.Label(['House Type'],style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(id='house_type_dropdown'
        ,options=[
        {'label':'S','value':'S'},
        {'label':'D','value':'D'},
        {'label':'T','value':'T'},
        {'label':'O','value':'O'},
        {'label':'F','value':'F'},
        ],
        value='D',
        #multi=True
        ),
    html.Label(['Lease Type'],style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(id='lease_dropdown'
    ,options=[
        {'label':'F','value':'F'},
        {'label':'L','value':'L'}
    ],
    value='F'
    ),
    dcc.Graph(
        id='house_price_uk_graph'
    ) 
])

def create_figure(df):
    fig=px.line(
    data_frame=df[['postcode_area','value','year']].groupby(['postcode_area','year']).mean().reset_index()
    ,x="year",y="value",color='postcode_area'
    )
    return fig

@app.callback(
    Output('house_price_uk_graph','figure'),
            [
            Input('house_type_dropdown','value'),
            Input('lease_dropdown','value')
            ])
def update_figure(house_type,lease):

    df_out=df[df['lease']==lease]
    df_out=df_out[df_out['type']==house_type]
    fig=create_figure(df_out)
    return fig


    
if __name__ =='__main__':
    #app.run_server(host='127.0.0.1', port=8050,debug=True)
    app.run_server()