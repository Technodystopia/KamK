"""
This module is used to parse weather data from an API and store it in a database.
"""

import json
import requests
import duckdb
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import warnings

class WeatherData:
    """
    A class to represent the weather data.
    """

    def __init__(self, db_file='../data/stats.duckdb', api_url="https://opendata.fmi.fi/wfs/fin?service=WFS&version=2.0.0&"):
        """
        Constructs all the necessary attributes for the weather data object.

        Parameters:
        db_file (str): Path to the database file.
        api_url (str): URL of the API.
        """
        self.con = duckdb.connect(db_file)
        self.api_url = api_url

    def parse_data(self, xml):
        """
        Parse the XML data from the API response.

        Parameters:
        xml (str): XML data as a string.

        Returns:
        DataFrame: Parsed data as a pandas DataFrame.
        """
        print("Parsing data...")
        root = ET.fromstring(xml)
        namespaces = {'wfs':'http://www.opengis.net/wfs/2.0', 'BsWfs':'http://xml.fmi.fi/schema/wfs/2.0', 'gml':'http://www.opengis.net/gml/3.2'}
        try:
            pos = root.findall('.//gml:pos', namespaces)[0].text.strip().split(" ")
        except IndexError as error:
            print(f"Error: {error}")
        list = []
        for element in root.findall('.//BsWfs:BsWfsElement', namespaces):
            d = {}
            tmp = []
            for c_element in element:
                if 'Time' in c_element.tag:
                    d[c_element.tag.split("}")[-1]] = pd.to_datetime(c_element.text)
                if 'ParameterName' in c_element.tag:
                    tmp.append(c_element.text)
                if 'ParameterValue' in c_element.tag:
                    if 'NaN' in c_element.text:
                        tmp.append(np.nan)
                    else:
                        tmp.append(float(c_element.text))
            d[tmp[0]] = tmp[-1]
            list.append(d)
        df = pd.DataFrame(list)
        df.rename(columns={'t2m':'Temperature', 'rh':'Humidity', 'snow_aws':'Snow depth', 'ri_10min':"Rain intensity", 'r_1h':'Rain amount', 'p_sea': 'Air pressure', 'vis':'Visibility',
                            'ws_10min': 'Wind speed', 'wg_10min': 'Gust speed', 'wd_10min': 'Wind direction', 'td': 'Dew point', 'n_man': 'Cloud cover'}, inplace=True)

        df = df.groupby('Time').first()
        print("Data parsed.")
        return df

    def fill_db(self):
        """
        Fill the database with weather data from the API.
        """
        print("Filling database...")
        with open("data/json/data.json", "r") as file:
            data = json.load(file)
        bbox = data["bbox"]
        
        min_date = pd.to_datetime('2019-03-01')
        max_date = pd.to_datetime('2020-01-31')

        while min_date < max_date:
            period_end_date = min_date + pd.Timedelta(days=7)
            start = min_date.isoformat(timespec='seconds') + 'Z'
            end = period_end_date.isoformat(timespec='seconds') + 'Z'

            params = {
                "starttime": start,
                "endtime": end,
                "request": "getFeature",
                "storedquery_id": "fmi::observations::weather::simple",
                "bbox": bbox,
                "fmisid": "103794",
                "timestep": "60",
                "parameters": "t2m,ws_10min,wg_10min,wd_10min,n_man,rh,td,r_1h,ri_10min,snow_aws,p_sea,vis"
            }
            with warnings.catch_warnings():
                warnings.simplefilter(action='ignore', category=UserWarning)
                response = requests.get(self.api_url, params=params)
                weather_df = self.parse_data(response.text)
                weather_df.reset_index().to_sql('weather', self.con, if_exists='append', index=False) 
                print(f"Inserting weather data from {min_date.strftime('%d.%m.%Y')} to {period_end_date.strftime('%d.%m.%Y')}...")
                min_date = period_end_date
        print("Database filled.")

    def query_db(self, query):
        """
        Query the database.

        Parameters:
        query (str): SQL query.

        Returns:
        DataFrame: Query result as a pandas DataFrame.
        """
        print("Executing query...")
        result = self.con.execute(query).fetch_df()
        result.rename(columns={'Time': 'timestamp'}, inplace=True)
        result.set_index('timestamp', inplace=True)
        print("Query executed.")
        return result

    def close_db(self):
        """
        Close the database connection.
        """
        self.con.close()

weather_data = WeatherData()
weather_data.fill_db()
print("Database ready.")
result = weather_data.query_db("SELECT * FROM weather")
print(result.head(20))
weather_data.close_db()
