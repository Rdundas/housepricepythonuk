import pandas as pd
from dash import dcc, html, Dash, Input, Output
import plotly.express as px


from config import * 

df=pd.read_csv(current_file)

app=Dash(__name__)

#get dropdowns
house_type_dropdown=list(set(df['type']))

#basic layout
app.layout = html.Div(children=[
    html.H1(children='Manchester House Price Dashboard'),
    dcc.Dropdown(id='house_type_dropdown'
        ,options=[
        {'label':'S','value':'S'},
        {'label':'D','value':'D'},
        {'label':'T','value':'T'},
        {'label':'O','value':'O'},
        {'label':'F','value':'F'},
        ],
        value='D'
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

@app.callback(Output('house_price_uk_graph','figure'),
            [Input('house_type_dropdown','value')])
def update_figure(selected_value):
    df_out=df[df['type']==selected_value]
    fig=create_figure(df_out)
    return fig

    
if __name__ =='__main__':
    app.run_server(debug=True)