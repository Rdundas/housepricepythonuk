#from housepricepythonuk.data.data_load import print_message
#from housepricepythonuk.data.data_load import load_data

from datetime import datetime

from data.data_loading import print_message
from data.data_loading import load_initial_data

#load config
from config import *

df=load_initial_data(data_in_filepath,min_year,postcodes)
df.to_csv(data_out_filepath+'\\processed'+datetime.now().strftime(('%Y-%m-%d'))+'.csv')