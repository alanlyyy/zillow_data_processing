import pandas as pd
from geo_coder import my_geocoder

#upload zillow data
df = pd.read_csv('Zip_Zhvi_AllHomes.csv')

user_input = input("Please select type the abbreviation of state wanted ( CA, NY, W ... ) : ")

try:
    #filter by user selected state
    mask = df['State'] == user_input

    filtered_city = df.loc[mask]

except:
    print("State is incorrect")
    quit()

column_mask = []

for index in range(0,9):
    column_mask.append(index)

#get the last 24 months
for index in range(len(filtered_city.columns) -40,len(filtered_city.columns)):
    column_mask.append(index)

#extract first several columns for address information and last 24 months
filtered_city = filtered_city.iloc[:,column_mask]

#filter state data by zipcode data
#zip_mask = (filtered_city['RegionName'] < 95000) & (filtered_city['RegionName'] > 94200)
#filtered_city = filtered_city.loc[zip_mask]

#calculate 24 month moving averages for past 6 months
filtered_city['24_moving_avg_previous_1'] = filtered_city.iloc[:,19:43].sum(axis=1)/24
filtered_city['24_moving_avg_previous_2'] = filtered_city.iloc[:,20:44].sum(axis=1)/24
filtered_city['24_moving_avg_previous_3'] = filtered_city.iloc[:,21:45].sum(axis=1)/24
filtered_city['24_moving_avg_previous_4'] = filtered_city.iloc[:,22:46].sum(axis=1)/24
filtered_city['24_moving_avg_previous_5'] = filtered_city.iloc[:,23:47].sum(axis=1)/24
filtered_city['24_moving_avg_current'] = filtered_city.iloc[:,24:48].sum(axis=1)/24

#calculate the change in price for the 2 moving averages
filtered_city['prev1_DELTA_MOVING_AVG'] = filtered_city['24_moving_avg_previous_2'] - filtered_city['24_moving_avg_previous_1']
filtered_city['prev1_DELTA_MOVING_AVG_%_Change'] = (filtered_city['prev1_DELTA_MOVING_AVG']/filtered_city['24_moving_avg_previous_1'])*100

filtered_city['prev2_DELTA_MOVING_AVG'] = filtered_city['24_moving_avg_previous_3'] - filtered_city['24_moving_avg_previous_2']
filtered_city['prev2_DELTA_MOVING_AVG_%_Change'] = (filtered_city['prev2_DELTA_MOVING_AVG']/filtered_city['24_moving_avg_previous_2'])*100

filtered_city['prev3_DELTA_MOVING_AVG'] = filtered_city['24_moving_avg_previous_4'] - filtered_city['24_moving_avg_previous_3']
filtered_city['prev3_DELTA_MOVING_AVG_%_Change'] = (filtered_city['prev3_DELTA_MOVING_AVG']/filtered_city['24_moving_avg_previous_3'])*100

filtered_city['prev4_DELTA_MOVING_AVG'] = filtered_city['24_moving_avg_previous_5'] - filtered_city['24_moving_avg_previous_4']
filtered_city['prev4_DELTA_MOVING_AVG_%_Change'] = (filtered_city['prev4_DELTA_MOVING_AVG']/filtered_city['24_moving_avg_previous_4'])*100

filtered_city['prev5_DELTA_MOVING_AVG'] = filtered_city['24_moving_avg_current'] - filtered_city['24_moving_avg_previous_5']
filtered_city['prev5_DELTA_MOVING_AVG_%_Change'] = (filtered_city['prev5_DELTA_MOVING_AVG']/filtered_city['24_moving_avg_previous_5'])*100


#convert lat long coordinates for the dataset
Geo_Converted = my_geocoder(filtered_city).geo_converter()

fileName = user_input + '__''Zip_Zhvi_AllHomes_filtered_output.csv'

filtered_city.to_csv(fileName)
