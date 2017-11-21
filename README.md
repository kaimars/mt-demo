This document describes the solution made to solve task described in "Task description.docx".

Solution overview
The solution has 2 parts: building a prediction model (train.py) and using the model to predict rating (api/*).
It is assumed that training the model and using the model can be done independently thus the training results are saved to file and can then be deployed to target environment.



Log
Based on given features and database description (/data/README) I mapped features to data columns as follows:
	Price -> geoplaces2.csv/price
	Parking -> chefmozparking.csv/parking_lot
	Smoking Area -> geoplaces2.csv/smoking_area
	Other Services -> geoplaces2.csv/other_services
	Dress Code -> geoplaces2.csv/dress_code
	Accessibility -> geoplaces2.csv/accessibility
	Rating -> rating_final.csv/rating

