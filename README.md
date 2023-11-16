# TreasureHacks
Our repo for the 2022 TreasureHacks Hackathon

View the devpost: https://devpost.com/software/parkr-97wdqu

View the demo video: https://youtu.be/IE5Ta5ngLik


As of 10/28/2023 we are starting the project again!


# POST HACKATHON

1) Reworked the whole programming for time efficiency, using less libraries and using csv files to get data instead of the reverse geocoder feature / using openAI to find population denisty (DONE)
2) Re-worked the risk algorithm  (DONE)
3) Cache the parkingmeters.csv data in order to save it into the JavaScript, so we don't have to reload the data over and over. Now the program displays marking data information (DONE)
4) Analyze veichile collision data in NYC and create zones where it's most risky to drive based on zip-code (in progress)
5) Add a system wheres users have to submit an image of the parking spot! (so make it more responsive for people on desktop) - push through Flask database and push it back to the javascript so image can be shown when users hover over it (in progress)
  2a) Note for side: use computer vision and AI to determine if this is a legitimate picture


# TESTING
1) Tested the program on my phone, need to work on responsiveness more with celluar device.
![parkr1](https://github.com/TJ-Hacker/TreasureHacks/assets/102444808/691a2a57-6169-496e-bddd-28f5329af34a)
