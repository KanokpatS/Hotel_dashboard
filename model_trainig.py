import pandas as pd
pd.options.mode.chained_assignment = None
from sklearn.cluster import KMeans
import pickle

def preprocess(df):
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)
    df['rating'] = df['rating'].astype(float)
    df['price'] = df['price'].astype(float)
    df['review'] = df['review'].astype(int)
    df['facilities'] = df['facilities1']
    return df

def create_feature_facilities(df):
    all_facilities_list = list()
    for i in range(len(df)):
        facilities1 = df.facilities1[i]
        facilities2 = df.facilities2[i]
        facilities3 = df.facilities3[i]
        facilities4 = df.facilities4[i]
        facilities = [facilities1, facilities2, facilities3, facilities4]
        all_facilities_list.append(facilities1)
        all_facilities_list.append(facilities2)
        all_facilities_list.append(facilities3)
        all_facilities_list.append(facilities4)
        df['facilities'][i] = facilities
    df = df.drop(columns=['facilities1', 'facilities2', 'facilities3', 'facilities4'])
    for fac in list(set(all_facilities_list)):
        df[fac] = 0
    for i in range(len(df)):
        for fac in df['facilities'][i]:
            df[fac][i] = 1
    df['Wi-Fi'] = df['Wi-Fi'] + df['Free Wi-Fi']
    df['Breakfast'] = df['Breakfast'] + df['Free breakfast']
    df = df.drop(columns=['Free Wi-Fi', 'Free breakfast'])
    return df

def predict_and_save_result(df, model):
    all_predictions = model.predict(dff)
    df['prdict'] = all_predictions
    df.to_excel('data/result.xlsx')

def save_model(model):
    filename = 'model.sav'
    pickle.dump(model, open(filename, 'wb'))

if __name__ == '__main__':
    df = pd.read_excel('data/hotel_data.xlsx')
    df = preprocess(df)
    df = create_feature_facilities(df)
    dff = df[['rating', 'review', 'star', 'price', 'Spa', 'Beach access', 'Fitness center', 'Parking',
            'Breakfast', 'Free parking', 'Airport shuttle', 'Pool', 'Air-conditioned', 'Wi-Fi']]
    dff = pd.get_dummies(dff)
    dff = dff.drop(columns=['star_No data'])
    model = KMeans(n_clusters=5)
    model.fit(dff)

predict_and_save_result(dff, model)
save_model(model)

