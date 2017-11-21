This document describes the solution made to solve task described in "Task description.docx".

## Solution overview
The solution has 3 parts: 
* data pipeline for rebuilding the prediction model (pipeline.py)
* prediction model trainer (train.py)
* web service to execute the prediction model (api/webapi.py)

### pipeline.py
This is set of Luigi framework tasks: DeployModel, TrainModel, PrepareData, CollectData.
TrainModel and DeployModel are meant to be used by end user, other are subtasks and not so useful standalone.
It is assumed that training the model and using the model can be done independently thus the training results are saved to file and can then be deployed to target environment. DeployModel is used to deploy the new version of prediction model over to web service.
#### Usage
```
$ luigi --module pipeline DeployModel --local-scheduler
$ luigi --module pipeline TrainModel --local-scheduler
```
Note that if the web service is running it has to be restarted to bring new prediction model into effect.


Log
Based on given features and database description (/data/README) I mapped features to data columns as follows:
* Price -> geoplaces2.csv/price
* Parking -> chefmozparking.csv/parking_lot
* Smoking Area -> geoplaces2.csv/smoking_area
* Other Services -> geoplaces2.csv/other_services
* Dress Code -> geoplaces2.csv/dress_code
* Accessibility -> geoplaces2.csv/accessibility
* Rating -> rating_final.csv/rating

