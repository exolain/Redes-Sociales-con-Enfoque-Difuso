import pandas as pd
import numpy as np
import requests
import time
import calendar
class Preprocess():

    def __init__(self):
        self.GOOGLE_MAPS_DIST_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'
        #GOOGLE_MAPS_TRAFFIC_MODEL = 'pessimistic'
        self.GOOGLE_MAPS_GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
        self.GOOGLE_MAPS_API_KEY = 'AIzaSyDyvEBuQ2z5RSowOkAmt_UtfGFakPcbVRE'

    def preprocess_data(self):
        df = pd.read_csv('../data/raw/Waze_Jam_Data.csv')
        data4 = df[df["city"]=="Boston, MA"]
        df = pd.DataFrame(data4)

        data = df.as_matrix(columns=["injectDate","street","city","endNode"])

        """
        inject_date = fecha en que se realiza el movimiento
        street = punto inicial (de salida)
        delay = tiempo adicional debido a trafico? quitarlo?
        endNode = destino final
        """
        new = pd.DataFrame(data)
        new.columns = ["injectDate","street","city","endNode"]
        
        data2 = new.sample(frac=0.05)
        new2 = pd.DataFrame(data2)

        #data3 = new2.dropna().to_csv("../data/clean/Waze_Jam_Data.csv")
        return new2.dropna()
    
    def generate_distance_time(self):
        prep_data = pd.read_csv('../data/clean/Waze_Jam_Data.csv')
        df = pd.DataFrame(prep_data)
                
        for index, row in df.iterrows():
            from_time =  calendar.timegm(time.strptime(row['injectDate'],  '%m/%d/%Y %I:%M:%S %p'))

            payload = {
                'origins' : str(row['street'])+','+str(row['city']),
                'departure_time' : from_time,
                'destinations' : str(row['endNode'])+','+str(row['city']),
                'key' : self.GOOGLE_MAPS_API_KEY
            }


            response = requests.get(self.GOOGLE_MAPS_DIST_MATRIX_URL, params=payload)
            json_resp = response.json()
            
            for rowi in json_resp['rows']:
                for element in (rowi['elements']):
                    if 'duration' in element:
                        duration = (element['duration'])['value']
                        distance = (element['distance'])['value']
                        df.set_value(index,'duration',duration)
                        df.set_value(index,'distance',distance)

        df.to_csv("../data/clean/Waze_Jam_Data2.csv")


        #
        #    row['neighborhood_initial'] = df['street']
        #df['neighborhood_destination'] = df.apply[lambda row: row['endNode']]
        #df['count'] = df.groupby('inject_date','neighborhood1','neighborhood2')['street'].transform(pd.Series.value_counts)
