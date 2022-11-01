import unittest

import pandas as pd
from datetime import datetime
#Contains unit tests of code

from data.data_loading import load_initial_data
from pandas.testing import assert_frame_equal

#Test filepaths
test_filepath_in='tests/test_data_in.csv'
test_filepath_out='tests/test_data_out.csv'


class TestSum(unittest.TestCase):
    def test_list_int(self):
        """
        Test load initial data function, this processes data from raw csv into a more readable/useful format
        """
        data_out=pd.read_csv(test_filepath_out)
        processed_data=load_initial_data(test_filepath_in,2019,['NR6'])
        assert_frame_equal(processed_data.astype(str), data_out.astype(str)), "Not getting expected data out"

if __name__ == '__main__':
    unittest.main()

