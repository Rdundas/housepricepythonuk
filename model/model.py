#builds a model
import pandas as pd 
from datetime import datetime    
import numpy as np
from catboost import CatBoostRegressor
import pickle

#if want to run locally or via docker, first row needed via docker

from app.config import current_file,year_ml_split,model,expected_columns,cat_features,retrain_ml_model,model_output_path

df = pd.read_csv(current_file)

#Basic Data Prep
def basic_model_data_prep(df):
    #read data and basic cleaning i.e. remove ID column and clean up dates
    try:
        df.drop(['Unnamed: 0','ID'],axis=1,inplace=True)
    except:
        pass
    #fill nas
    df.fillna(0,inplace=True)
    #convert date
    df['date']=df['date'].astype('datetime64')
    #get day, month and year
    df['day']=df['date'].dt.day
    df['month']=df['date'].dt.month
    df['year']=df['date'].dt.year
    df.drop(['date'],axis=1,inplace=True)
    df.drop('address',axis=1,inplace=True)
    #remove offices
    df=df[df['type']!='O']

    return df

#Adjust data for trending
def adjust_for_trend(df):
    '''
    Adjusts for house price trend by year, currently calculates from data loaded in
    '''
    adjust=df[['year','value']].groupby('year').mean().reset_index()
    latest_value=float(adjust['value'][-1:])
    adjust['adjustment']=adjust['value']/latest_value
    adjust.drop('value',axis=1,inplace=True)
    df=df.merge(adjust)
    df['value']=df['value']/df['adjustment']
    df.drop('adjustment',axis=1,inplace=True)
    return df

#Enforces the schema and errors if fails, not done for now
#def enforce_schema(df,expected_columns):
#    '''
#    Checks the columns 
#    '''
#    data_res = pd.DataFrame(columns = expected_columns)
#    for col in expected_columns:
#        try:
#            data_res[col] = df[col]
#        except:
#            data_res[col] = 0
                
#    return data_res
#df_col_check

#Create Model class
class Model:
     def __init__(self,df):
         self.df=df
         self.cat_features=cat_features
         self.target='value'
         self.expected_columns=expected_columns
         self.cat_features=cat_features
         self.year_ml_split=year_ml_split
         self.model=model
    #could add feature imputation here e.g. for continuous features. Start with defaults but have an update method

    #fit ml model methods, methods very simple so not added unit testing. Could look to add in a future phase
     def split(self):
        X_train,y_train=df[df['year']<=year_ml_split].drop('value',axis=1),df[df['year']<=year_ml_split]['value']
        X_test,y_test=df[df['year']>year_ml_split].drop('value',axis=1),df[df['year']>year_ml_split]['value']
        self.X_train,self.X_test,self.y_train,self.y_test=X_train,X_test,y_train,y_test

     def fit(self):
        self.model=self.model.fit(self.X_train,self.y_train,cat_features=self.cat_features,silent=True)

     def predict(self):
        self.train_predictions=model.predict(self.X_train)
        self.test_predictions=model.predict(self.X_test)
    
     def r_squared(self):
        self.train_rsquared=1-np.sum(((self.train_predictions-self.y_train)**2))/np.sum(((self.y_train-np.mean(self.y_train))**2))
        self.test_rsquared=1-np.sum(((self.test_predictions-self.y_test)**2))/np.sum(((self.y_test-np.mean(self.y_test))**2))

#Now prep data and pass into model
df=basic_model_data_prep(df)
#df=adjust_for_trend(df)
model_instance=Model(df)

def get_model(model_instance,retrain_ml_model=True):
    if retrain_ml_model:
        #model_instance.enforce_schema
        model_instance.split()
        model_instance.fit()
        model_instance.predict()
        model_instance.r_squared()
        print(model_instance.train_rsquared)
        print(model_instance.test_rsquared)
        pickle.dump(model_instance.model,open('model.pkl','wb'))
        model=model_instance.model
    else:
        with open(model_output_path, 'rb') as target_file:
            model= pickle.load(target_file)

    return model

model=get_model(model_instance,retrain_ml_model=retrain_ml_model)














