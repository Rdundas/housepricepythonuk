#Plotly Dash App for ML dashboard
import pandas as pd
import pickle
from dash import dcc, html, Dash, Input, Output, State
import plotly.express as px
from flask import Flask
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

#if want to run locally or via docker, first row needed via docker
try:
    from app.config import current_file,model_output_path
except:
    from config import current_file,model_output_path

#Load Model
with open(model_output_path, 'rb') as target_file:
    model= pickle.load(target_file)


#for gunicorn
app=Dash(__name__)
server=app.server
#for local
#app=Dash(__name__)
app.title='Dashboard'

df=pd.read_csv(current_file)


#get dropdowns
house_type_dropdown=list(set(df['type']))
#postcode lists
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
    ]),
    #Now do API Inputs
    html.Div(children=[
    html.Label(['Predict Your Own House Price Here'],style={'font-weight': 'bold', "text-align": "center"}),
    html.H5('Postcode, must include spaces!'),
    dcc.Input(id='model_zip_code',placeholder='M20 6RS',type='text',maxLength=8),
    html.H5('House Type'),
    dcc.Dropdown(id='model_house_type'
            ,options=[
            {'label':'S','value':'S'},
            {'label':'D','value':'D'},
            {'label':'T','value':'T'},
            {'label':'O','value':'O'},
            {'label':'F','value':'F'},
            ],
            value='T',
            #multi=True
            style=dict(width='50%')
            ),
    html.H5('Commercial Building YN'),
    dcc.Dropdown(id='model_commercial'
            ,options=[
            {'label':'Y','value':'Y'},
            {'label':'N','value':'N'},
            ],
            value='N',
            style=dict(width='50%')
            ),
    html.H5('Freehold/Leasehold'),
    dcc.Dropdown(id='model_lease'
            ,options=[
            {'label':'F','value':'F'},
            {'label':'L','value':'L'},
            ],
            value='F',
            style=dict(width='50%')
            ),
    html.H5('Year'),
    dcc.Input(id='model_year',placeholder=2015,type='number',min=2015,max=2022),
    html.H5('Month'),
    dcc.Input(id='model_month',placeholder=1,type='number',min=8,max=12),
    dbc.Row([dbc.Button('Submit', id='submit-val', n_clicks=0, color="primary")]),
    html.Br(),
    dbc.Row([html.Div(id='prediction output')])

    ])
]#,style={'display': 'flex', 'flex-direction': 'column'}
)


def create_figure(df,postcode_area_type):
    '''
    creates the house price graph by year/postcode areas for either postcode area or postcode sector
    '''
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

#house price graph callback
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


#house price api callback, predicts value and doesn't display if not entered
@app.callback(
    Output('prediction output','children'),
    Input('submit-val', 'n_clicks'),
    State('model_zip_code','value'),
    State('model_house_type','value'),
    State('model_commercial','value'),
    State('model_lease','value'),
    State('model_year','value'),
    State('model_month','value'),
    )
def update_prediction(n_clicks,model_zip_code,model_house_type,model_commercial,model_lease,model_year,model_month):
    if n_clicks is None or n_clicks==0:
        raise PreventUpdate
    else:
        X=[
            model_zip_code,
            model_house_type,
            model_commercial,
            model_lease,
            '',
            '',
            '',
            model_year,
            model_month,
            model_zip_code.split(' ')[0],
            model_zip_code.split(' ')[0]+' '+model_zip_code.split(' ')[1][0],
            1
        ]

        prediction= model.predict(X)
        return f'The predicted house price value is {prediction}'


if __name__ =='__main__':
    #changed from 127.0.0.1
   app.run_server(host='0.0.0.0', port=80,debug=True)








