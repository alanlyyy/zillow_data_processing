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

    for index in range(0,len(CA_filtered)):
        
        #create address string
        addr  = CA_filtered['RegionName'].iloc[index] + " " + CA_filtered['State'].iloc[index] + " " + CA_filtered['CountyName'].iloc[index]
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
    

#read the csv
housing_df = pd.read_csv('City_Zhvi_SingleFamilyResidence.csv', sep=',', header= 0)

#get the first five datapoints
print(housing_df.head())

#get all CA cities subset
CA_cities = housing_df['StateName'] == 'CA'

#filter only CA cities
CA_cities = housing_df.loc[CA_cities]
#print(CA_cities.head())


#----------method 1 of extracting specific columns from DF--------------
#extract specific columns
column_mask = []

for index in range(0,8):
    column_mask.append(index)

#get the last 24 months
for index in range(len(CA_cities.columns) -24,len(CA_cities.columns)):
    column_mask.append(index)

CA_filtered = CA_cities.iloc[:,column_mask]
print(CA_filtered.head())

#---------method 2 of extracting specific columns from DF--------------
#get the last 24 months couple months of 2020
#column_identity = CA_cities.iloc[:,0:8]
#ca_time_filter = CA_cities.iloc[ :,-24:len(CA_cities.columns):1]
#CA_filtered = pd.concat([column_identity,ca_time_filter], axis = 1)
#print(CA_filtered.head())

CA_filtered['6_moving_avg_6mo'] = CA_filtered.iloc[:,8:14].sum(axis=1)/6
CA_filtered['12_moving_avg_6mo'] = CA_filtered.iloc[:,14:20].sum(axis=1)/6
CA_filtered['18_moving_avg_6mo'] = CA_filtered.iloc[:,20:26].sum(axis=1)/6
CA_filtered['24_moving_avg_6mo'] = CA_filtered.iloc[:,26:32].sum(axis=1)/6
CA_filtered['3_moving_avg_3mo'] = CA_filtered.iloc[:,8:11].sum(axis=1)/3
CA_filtered['6_moving_avg_3mo'] = CA_filtered.iloc[:,11:14].sum(axis=1)/3
CA_filtered['9_moving_avg_3mo'] = CA_filtered.iloc[:,14:17].sum(axis=1)/3
CA_filtered['12_moving_avg_3mo'] = CA_filtered.iloc[:,17:20].sum(axis=1)/3
CA_filtered['15_moving_avg_3mo'] = CA_filtered.iloc[:,20:23].sum(axis=1)/3
CA_filtered['18_moving_avg_3mo'] = CA_filtered.iloc[:,23:26].sum(axis=1)/3
CA_filtered['21_moving_avg_3mo'] = CA_filtered.iloc[:,26:29].sum(axis=1)/3
CA_filtered['24_moving_avg_3mo'] = CA_filtered.iloc[:,29:32].sum(axis=1)/3

print(CA_filtered.head())

CA_filtered.to_csv('SFR_CA_output_2.csv')
