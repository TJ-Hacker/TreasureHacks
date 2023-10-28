# Notes for this python file

""""

The goal for this is to analyze population density, break this csv down to only contain information for brooklyn, bronx, staten island, queens and manhattan

"""

import pandas as pd
#import matplotlib.pyplot as plt


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

