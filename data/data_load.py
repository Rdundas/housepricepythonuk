import pandas as pd
from datetime import datetime


def print_message(message):
    print(message)



def load_initial_data(filepath,min_year=1900,postcodes=None):
    '''
    'loads inital data, takes a filepath and minimum year
    columns to keep will not change
    '''
    i=0
    data_columns=['ID','value','date','zip_code','type','commercial','lease',
            'name_number']
    dict={}
    for chunk in pd.read_csv(filepath,header=None,chunksize=10000):

        #get first eight rows
        df=chunk.iloc[:,0:8]
        df.columns=data_columns
        #add year/month
        df['year']=df['date'].str[0:4].astype('int16')
        df['month']=df['date'].str[5:7].astype('int8')
        df['postcode_area']=df['zip_code'].str.split(' ',expand=True)[0]
        #drop years don't want
        df=df[df['year']>=min_year]
        #only keep postcodes
        if postcodes is not None:
            df=df[df['postcode_area'].isin(postcodes)]
        #keep non empty dictionaries
        if df.shape[0]>0:
            dict['chunk'+str(i)]=df
        i=i+1
    return pd.concat(dict.values(), ignore_index=True)


