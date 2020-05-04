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
for index in range(len(NY_cities.columns) -25,len(filtered_city.columns)):
    column_mask.append(index)

#extract first several columns for address information and last 24 months
filtered_city = filtered_city.iloc[:,column_mask]

#filter New york city data
zip_mask = (filtered_city['RegionName'] < 11500) & (filtered_city['RegionName'] > 10000)
filtered_city = filtered_city.loc[zip_mask]

#calculate 24 month moving averages for previous month and current month
filtered_city['24_moving_avg_previous'] = filtered_city.iloc[:,9:33].sum(axis=1)/24
filtered_city['24_moving_avg_current'] = filtered_city.iloc[:,10:34].sum(axis=1)/24

#calculate the change in price for the 2 moving averages
filtered_city['DELTA_MOVING_AVG'] = filtered_city['24_moving_avg_current'] - filtered_city['24_moving_avg_previous']
filtered_city['DELTA_MOVING_AVG_%_Change'] = (filtered_city['DELTA_MOVING_AVG']/filtered_city['24_moving_avg_previous'])*100

#convert lat long coordinates for the dataset
Geo_Converted = my_geocoder(filtered_city).geo_converter()

fileName = 'Zip_Zhvi_AllHomes_filtered_output.csv'

filtered_city.to_csv(fileName)
