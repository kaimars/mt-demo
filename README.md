This document describes the solution made to solve task described in "Task description.docx".

## Solution overview
The solution has 3 parts: 
* data pipeline for rebuilding the prediction model (pipeline.py)
* web service to execute the prediction model (api/webapi.py)
* prediction model trainer (train.py)

### Data pipeline (pipeline.py)
This is set of Luigi framework tasks: DeployModel, TrainModel, PrepareData, CollectData.
TrainModel and DeployModel are meant to be used by end user, other are subtasks and not so useful standalone.
It is assumed that training the model and using the model can be done independently thus the training results are saved to file and can then be deployed to target environment. DeployModel is used to deploy the new version of prediction model to web service.
#### Usage
```
$ PYTHONPATH='.'
$ luigi --module pipeline DeployModel --local-scheduler
$ luigi --module pipeline TrainModel --local-scheduler
```
DeployModel is the default task, so you can execute it also like this:
```
$ python pipeline.py
```
Note that if the web service is running it has to be restarted to bring new prediction model into effect.

### Web service
Web service is a Flask application in file /api/webapi.py. 
#### Usage
To run the web service, **first run DeployModel task** described above and then run
```
$ cd api
$ python webapi.py
```
The web service is by default configured to use port 5000. Open [http://127.0.0.1:5000] to test the service. The web application is documented using Swagger API and has page to make test calls to the service.

### Prediction model trainer
To separate data model training tasks from web service and scheduling concerns, I put it separately to train.py.
Based on given features and database description (/data/README) I mapped features to data columns as follows:
* Price -> geoplaces2.csv/price
* Parking -> chefmozparking.csv/parking_lot
* Smoking Area -> geoplaces2.csv/smoking_area
* Other Services -> geoplaces2.csv/other_services
* Dress Code -> geoplaces2.csv/dress_code
* Accessibility -> geoplaces2.csv/accessibility
* Rating -> rating_final.csv/rating
For given features all restaurants had values for all features, so no decisions were made about missing data. Also all restaurants had some ratings. I decided to use most common rating (mode) to fit the prediction model because it had larger variability than mean value. After merging the 3 data files and encoding values to numeric values I got the training data. 
Decision tree classifier is used. Cross-validatation or other evaluation techniques are not used since the training is not in focus for the task.

## Final notes
Collecting the data for feeding the model trainer was quite easy due to simple data.

Luigi framework was totally new for me and the principle of cancellable/resumable workflow made me rethink how split the workflow into smaller chunks.

Previously I had brief exposure to Flask framework. During the task I discovered flask_restplus package and decided to use the opportunity to learn this also. Nice way to document web services!
