import pandas as pd
import pickle
import streamlit as st
import plotly.express as px

#if want to run locally or via docker, first row needed via docker
try:
    from app.config import current_file,model_output_path
except:
    from config import current_file,model_output_path

#Load Data
df=pd.read_csv(current_file)

#Load ML model, probably better to have the api as a seperate component that is called by this app
with open(model_output_path, 'rb') as target_file:
    model= pickle.load(target_file)

#get dropdowns, first house types
house_type_list=sorted(list(set(df['type'])))
house_type_list.append('All')

#lease types
lease_type_list=sorted(list(set(df['lease'])))
lease_type_list.append('All')

#postcode lists
postcode_area_list=sorted(list(set(df['postcode_area'])))
postcode_area_list.append('All')
postcode_sector_list=sorted(list(set(df['postcode_sector'])))
postcode_sector_list.append('All')

#Title
st.title('House Price Dashboard')
#Header
st.header('Select inputs')
#Split inputs into two columns
col1, col2 = st.columns(2)
#Order dropdowns
with col1:
    house_type_select= st.multiselect(
        'Select House Type',
        house_type_list,
        ['D'])

    lease_type_select= st.multiselect(
        'Select Lease Type',
        lease_type_list,
        ['F'])

with col2:
    postcode_area_level_select=st.selectbox(
        'Select Postcode area level',
        options=pd.Series(['postcode_area','postcode_sector']),
        index=0)

    postcode_select= st.multiselect(
        'Select Postcode',
        postcode_area_list if postcode_area_level_select=='postcode_area' else postcode_sector_list,
        ['All'])

#Collect selections in a dictionary for ease of use/coding. If add more filters need to add this to dictionary
select_dict={
    'type':house_type_select,
    'lease':lease_type_select,
    postcode_area_level_select:postcode_select
}

#Apply filters to data sequentially, if 'All' selected no filter is added
def filter_data(df,select_dict):
    filtered_df=df
    for keys,values in select_dict.items():
        if 'All' in values:
            pass
        else:
            filtered_df=filtered_df[filtered_df[keys].isin(values)]
    return filtered_df

#Create aggregated data for plotting
def create_figure(df,postcode_area_level_select):
    '''
    creates data for graph aggregating by year/postcode area type
    '''
    graph_df=df[[postcode_area_level_select,'value','year']].groupby([postcode_area_level_select,'year']).mean().reset_index()
    return graph_df

#Apply filtering/aggregation to create graph data
filter_df=filter_data(df,select_dict)
graph_df=create_figure(filter_df,postcode_area_level_select)
#Add plotly wrapper and display graph
fig=px.line(data_frame=graph_df,x="year",y="value",color='postcode_area')
st.plotly_chart(fig)
