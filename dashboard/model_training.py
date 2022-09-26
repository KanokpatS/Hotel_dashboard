import pandas as pd
pd.options.mode.chained_assignment = None
from sklearn.cluster import KMeans
import pickle

class Model_clustering:
    def __init__(self, n_class:int, type:str):
        """
        :param n_class: Number of cluster
        :param type: Type of clustering
        """
        self.n_class = n_class
        self.type = type

    def clean_data(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Clean hotel data
        :param df: Hotel dataframe
        :return: Hotel dataframe
        """
        df['latitude'] = df['latitude'].astype(float)
        df['longitude'] = df['longitude'].astype(float)
        df['rating'] = df['rating'].astype(float)
        df['price'] = df['price'].astype(float)
        df['review'] = df['review'].astype(int)
        df['facilities'] = df['facilities1']
        return df

    def create_feature_facilities(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Create feature facilities
        :param df: Hotel dataframe
        :return: Hotel dataframe with feature facilities
        """
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

    def preprocess(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Combine clean data and create feature function and choose feature to train model
        :param df: Hotel dataframe
        :return: Dataframe for training
        """
        df = self.clean_data(df)
        df = self.create_feature_facilities(df)
        dff = df[['rating', 'review', 'star', 'price', 'Spa', 'Beach access', 'Fitness center', 'Parking',
                  'Breakfast', 'Free parking', 'Airport shuttle', 'Pool', 'Air-conditioned', 'Wi-Fi']]
        dff = pd.get_dummies(dff)
        dff = dff.drop(columns=['star_No data'])
        return dff

    def training(self, df:pd.DataFrame):
        """
        Train model
        :param df: dataframe from preoprecess function
        :return: Model
        """
        dff = self.preprocess(df)
        if self.type == 'KMeans':
            model = KMeans(n_clusters=self.n_class)
            model.fit(dff)
        return model

    def predict(self, df:pd.DataFrame, model):
        """
        Predict data and save result of model prediction
        :param df: Hotel dataframee
        :param model: Model
        :return: Prediction dataframe
        """
        dff = self.preprocess(df)
        all_predictions = model.predict(dff)
        df['predict'] = all_predictions
        filename = f'data/output/result_{self.type}_{self.n_class}.xlsx'
        df.to_excel(filename)
        return df

if __name__ == '__main__':
    df = pd.read_excel('data/hotel_data.xlsx')
    model_clustering = Model_clustering(n_class=5, type='KMeans')
    model = model_clustering.training(df)
    result_df = model_clustering.predict(df, model)


