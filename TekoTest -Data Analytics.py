#Note: I had learnt a crash course quite a long time ago and haven't used it until now. After getting the test from HR,
# I had tried to use everything left in my head with the support from Google to complete the test. From my perception, my result below
# is more about exploratory data analysis. My approach to this problem follows these steps: clean data ( duplicate,
# illogical, null values with logic with conditions) and visualization. I try to plot the data as histogram to see the
# distribution. After that I plot some fields which are trip distance, trip duration, total amount  over time and vendors.

# 1. import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

# 2. load data and check top 20 rows
data = pd.read_csv("nyc_taxi_data_2014.csv")
print(data.head(20))

#3. check data info -> convert pick up/dropoff datetime from object to datetime
data.info()
data['pickup_datetime']=pd.to_datetime(data['pickup_datetime'])
data['dropoff_datetime']=pd.to_datetime(data['dropoff_datetime'])

#4. eliminate duplicate values
data = data.drop_duplicates()

#5. check null value and eliminate null values
data.isnull().sum().sort_values(ascending=False)
#there are total nearly 15million records, 7603464 record with null store_and_fwd_flag -> need to recheck before drop the data
# I found out that null store and fwd flag happens for VTS vendor only. However I don't understand the meaning of
# store_and_fwd_flag

#6. 145 null records in dropoff_longitute and dropoff_latitude -> the number of null value is small (145)
# -> eliminate null value
data=data.dropna(subset =['dropoff_longitude','dropoff_latitude'])

#7. check nonnegative value
data.describe()
#-> all passenger count, distance, fare mount, surchage etc. have positive value

#8. clean up illogical logic. exp: pickup_datetime > dropoff_Datetime
data= data[data.pickup_datetime < data.dropoff_datetime]
#since I don't know abt the capacity of taxi, the limit speed, limit distance of NYC cities -> dont know rule to set

#9. Add Year, Month, Week, Day, Hour, trip_duration to the data
data['pickup_datetime']=pd.to_datetime(data['pickup_datetime'])
data['Day']=data['pickup_datetime'].dt.weekday
data['Week']=data['pickup_datetime'].dt.week
data['Month']=data['pickup_datetime'].dt.month
data['Year']=data['pickup_datetime'].dt.year
data['Hour']=data['pickup_datetime'].dt.hour

data['trip_duration']=data['dropoff_datetime'] - data['pickup_datetime']
data['trip_duration'].describe()
data['trip_duration']=data['trip_duration'].dt.total_seconds()

data['trip_duration'].dtype
data['trip_duration']=data['trip_duration'].astype('int64')

#10. Plot scatter plot between trip_duration and trip_distance
plt.figure(figsize=(10,10))
plt.scatter( data["trip_distance"],data["trip_duration"])
plt.xlabel('trip_distance')
plt.ylabel('trip_duration')
plt.show()
#-> abnormal distribution. Some records with very short distance but long time. Why?. Is it because of waiting time in congestion
#or other reasons. The longest duration is 13 days, which is impossible for a taxi drive. In reality, the taxi trip duration
# that is greater than 1 day, is already abnormal
# These record could be outlier (doesn't make sense to the data) -> need to be drop out.
# the threshold to detect outlier is 100.000second (~27h). Another way to detect outlier, check z score. IF the value is
# out of range (-3z,3z) , these value can be treated as outlier

#11. plot taxi demand & time (Week, Day, Hour)
plt.figure(figsize=(12,8))
sns.countplot(x="Hour", data=data)
plt.show()
# interm of hour -> the highest demand time are from 18h to 23h. The lowest demand time are between 4-5h am

#in term of day
plt.figure(figsize=(12,8))
sns.countplot(x="Day", data=data)
plt.show()
#- > Day have value from 0 to 6, while 0 is sunday and 6 is saturday. The demand for taxi drive is quite
# even from Monday to Sunday. The highest demand during the week is day from Tuesday to Thursday (around 2.500.000 drives).
# the lowest demand is on Monday (around 1.700.000)

#in term of month -> there are only 2 months which are January and February in dataset
# -> Since the cycle is small, I don't want to plot these info

# 12. define unique vendors
unique_vendors1 = data.vendor_id.unique()
#  vendor_id -> there are 2 uniques value for vendor_id which are "CMT" and "VTS"

#13. create pivot table to see the number of drivers, revenue from each vendor
#no of drive
a1=data.pivot_table(index='vendor_id',columns='Week',values='total_amount',aggfunc='count')
# sum of total amount
a2=data.pivot_table(index='vendor_id',columns='Week',values='total_amount',aggfunc=np.sum)
# sum of trip distance
a3=data.pivot_table(index='vendor_id',columns='Week',values='trip_distance',aggfunc=np.sum)

#14. plot histogram of trip_distance
plt.hist(data['trip_distance'],bins ='auto',range=[0,20], alpha=0.5,rwidth=0.85)
#-> abnormal distribution, there are some distance with very high peak, the area is not smooth. The range step are quite even
#-> hypothesis: there are 2 kinds of distributions here and can be different for each vendor

#15. break down histogram of trip distance by vendor_id
#for vendor_id ='VTS'
b2= data[data['vendor_id']=='VTS']
fig2=plt.hist(b2['trip_distance'],bins ='auto',range=[0,20], alpha=0.5,rwidth=0.85,color='#0504aa')
fig2
#the distribution of this vendor has smooth function. The distance are shown in continuous value. The coule be a policy that
# the speedometer change continuously.

#for vendor_id = 'CMT'
b1= data[data['vendor_id']=='CMT']
fig1=plt.hist(b1['trip_distance'],bins ='auto',range=[0,20], alpha=0.5,rwidth=0.85,color='#0504aa')
fig1
#the distribution of this vendor is step function, since the step range is quite even. There is a hypothesis that this vendor's distance policy
# follow step function. For example, for each 500m, the speedometer will change one time.


# 16. Plot no of drive for each vendor in the same plot
groupbymonth = data.groupby(by =['vendor_id','Week']).count()
unique_vendors = data.vendor_id.unique()
for vendor in unique_vendors:
    week_df = groupbymonth.loc[(vendor, )]
    plt.plot(week_df.index, week_df.pickup_datetime, label=vendor)

plt.legend(loc=2, ncol=2)
plt.xlabel("Week")
plt.ylabel("Count By Week")
plt.show()
#Insight: WHy there is no data logged for Week 8,9 with vendor "CMT" and no data logged for Week 8 for vendor "VTS". The
# system has some problem then there is no data logged or another reason? Week 9 is a partial week so the data is small
# to evaluate. Another hypothesis is the data updated for VTS is realtime while the data updated for CMT vendor is offline
# (for example: at the end of the week)
# VTS has higher number of drive rather than CMT vendor. Both raises at week 2 and then drop significantly by week 6 for CMT and
# by week 7 for VTS. With vendor = CMT, Why it drops until week 6 and recover after that. However, for vendor VTS,
# the number of drive drop until week 7 and increase again.
# what's happened between week 3 and week 6 (from 19/01 - 03/02/2014) in NYC. WHy demand is so low? Hypothesis 1:
# Because holiday, people don't have demand or hypothesis 2: maybe there is a strike during these weeks -> drivers don't work

#17. Plot total amounts of each vendor
groupbymonth1 = data.groupby(by =['vendor_id','Week']).sum()
unique_vendors1 = data.vendor_id.unique()
for vendor in unique_vendors1:
    week_df = groupbymonth1.loc[(vendor, )]
    plt.plot(week_df.index, week_df.total_amount, label=vendor)

plt.legend(loc=2, ncol=2)
plt.xlabel("Week")
plt.ylabel("Total Amount")
plt.show()
#Insight:-> the shape total amount lines are quite the same as the shape of no of drive" lines. IT can be inferred that the taxi rate of
# both taxi vendors are similar.

#18. plot histogram of passenger of each vendor
sns.countplot(x="passenger_count", data=data[data["vendor_id"] == 'CMT'])
sns.countplot(x="passenger_count", data=data[data["vendor_id"] == 'VTS'])
# Insight: Since the passengers per drive of CMT vendor range from 1 to 4. This is inferred that Cars of CMT vendor have maximum
# 4 seats while cars of VTS can have maximum 6 seats. The number of trips that contain 5-6 people are quite high (around 180.000)
#It is can inferred that VTS has bigger car than CMT and VTS is quite popular among group.

#19. plot passenger count of each vendor
groupbymonth3 = data.groupby(by =['vendor_id','Week']).sum()
unique_vendors1 = data.vendor_id.unique()
for vendor in unique_vendors1:
    week_df = groupbymonth3.loc[(vendor, )]
    plt.plot(week_df.index, week_df.passenger_count, label=vendor)

plt.legend(loc=2, ncol=2)
plt.xlabel("Week")
plt.ylabel("Passenger Count")
plt.show()
#Insight: after plotting, it is obviously shown that the passenger of VTS is much higher than the passenger of CMT.
# The reason could be the higher capacity of VTS cars, which is more suitable for big groups.

