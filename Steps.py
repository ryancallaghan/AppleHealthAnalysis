import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, datetime, timedelta as td
import pytz


#import CSV file with steps data
steps = pd.read_csv(r'C:\Users\ryanm\AppData\Local\Programs\Python\Python310\Final Project\HKQuantityTypeIdentifierStepCount.csv', encoding='cp1252')

#setup time conversion into useable format
convert_tz = lambda x: x.to_pydatetime().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Eastern'))
get_year =lambda x: convert_tz(x).year
get_month = lambda x: '{}-{:02}'.format(convert_tz(x).year, convert_tz(x).month)
get_date = lambda x: '{}-{:02}-{:02}'.format(convert_tz(x).year, convert_tz(x).month, convert_tz(x).day)
get_day =lambda x: convert_tz(x).day
get_hour =lambda x: convert_tz(x).hour
get_minute =lambda x: convert_tz(x).minute
get_day_of_week =lambda x: convert_tz(x).weekday()

#convert time into useable format
steps['startDate'] = pd.to_datetime(steps['startDate'])
steps['year'] = steps['startDate'].map(get_year)
steps['month'] = steps['startDate'].map(get_month)
steps['date'] = steps['startDate'].map(get_date)
steps['day'] = steps['startDate'].map(get_day)
steps['hour'] = steps['startDate'].map(get_hour)
steps['weekdate'] = steps['startDate'].map(get_day_of_week)

#add all steps for each date to have 1 step number per date 
steps_by_date= steps.groupby(['date'])['value'].sum().reset_index(name='Steps')

#write this new data into a new file
steps_by_date.to_csv("steps_by_date.csv", index=False)

#plot moving average of steps 
steps_by_date['RollingMeanSteps'] = steps_by_date.Steps.rolling(window=10, center=True).mean()
steps_by_date.plot(x='date', y='RollingMeanSteps', title= 'Daily step counts rolling mean over 10 days', figsize=[10, 6])
plt.show()

#collect average steps per day of the week
steps_by_date['date'] = pd.to_datetime(steps_by_date['date'])
steps_by_date['weekdate'] = steps_by_date['date'].dt.weekday

#plot average steps per day of the week
data = steps_by_date.groupby(['weekdate'])['Steps'].mean()
fig, ax = plt.subplots(figsize=[10, 6])
ax = data.plot(kind='bar', x='day_of_week')
n_groups = len(data)
index = np.arange(n_groups)
opacity = 0.75
ax.yaxis.grid(True)
plt.suptitle('Average Steps by Day of the Week', fontsize=16)
weekdate_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
plt.xticks(index, weekdate_labels, rotation=45)
plt.xlabel('Day of Week', fontsize=12, color='red')
plt.show()

#collect average steps per month & plot
steps_by_month= steps.groupby(['month'])['value'].sum().reset_index(name='Steps')
steps_by_month.to_csv("steps_by_month.csv", index=False)
steps_by_month['Monthlysteps'] = steps_by_month.Steps.rolling(window=3, center=True).mean()
steps_by_month.plot(x='month', y='Monthlysteps', title= 'Average Step counts in 3 month intervals', figsize=[10, 6])
plt.show()


