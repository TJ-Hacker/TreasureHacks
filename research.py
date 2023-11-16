# Notes for this python file

""""

The goal for this is to analyze population density, break this csv down to only contain information for brooklyn, bronx, staten island, queens and manhattan

"""

import pandas as pd
#import matplotlib.pyplot as plt
# Source: https://www.fourfront.us/data/datasets/us-population-density/

"""# Note: This code below created a new output.csv file which contains mostly all NYC zipcodes, will be parsed later in the code again 
# Define the path to the input CSV file and the values to match in the 5th column
input_csv_file = "pop.csv"
cities_to_match = ['Brooklyn', 'New York', 'Queens', 'Staten Island', 'Bronx']  # Add all the values you want to match # Queens according to the database has #multiple cities so we needed a country value 
county_value = 'Queens'
# Read data
df = pd.read_csv(input_csv_file)

# Filter the rows based on the condition in the 5th column
filtered_df = df[(df['City'].isin(cities_to_match)) | (df['County'] == county_value)]

output_csv_file = "output.csv"

filtered_df.to_csv(output_csv_file, index=False)
"""
# Filter again by state (some cities can be named twice )

"""input_csv_file = "output.csv"
df = pd.read_csv(input_csv_file)
filtered_df = df[df['St'] == 'New York']
filtered_df.to_csv('nyc_zipcodes.csv', index=False) # create final list with all the NYC zipcodes
"""

# NEW CSV FILE NAME: nyc_zipcodes.csv (Contains, Brooklyn, Queens, Manhattan (New York), Bronx and Staten Island)



# RESEARCH DOWN HERE

#lat = 40.64509741769572
#long = -73.97994976081495
# ideally should get zipcode 11218
# round it to the nearest 2th decimal


# Round down the latitude and longitude to two decimal places
#rounded_lat = int(lat * 100) / 100
#rounded_long = int(long * 100) / 100

#print(rounded_lat,rounded_long)

#nycInfo = pd.read_csv('nyc_zipcodes.csv')
#filtered_row = nycInfo[(nycInfo['lat'].apply(int) == rounded_lat * 100) & (nycInfo['long'].apply(int) == rounded_long * 100)]
#result = filtered_row['Zip']
#print(result)
#result = filter_row['Zip']

# Test - 2: Get the population density based on the zipcode
#zip  = 10011


#density = nycInfo.query(f"Zip=={zip}")["density"].iloc[0] # iloc - access the first element in this series 
#print(density)
#print(type(density)) # returns a float

# MAP OUT THE HIGHEST DENSITY


#print(nycInfo['density'].max())
#print(((nycInfo['density'].max() - nycInfo['density'].median())/2)-nycInfo['density'].max())
#print(nycInfo['density'].median())
#print(nycInfo['density'].min())
#print(8398.75/2)

# REFER TO THESE MEASUREMENTS FOR THE POPULATION DENSITY DATA AND THE RISK ALGORITHM

# MaxL 56520.9
# 3rd Quartile: 32459.8
#Median: 8398.75
# 2nd quartile: 4199.37
# Min: 0

# PART TWO OF THE PROGRAM 

""""
GRAB PARKING METER SPOT DATA!

- First get the original CSV file and only take the latitude and longitude data for time complexity
- Delete the original CSV file (parkingmeters.csv)
"""

# Source: https://data.cityofnewyork.us/Transportation/Parking-Meters-Locations-and-Status-Map-/mvib-nh9w

"""meters = pd.read_csv('parkingmeters.csv')

#data = meters.groupby("Borough")
#print(data)

selected_columns = ['Meter_Hours', 'Latitude', 'Longitude', 'Pay By Cell Number']
filtered_df = meters[selected_columns]
filtered_df.to_csv('parkingmeter.csv', index=False) # save as new csv file"""


"""
Next part of project:
Get veichile collision data (NYC open data) and find the areas (zipcodes) with the most amount of crash crashes/vehicle issue and add a possible shading over it / warn the users about the risk

Collision Data: (https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/explore)

Logic Part:

For each zipcode, loop through it and count the value_count() of each insident, murders are worth 2x more than injuries. (Every murder add +2 to score, every injury add +1 to the score), map out and create an algorithm that sees the risk of the zipcode (in terms of car crashing!)
    - All murders add 2 to the score while all injured add 1 to the score, as  murders worse
    - Create a new dataframe labeled Score (higher score the worst)
    - Take first, second, third and fourth quartile data for each zipcode
    - For this program as of now only have the worst 10% (around 25 zipcodes) being used for the program
"""

#motorCrash = pd.read_csv('motorcrashes.csv')
#crashData = motorCrash.fillna(0) # replace all the null values with the 0 instead

# delete all column where the zipcode is equal to 0
#crashData = crashData[crashData['ZIP CODE'] != 0] 
#crashData.to_csv('crashes.csv', index=False) # NEW CSV FILE

#crashData = pd.read_csv('crashes.csv')
# group the data and sum using aggregate 
"""
zipcode_counts = crashData.groupby('ZIP CODE').agg({
    'NUMBER OF PERSONS INJURED': 'sum',
    'NUMBER OF PERSONS KILLED': 'sum',
    'NUMBER OF CYCLIST INJURED': 'sum',
    'NUMBER OF CYCLIST KILLED': 'sum',
    'NUMBER OF MOTORIST INJURED': 'sum',
    'NUMBER OF MOTORIST KILLED': 'sum'
}).reset_index()"""

#print(zipcode_counts)

# MAKE ZIPCODE COUNTS HERE A NEW CSV FILE 
# 235 CHOICES, ADDS ALL THE DATA FOR EACH ZIPCODE, LESS TIME COMPLEXITY
#zipcode_counts.to_csv('collisions.csv', index=False)


# PART THREE OF PROGRAM ADD THE VALUE OF COLLISION DATA AS A NEW DATAFRAME REFER TO LINE 116 FOR ALGORITHM LOGIC 
#df = pd.read_csv('collisions.csv')

# refer to line 115 - create a new dataframe
#df = df.drop(index=0) # drop the first index as it has no zipcode correlated 
#df['score'] = (df['NUMBER OF PERSONS INJURED'] + df['NUMBER OF CYCLIST INJURED'] + df['NUMBER OF MOTORIST INJURED'] + 2 * (df['NUMBER OF PERSONS KILLED'] + df['NUMBER OF CYCLIST KILLED'] + df['NUMBER OF MOTORIST KILLED']))


#df.to_csv('crashDATA.csv', index=False) # NEW DATA WILL BE USED 

dataFrame = pd.read_csv('crashDATA.csv')
"""
Get quartile for the risk of the ZIPCODE being hit
Max Number - 400
Quartile 1 - 252
Quartile 2 (Median) - 104.124
Quartile 3 - 52
Min - 0

print(dataFrame['score'].max())
print((dataFrame['score'].max() + dataFrame['score'].mean()) / 2) #  Q1
print(dataFrame['score'].mean())
print((dataFrame['score'].min() + dataFrame['score'].mean()) / 2) #  Q3
print(dataFrame['score'].min())

"""

