import pandas as pd
from geopy.geocoders import Nominatim
import time
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="price_map")

def do_geocode(address, attempt=1, max_attempts=5):
    """recursively call geocoder if a timeout occurs maximum 5 attempts"""
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return do_geocode(address, attempt=attempt+1)
        raise

def geo_converter(df):
    """Takes data frame and creates addr string and queries for lat long coordinates."""
    LAT_store = []
    LONG_store = []

    for index in range(0,len(df)):
        
        #create address string
        addr  = df['City'].iloc[index] + " " + df['State'].iloc[index] + " " + df['CountyName'].iloc[index] + " " + str(df['RegionName'].iloc[index])
        try:
            geo_addr = do_geocode(addr)
            LAT = geo_addr.latitude
            LONG= geo_addr.longitude
            
        except:
            #if null error occur due to address not found, store the null objects
            LAT = None
            LONG = None
        
        print(LAT,LONG)    
        LAT_store.append(LAT)
        LONG_store.append(LONG)
    
    df["LAT"] = LAT_store
    df["LONG"] = LONG_store
    
    return df
    
df = pd.read_csv(r'C:\Users\Alan\Downloads\NY_ZILLOW_RE_PRICE_BY_ZIP.csv')

geocode_df = geo_converter(df)

geocode_df.to_csv('GEOCODE_NY_output_2.csv')