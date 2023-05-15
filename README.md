# AppleHealthAnalysis
This code can be used to upload health information from an apple watch, and analyze key metrics such as heart rate, steps, and workout data.

First you need to export your health information from the apple health app.
On your iphone go to Health>Your Account> Export All Health Data.
the export.xml path location is what is used in this code.
In addition for the workout specific information, I used the "Health Auto Export" to get the data into a csv file, as apple does not have a friendly way to organize this health data when exported.
Use apple-health-data-parser.py to import 

Once parsed, 
Link  heartrate csv files in heartrate.py
Link Workout csv file in Final Project.py
Link Steps csv file in Steps.py

Use this code to discover more data analytics and help get insight on workout data.
