"""
This class is used to take address contents from dataframe df,
and convert to coordinates LAT LONG.
The LAT LONG coordinates are then stored in the dataframe df.
Code is designed to be modular for reuse in the future.

Alan Ly 05-03-2020
"""
import pandas as pd
from geopy.geocoders import Nominatim
import time
from geopy.exc import GeocoderTimedOut


class my_geocoder:

    def __init__(self,df):
        
        #initialized a pandas dataframe 
        self.df = df
        self.geolocator = Nominatim(user_agent="price_map")

    def do_geocode(self,address, attempt=1, max_attempts=5):
        """recursively call geocoder if a timeout occurs maximum 5 attempts"""
        try:
            return self.geolocator.geocode(address)
        except GeocoderTimedOut:
            if attempt <= max_attempts:
                return self.do_geocode(address, attempt=attempt+1)
            raise

    def geo_converter(self):
        """Takes data frame and creates addr string and queries for lat long coordinates."""
        LAT_store = []
        LONG_store = []

        for index in range(0,len(self.df)):
            
            #create address string
            #if there isn't an RegionName column, throw an exception and create addr string without RegionName
            try:
                addr  = self.df['City'].iloc[index] + " " + self.df['State'].iloc[index] + " " + self.df['CountyName'].iloc[index] + " " + str(self.df['RegionName'].iloc[index])
            except:
                addr  = self.df['City'].iloc[index] + " " + self.df['State'].iloc[index] + " " + self.df['CountyName'].iloc[index] 
            
            #convert addr to lat long
            try:
                geo_addr = self.do_geocode(addr)
                LAT = geo_addr.latitude
                LONG= geo_addr.longitude
                
            except:
                #if null error occur due to address not found, store the null objects
                LAT = None
                LONG = None
            
            print(LAT,LONG)
            
            
            LAT_store.append(LAT)
            LONG_store.append(LONG)
        
        self.df["LAT"] = LAT_store
        self.df["LONG"] = LONG_store
        
        return self.df