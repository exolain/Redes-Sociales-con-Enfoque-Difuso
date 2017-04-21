import pandas as pd
import numpy as np
import requests

class Preprocess():

    def __init__(self):
        #GOOGLE_MAPS_DIST_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'
        # #GOOGLE_MAPS_TRAFFIC_MODEL = 'pessimistic'
        self.GOOGLE_MAPS_GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
        self.GOOGLE_MAPS_API_KEY = 'AIzaSyDyvEBuQ2z5RSowOkAmt_UtfGFakPcbVRE'

    def preprocess_data(self):
        df = pd.read_csv('../data/raw/Waze_Jam_Data.csv')
        data4 = df[df["city"]=="Boston, MA"]
        df = pd.DataFrame(data4)

        data = df.as_matrix(columns=["injectDate","street","city","delay","endNode"])

        """
        inject_date = fecha en que se realiza el movimiento
        street = punto inicial (de salida)
        delay = tiempo adicional debido a trafico? quitarlo?
        endNode = destino final
        """
        new = pd.DataFrame(data)
        new.columns = ["injectDate","street","city","delay","endNode"]
        
        data2 = new.sample(frac=0.02)
        new2 = pd.DataFrame(data2)

        data3 = new2.dropna().to_csv("../data/clean/Waze_Jam_Data.csv")
        return new2.dropna()
    
    def generate_neighborhoods_column(self):
        print "Starting neighborhood addition"
        prep_data = self.preprocess_data()
        df = pd.DataFrame(prep_data)
        for index, row in df.iterrows():
            payload = {
                'address' : str(row['street'])+','+str(row['city']),
                'key' : self.GOOGLE_MAPS_API_KEY
            }

            response = requests.get(self.GOOGLE_MAPS_GEOCODE_URL, params=payload)
            json_resp = response.json()

            for component in json_resp['results']:
                for comp in (component['address_components']):
                    if 'neighborhood' in comp['types']:
                        df.set_value(index,'neighborhood_initial',comp['long_name'])

            payload = {
                'address' : str(row['endNode'])+','+str(row['city']),
                'key' : self.GOOGLE_MAPS_API_KEY
            }
            response2 = requests.get(self.GOOGLE_MAPS_GEOCODE_URL, params=payload)
            json_resp = response2.json()

            for component in json_resp['results']:
                for comp in (component['address_components']):
                    if 'neighborhood' in comp['types']:
                        df.set_value(index,'neighborhood_destination',comp['long_name'])


                        
        df.to_csv("../data/clean/Waze_Jam_Data.csv")


        #
        #    row['neighborhood_initial'] = df['street']
        #df['neighborhood_destination'] = df.apply[lambda row: row['endNode']]
        #df['count'] = df.groupby('inject_date','neighborhood1','neighborhood2')['street'].transform(pd.Series.value_counts)
