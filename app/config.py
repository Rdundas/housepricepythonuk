#config file for model
from catboost import CatBoostRegressor

postcodes=['M20','M21','M33','SK1','SK12','SK15','SK2','SK3'
,'SK4','SK5','SK6','SK7','SK8','SK9','WA13','WA14','WA15','WA16']


#Initial Data filepaths, this data does not exist in project so this would need to be modified
#In reality this would likely come from a seperate DB/job
data_in_filepath="pp-complete.csv"
data_out_filepath="app"

#Loaded data filepaths, this forms the core of the app
current_file="app/processed2022-10-31.csv"
min_year=2010

#ML PARAMS
year_ml_split=2019
model=CatBoostRegressor(n_estimators=300,random_state=42,max_depth=10,l2_leaf_reg=10)
retrain_ml_model=False

#expected columns for data input to ml model
expected_columns=['value', 'zip_code', 'type', 'commercial', 'lease', 'name_number',
       'flat', 'road', 'year', 'month', 'postcode_area', 'postcode_sector',
       'day']
#cat features for ml model
cat_features=['zip_code', 'type', 'commercial', 'lease', 'name_number',
       'flat', 'road', 'postcode_area',
       'postcode_sector']
#output pathfor ml model
model_output_path="model/model.pkl"


