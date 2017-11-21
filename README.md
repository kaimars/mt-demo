This document describes the solution made to solve task described in "Task description.docx".

## Solution overview
The solution has 3 parts: 
* data pipeline for rebuilding the prediction model (pipeline.py)
* prediction model trainer (train.py)
* web service to execute the prediction model (api/webapi.py)

### pipeline.py

It is assumed that training the model and using the model can be done independently thus the training results are saved to file and can then be deployed to target environment.



Log
Based on given features and database description (/data/README) I mapped features to data columns as follows:
* Price -> geoplaces2.csv/price
* Parking -> chefmozparking.csv/parking_lot
* Smoking Area -> geoplaces2.csv/smoking_area
* Other Services -> geoplaces2.csv/other_services
* Dress Code -> geoplaces2.csv/dress_code
* Accessibility -> geoplaces2.csv/accessibility
* Rating -> rating_final.csv/rating

