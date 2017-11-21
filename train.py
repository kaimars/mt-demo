import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib

class ModelTrainer:
    features = ['smoking_area', 'dress_code', 'accessibility', 'price', 'other_services', 'parking_lot']
    encoders = {}
    train_df = None
    model = None

    def LoadRawData(self, places_file, parking_file, rating_file):
        df1 = pd.read_csv(places_file,
                          usecols=['placeID', 'price', 'smoking_area', 'other_services', 'dress_code', 'accessibility'],
                          dtype={'placeID': 'int64',
                                 'price': 'category',
                                 'smoking_area': 'category',
                                 'other_services': 'category',
                                 'dress_code': 'category',
                                 'accessibility': 'category'})
        df2 = pd.read_csv(parking_file,
                          dtype={'parking_lot': 'category'})
        ratings_raw = pd.read_csv(rating_file, usecols=["placeID", "rating"])
        place_rating_means = ratings_raw.groupby("placeID", as_index=False).median().astype('int')
        self.train_df = df1.merge(df2, on="placeID").merge(place_rating_means, on="placeID")
        return self.train_df

    def TransformData(self):
        for feature in self.features:
            encoder = LabelEncoder()
            encoder.fit(self.train_df[feature])
            self.train_df[feature] = encoder.transform(self.train_df[feature])
            self.encoders[feature] = encoder

    def ExportTrainingData(self, path):
        self.train_df.to_csv(path)

    def ExportMappingData(self, path):
        with open(path, 'wb') as file:
            pickle.dump(self.encoders, file)

    def LoadTrainingData(self, path):
        self.train_df = pd.read_csv(path)
        return self.train_df

    def TrainModel(self):
        x_values = self.train_df[list(self.features)].values
        y_values = self.train_df["rating"].values
        rf = RandomForestClassifier()
        self.model = rf.fit(x_values, y_values)
        #print(rf.score(x_values, y_values))
        return self.model

    def ExportModel(self, path):
        joblib.dump(self.model, path)

    def LoadModel(self, path):
        self.model = joblib.load(path)

if __name__ == "__main__":
    # smoke test scenario
    mt = ModelTrainer()
    df = mt.LoadRawData('data/geoplaces2.csv', 'data/chefmozparking.csv', 'data/rating_final.csv')
    print(df.head())
    mt.TransformData()
    mt.ExportTrainingData('training.csv')
    mt.ExportMappingData('mapping.dat')
    with open('mapping.dat', 'rb') as mapping_file:
        print(pickle.load(mapping_file)['price'].classes_)
    mt.TrainModel()
    mt.ExportModel('model.dat')
    mt.LoadModel('model.dat')