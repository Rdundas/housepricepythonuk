#from housepricepythonuk.data.data_load import print_message
#from housepricepythonuk.data.data_load import load_data

from datetime import datetime

from data.data_load import print_message
from data.data_load import load_initial_data

postcodes=['M20','M21','M33','SK1','SK12','SK15','SK2','SK3'
,'SK4','SK5','SK6','SK7','SK8','SK9','WA13','WA14','WA15','WA16']

data_in_filepath="C:\\Users\\richa\\Documents\\DataScience\\House Price\\pp-complete.csv"
data_out_filepath="C:\\Users\\richa\\Documents\\DataScience\\House Price"
min_year=2019

df=load_initial_data(data_in_filepath,min_year,postcodes)
df.to_csv(data_out_filepath+'\\processed'+datetime.now().strftime(('%Y-%m-%d'))+'.csv')