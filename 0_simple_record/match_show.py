#!/usr/bin/env python
# coding: utf-8

# %load chan_record
#!/usr/bin/env python

import pandas as pd
from datetime import datetime
from datetime import date
import pytz
import sys


from libdvr.zap import the_show, tv_df_make
from libdvr.titan_classes import init_dvr, record_the_show


init_dvr()


mdf = pd.read_csv('/home/tony/.match_tv', sep=',')


mdf


matches = mdf['match'].to_list()


df = tv_df_make()


import pandas as pd
from datetime import datetime, time, timedelta

# Assuming your DataFrame is named 'df' and contains the specified columns

now = datetime.now()
local_timezone = now.astimezone().tzinfo
    # now_aware = datetime.now(local_timezone)
    # now = now_aware

# Get today's date at 12:00 AM
today_start = datetime.combine(datetime.today(), time(0, 0))
#today_start = now
today_start = today_start.replace(tzinfo=local_timezone)


# Get today's date at 12:00 AM tomorrow
today_end = today_start + timedelta(days=1)
#today_end = datetime.combine(datetime.today(), time(17, 0))
today_end = today_end.replace(tzinfo=local_timezone)



# Filter the DataFrame based on the conditions
filtered_df = df[(df['start'] < today_end) & (df['stop'] > today_start)]

# Print the filtered results
print(filtered_df)


df = filtered_df
result_df = df[df['title'].str.contains('48')]


result_df


df = filtered_df

for match in matches:
    result_df = df[df['title'].str.contains(match)]
    for i, r in result_df.iterrows():
        station = r['vchan']
        tim = r['start']
        tim_str = tim.strftime("%H%M")
        record_the_show(station, tim_str)
    


#f.head()

