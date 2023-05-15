import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, datetime, timedelta as td
import pytz

#seperate file for heart rate data & calculations
from heartrate import hrr

#import CSV file with workout data
wk = pd.read_csv(r'C:\Users\ryanm\AppData\Local\Programs\Python\Python310\Final Project\Workouts.csv', \
                        sep=',')

#convert time to useable format (via Vinayak Gaur (Medium.com))
convert_tz = lambda x: x.to_pydatetime().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Eastern'))
get_year =lambda x: convert_tz(x).year
get_month = lambda x: '{}-{:02}'.format(convert_tz(x).year, convert_tz(x).month)
get_date = lambda x: '{}-{:02}-{:02}'.format(convert_tz(x).year, convert_tz(x).month, convert_tz(x).day)
get_day =lambda x: convert_tz(x).day
get_hour =lambda x: convert_tz(x).hour
get_minute =lambda x: convert_tz(x).minute
get_day_of_week =lambda x: convert_tz(x).weekday()

#take out non running workouts & columns not being used 
run = wk[wk['Type'] == 'Running']
run = run.drop(['Step Count (count)', 'Swimming Stroke Count (count)', 'Swim Stoke Cadence (spm)', 'Flights Climbed (count)', 'Elevation Descended (ft)'
], axis=1)

#Parse out dates/times for analysis based on time
run['Start'] = pd.to_datetime(run['Start'])
run['year'] = run['Start'].map(get_year)
run['month'] = run['Start'].map(get_month)
run['date'] = run['Start'].map(get_date)
run['day'] = run['Start'].map(get_day)
run['hour'] = run['Start'].map(get_hour)
run['weekdate'] = run['Start'].map(get_day_of_week)

# fix cadence to steps per minute, not per second 
run['Step Cadence (spm)'] = run['Step Cadence (spm)']*60

#sort rows based on workout duration
run = run.sort_values('Duration', ascending=True)

# add heart rate zone column to workouts
conditions = [
    (run['Avg Heart Rate (bpm)'] <= 0.5*hrr),
    (run['Avg Heart Rate (bpm)']  > 0.5*hrr) & (run['Avg Heart Rate (bpm)']  <= hrr),
    (run['Avg Heart Rate (bpm)']  > hrr) & (run['Avg Heart Rate (bpm)']  <= 1.2*hrr),
    (run['Avg Heart Rate (bpm)']  > 1.2*hrr) & (run['Avg Heart Rate (bpm)']  <= 1.3*hrr),
    (run['Avg Heart Rate (bpm)']  > 1.3*hrr) & (run['Avg Heart Rate (bpm)']  <=1.5*hrr),
    (run['Avg Heart Rate (bpm)']  > 1.5*hrr)
    ]

# create a list of the values we want to assign for each heart rate zone
values = ['Resting', 'Aerobic Training', 'Fitness Training', 'Anaerobic Training', 'VO2 Max Zone', 'Dangerous']

# create a new column and assign values to each condition
run['zone'] = np.select(conditions, values)

#export manipulated csv file
print(run.to_string())
run.to_csv('workout_csv')
    
#seperate data based on heart rate zones
Resting= run[(run['zone'] == 'Resting')].value_counts(normalize=True)
AerobicTraining= run[(run['zone'] == 'Aerobic Training')].value_counts(normalize=True)
FitnessTraining= run[(run['zone'] == 'Fitness Training')].value_counts(normalize=True)
AnaerobicTraining= run[(run['zone'] == 'Anaerobic Training')].value_counts(normalize=True)
VO2Max= run[(run['zone'] == 'VO2 Max Zone')].value_counts(normalize=True)
Dangerous= run[(run['zone'] == 'Dangerous')].value_counts(normalize=True)

#creates histogram of # Active Calories burned per workout
plt.figure(figsize=(10,6), tight_layout=True)
bins = [100, 200, 300, 400, 500, 600, 700]
plt.hist(run['Active Energy (kcal)'], bins=bins, color=sns.color_palette('Set2')[2], linewidth=2)
plt.title('Histogram')
plt.xlabel('Active Energy (kcal)')
plt.ylabel('Count')
ax = sns.histplot(data=run, x='Active Energy (kcal)', bins=bins, color=sns.color_palette('Set2')[2], linewidth=2)
ax.set(title='Active Calories burned per workout', xlabel='Active Energy (kcal)', ylabel='Count')
plt.show()

#Scatterplot of average speed and step cadence
plt.figure(figsize=(10,6), tight_layout=True)
ax = sns.scatterplot(data=run, x='Avg Speed(mi/hr)', y='Step Cadence (spm)',   hue='zone', palette='Set1', s=60)
ax.set(xlabel='Avg Speed(mi/hr)', ylabel='Step Cadence (spm)')
ax.legend(title='Avg Speed and Step Cadence Correlation', title_fontsize = 12) 
plt.show()



#scatterplot of average speed and max heart rate 
plt.figure(figsize=(10,6), tight_layout=True)
ax = sns.scatterplot(data=run, x='Avg Speed(mi/hr)', y='Max Heart Rate (bpm)',   hue='zone', palette='Set2', s=60)
ax.set(xlabel='Avg Speed(mi/hr)', ylabel='SMax Heart Rate (bpm)')
ax.legend(title='How running speed affects heart rate', title_fontsize = 12) 
plt.show()

#scatterplot of heart rate zone and calories burned
plt.figure(figsize=(10,6), tight_layout=True)
ax = sns.boxplot(data=run, x='zone', y='Active Energy (kcal)', palette='Set2', linewidth=2.5)
ax.set(title='Heart Rate Zone and Calories Burned', xlabel='', ylabel='Active Energy (kcal)')
plt.show()



