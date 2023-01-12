#Deploys our model as an API

from fastapi import FastAPI
from fastapi.testclient import TestClient
import uvicorn
 
# Declaring our FastAPI instance
app = FastAPI()
 
# Defining path operation for root endpoint
@app.get('/')
def main():
    return {'message': 'Welcome to the Manchester House Price API!'}
 
# Defining path operation for /name endpoint
#@app.get('/{name}')
#def hello_name(name : str):
#    # Defining a function that takes only string as input and output the
#    # following message.
#    return {'message': f'Welcome to My First Model API!, {name}'}#

#Basic Model Code as well as data set
import pandas as pd
import pickle
from app.config import model_output_path

#Load Model
with open(model_output_path, 'rb') as target_file:
    model= pickle.load(target_file)

from pydantic import BaseModel

class request_body(BaseModel):
#set data types expectd here
    zip_code: str
    type: str
    commercial: str
    lease : str
    name_number: str
    flat : str
    road: str 
    year: int
    month : int
    postcode_area : str
    postcode_sector: str
    day: int


@app.post('/predict')
def predict(data : request_body):
    test_data = [[
        data.zip_code,
        data.type,
        data.commercial,
        data.lease,
        data.name_number,
        data.flat,
        data.road,
        data.year,
        data.month,
        data.postcode_area,
        data.postcode_sector,
        data.day
    ]]
    prediction = model.predict(test_data).tolist()
    return { 'value' : prediction}


#to run in terminal if needed
#uvicorn model.api:app --reload