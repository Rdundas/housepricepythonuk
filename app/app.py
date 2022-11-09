import pandas as pd
from dash import dcc, html, Dash, Input, Output
import plotly.express as px
from flask import Flask

#if want to run locally or via docker, first row needed via docker
try:
    from app.config import current_file 
except:
    from config import current_file 

#for gunicorn

app=Dash(__name__)
server=app.server
#for local
#app=Dash(__name__)
app.title='Dashboard'

df=pd.read_csv(current_file)


#get dropdowns
house_type_dropdown=list(set(df['type']))
#
postcode_list = [{'label': i, 'value': i} for i in df['postcode_area'].unique()]
postcode_list.insert(0,{'label': 'All', 'value': 'All'})


#basic layout
app.layout = html.Div([
    html.Div(children=[
        html.H1(children='Manchester House Price Dashboard')
        ]
    ),
    #Add Dropdowns
    #House Type
    html.Div(children=[
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
            style=dict(width='50%')
            ),
        #Lease Type
        html.Label(['Lease Type'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='lease_dropdown'
        ,options=[
            {'label':'F','value':'F'},
            {'label':'L','value':'L'}
        ],
        value='F',
        style=dict(width='50%')
        )
    ],style=dict(display='flex')
    ),
    #Postcode Areas
    html.Div(children=[
        html.Label(['Postcode Area Type'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='postcode_area_type_dropdown'
        ,options=[
            {'label':'Area','value':'area'},
            {'label':'Sector','value':'sector'}
        ],
        value='area'
        ,style=dict(width='50%')
        ),
        #Postcodes
        html.Label(['Postcodes'],style={'font-weight': 'bold', "text-align": "center"}),
        #Need Special Processing for Postcodes
        #End Special Processing
        dcc.Dropdown(id='postcode_area_dropdown'
        ,options=postcode_list
        ,value='All'
        #,multi=True
        ,style=dict(width='50%')
        )
        ],style=dict(display='flex')
    ),
    #Year
    html.Div(children=[
        dcc.Graph(
            id='house_price_uk_graph'
            ) 
    ])
]#,style={'display': 'flex', 'flex-direction': 'column'}
)


def create_figure(df,postcode_area_type):
    if postcode_area_type=='area':
        fig=px.line(
        data_frame=df[['postcode_area','value','year']].groupby(['postcode_area','year']).mean().reset_index()
        ,x="year",y="value",color='postcode_area'
        )
    else:
        fig=px.line(
        data_frame=df[['postcode_sector','value','year']].groupby(['postcode_sector','year']).mean().reset_index()
        ,x="year",y="value",color='postcode_sector'
        )
    return fig

@app.callback(
    Output('house_price_uk_graph','figure'),
            [
            Input('house_type_dropdown','value'),
            Input('lease_dropdown','value'),
            Input('postcode_area_type_dropdown','value'),
            Input('postcode_area_dropdown','value')
            ])
def update_figure(house_type,lease,postcode_area_type,postcode_area):
    df_out=df[df['lease']==lease]
    df_out=df_out[df_out['type']==house_type]
    if postcode_area=='All':
        pass
    else:
        df_out=df_out[df_out['postcode_area']==postcode_area]
    fig=create_figure(df_out,postcode_area_type)
    return fig

#Possibly need to remove to run in Prod
if __name__ =='__main__':
    #changed from 127.0.0.1
   app.run_server(host='0.0.0.0', port=8050,debug=True)
 