import pandas as pd
from datetime import datetime
from pandas.testing import assert_frame_equal
#Contains unit tests for data load functions

import sys
sys.path.append("..")

from data.data_loading import load_initial_data
#python3 -m tests.test_data_loading allows this file to run

#Test filepaths
test_filepath_in='tests/test_data_in.csv'
test_filepath_out='tests/test_data_out.csv'

def test_init_load():
    '''
    #test the initial load data function
    '''
    data_out=pd.read_csv(test_filepath_out)
    processed_data=load_initial_data(test_filepath_in,2019,['NR6'])
    assert_frame_equal(processed_data.astype(str), data_out.astype(str)), "Not getting expected data out"

#to run all tests
#python3 -m pytest

