# teko-test
This repository is the solution for Data Analytics Test at Teko. The dataset includes taxi drives in NYC in 2014 of 2 vendors,
which are CMT and VTS. My repository is a kind of exloratory data analysis for this dataset. I started with cleaning dataset and then 
visualize the data. 

Which data I have cleaned: 
- Duplicate
- null value in dropoff_latitude and dropoff_longitude
- records with pick up time > dropoff time
- check non-negative and eliminate non-negative values in passenger counts, time and all kind of amounts
- I suppose to check the maximum trip distance and trip duration to eliminate some impossible cases. However I don't know the policies
of NYC taxi, whether they have a cap on distance and duration. THere are some records with very short distance but the trip duration is 
up to 13 days (which is quite abnormal for a taxi drive). But I don't know this data is suppose to correct or not, need to look at how 
we collect the data and the policies of the taxi. 
- There are around 7million null record in store_and_fwd_flag. Since in total we have 15million records, if we eliminate all null value 
in store_and_fwd_flag, it means we reduce half of population size. This could lead to unbalanced dataset or the sample can't reflect true 
meaning of population. Because my visualization doesn't relate to this field, I think it is ok to keep this column. Actually when I looked 
at null value of store_and_fwd_flag, all of them are from vendor VTS. There could be a question about how we collect the data and what's 
happened to VTS system.

All my hypothesis 
- VTS has higher number of drive, total amount and passengers if the way we collect data is correct
- VTS has bigger car with higher capacilities (maximum 6 seats) rather than CMT (maximum 4 seats)
- VTS has continuous speedometer whilte CMT has step - function speedometer (for example, each 500m speedometer will change again)
- No data logged for CMT in week 8,9 and no data logged for VTS in week 8. CMT and VTS system have some problem or we missed data in W8,9
- There is a significant drop in taxi drive from week 4 to week 6. My hypothesis is that there was a strike during these week so drivers
don't work. 
- Week 9 is partical week, don't have enough data to evaluate with other week
- Highest demand for taxi drive is between 18h-23h, the lowest demand is between 4-5am
- The demand over the week doesn't fluctuate significantly. THe highest demand range between Tuesday and Thursday while Monday has the lowest
demand.
