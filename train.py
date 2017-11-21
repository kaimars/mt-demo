import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

df1 = pd.read_csv("data/geoplaces2.csv",
                  usecols=['placeID', 'price', 'smoking_area', 'other_services', 'dress_code', 'accessibility'],
                  dtype={'placeID': 'int64',
                         'price': 'category',
                         'smoking_area': 'category',
                         'other_services': 'category',
                         'dress_code': 'category',
                         'accessibility': 'category'})
df2 = pd.read_csv("data/chefmozparking.csv",
                  dtype={'parking_lot': 'category'})
ratings_raw = pd.read_csv("data/rating_final.csv", usecols=["placeID", "rating"])
place_rating_means = ratings_raw.groupby("placeID", as_index=False).median().astype('int')
train_df = df1.merge(df2, on="placeID").merge(place_rating_means, on="placeID")

features = ['smoking_area', 'dress_code', 'accessibility', 'price', 'other_services', 'parking_lot']
encoders = {}
for feature in features:
    encoders[feature] = LabelEncoder()
    encoders[feature].fit(train_df[feature])
    train_df[feature] = encoders[feature].transform(train_df[feature])

print(encoders['price'].classes_)
encoders_path = 'encoders.pkl'
list_pickle = open(encoders_path, 'wb')
pickle.dump(encoders, list_pickle)
list_pickle.close()

list_unpickle = open(encoders_path, 'rb')
numbers_list = pickle.load(list_unpickle)
print(numbers_list['price'].classes_)

x_values = train_df[list(features)].values
y_values = train_df["rating"].values
rf = RandomForestClassifier()
model = rf.fit(x_values, y_values)
print(rf.score(x_values, y_values))