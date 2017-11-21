import pandas as pd
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib

class ModelTrainer:
    features = ['smoking_area', 'dress_code', 'accessibility', 'price', 'other_services', 'parking_lot']
    encoders = {}
    train_df = None
    model = None

    def LoadRawData(self, places_file, parking_file, rating_file):
        df1 = pd.read_csv(places_file,
                          usecols=['placeID', 'price', 'smoking_area', 'other_services', 'dress_code', 'accessibility'])
        df2 = pd.read_csv(parking_file)
        ratings_raw = pd.read_csv(rating_file, usecols=['placeID', 'rating'])
        # we use most common rating (mode) to train the prediction model
        aggregated_ratings = ratings_raw.groupby(['placeID'], as_index=False).agg(lambda x: x.value_counts().index[0])
        self.train_df = df1.merge(df2, on='placeID').merge(aggregated_ratings, on='placeID')
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
            joblib.dump(self.encoders, file)

    def LoadTrainingData(self, path):
        self.train_df = pd.read_csv(path)
        return self.train_df

    def TrainModel(self):
        x_values = self.train_df[list(self.features)].values
        y_values = self.train_df['rating'].values
        classifier = tree.DecisionTreeClassifier(min_samples_leaf=10)
        self.model = classifier.fit(x_values, y_values)
        return self.model

    def ExportModel(self, path):
        joblib.dump(self.model, path)


if __name__ == '__main__':
    # basic smoke test scenario
    mt = ModelTrainer()
    df = mt.LoadRawData('data/geoplaces2.csv', 'data/chefmozparking.csv', 'data/rating_final.csv')
    print(df.head(10))
    mt.TransformData()
    mt.ExportTrainingData('training.csv')
    mt.ExportMappingData('mapping.dat')
    with open('mapping.dat', 'rb') as mapping_file:
        print(joblib.load(mapping_file)['price'].classes_)
    mt.TrainModel()
    mt.ExportModel('model.dat')
    mt.LoadModel('model.dat')