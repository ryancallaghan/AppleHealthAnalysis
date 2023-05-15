import pandas as pd

#import CSV file with workout data
rhr = pd.read_csv(r'C:\Users\ryanm\AppData\Local\Programs\Python\Python310\Final Project\HKQuantityTypeIdentifierRestingHeartRate.csv', encoding='cp1252')

avgrhr= (rhr['value'].mean())
print ("Your resting heart rate is: ")
print (avgrhr);

hr=pd.read_csv(r'C:\Users\ryanm\AppData\Local\Programs\Python\Python310\Final Project\HKQuantityTypeIdentifierHeartRate.csv', encoding='cp1252')

mhr= (hr['value'].max())
print ("Your max heart rate is: ")
print (mhr);

hrr=mhr-avgrhr
print ("Your heart rate reserve is: ")
print (hrr)


