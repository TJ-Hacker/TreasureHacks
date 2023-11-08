# TreasureHacks
Our repo for the 2022 TreasureHacks Hackathon
View the devpost: https://devpost.com/software/parkr-97wdqu


As of 10/28/2023 we are starting the project again!


# POST HACKATHON

1) Reworked the whole programming for time efficiency, using less libraries and using csv files to get data instead of the reverse geocoder feature / using openAI to find population denisty.
3) Cache the parkingmeters.csv data in order to save it into the JavaScript, so we don't have to reload the data over and over
4) Add a system wheres users have to submit an image of the parking spot! (so make it more responsive for people on desktop) - push through Flask database and push it back to the javascript so image can be shown when users hover over it.
  2a) Note for side: use computer vision and AI to determine if this is a legitimate picture
