#file to load data, simply runs the load_initial_data function based on config params, it is not part of the main app
import os,sys

from datetime import datetime

from data_loading import load_initial_data

#load config
currentdir = os.path.dirname(os.path.realpath(__name__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from app.config import *

df=load_initial_data(data_in_filepath,min_year,postcodes)
df.to_csv(data_out_filepath+'\\processed'+datetime.now().strftime(('%Y-%m-%d'))+'.csv')