# Manchester House Price Project

This is an example python project that contains many of the key components that might be expected in a modern python application. At the moment only house prices in Manchester from 2014-2022 are included. This keeps data volumes low but still has enough data to test the concepts below.

These are

A config file containing run time parameters (config.py)

A python virtual environment and jupyter notebook, that can be created in the directory and can be used for model prototyping.

A dash dashboard (app.py) that has an ML model embedded into it (model.pkl/model.py). 

A FASTApi end point (api.py). This is basic but shows how to set a model up as an api using the framework.

Unit testng via pytest split by module (test_data_loading.py and test_model.py), with data in/out added.

Dev and Prod docker files, the former containing volumes so it can be developed dynamically locally. The latter can be deployed onto AWS.

Dev and Prod docker compose files, to ease the building/running of the docker containers.

Github actions that run unit tests on merge to main (and stop merges that fail), and deploy the container to AWS (using gitlab keys and the task definition in task-definition.json)

Data loading functions which are not useful here (they run against the extracts generated here https://landregistry.data.gov.uk/app/ukhpi). The initial data set was not included in the repo for size reasons. A flat file (processed2022-10-31.csv) has been included as a data input, but this could be extended to be from a DB and have update functionality to it. This has not been included as it was not a key considderation


Richard Dundas 16th Jan 2023

