import pandas as pd
from datetime import datetime
from pandas.testing import assert_frame_equal
#Contains unit tests for model functions

import sys
sys.path.append("..")

from app.config import year_ml_split
from model.model import basic_model_data_prep, adjust_for_trend,Model

#load test file path out
test_filepath_in='tests/test_data_out.csv'
test_filepath_out='tests/basic_model_data_prep_out.csv'

def test_init_load():
        """
        Test basic model data prep function, this takes the processed data out and performs some basic data cleaning
        """
        data_out=pd.read_csv(test_filepath_out)
        processed_data=basic_model_data_prep(pd.read_csv(test_filepath_in))
        assert_frame_equal(processed_data.astype(str), data_out.astype(str)), "Not getting expected data out"

def test_adjust_for_trend():
        """
        Tests the adjust for trend funcion, the answer should all be equal to the last value
        """
        data={'year':[1,2,3],'value':[100,150,200]}
        data=pd.DataFrame.from_dict(data)
        processed_data=adjust_for_trend(data)
        assert processed_data.iloc[0,1]==200


