#!/usr/bin/env python
# coding: utf-8

from datetime import datetime
import pytz


from libdvr.zap import the_show
from libdvr.titan_classes import clean_string, run_at, init_dvr


init_dvr()


def record_the_show(station, start_time):
    my_show = the_show(station, start_time)
    dur_seconds = my_show['length'].values[0]
    station = my_show['vchan'].values[0]
    station = f'v{station}'
    a = my_show['start'].values[0]
    a1 = a.astype('datetime64[us]').astype(datetime) 
    b1 = a1.astimezone() 
    title = my_show['title'].values[0]
    episode = my_show['sub-title'].values[0]
    now = datetime.now()
    local_timezone = now.astimezone().tzinfo
    local_datetime = b1.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    at_time = local_datetime.strftime('%Y%m%d%H%M')
    name_of_recording = f'{title}_{episode}_{station}_{at_time}'
    clean_name_of_recording = clean_string(name_of_recording)
    clean_name_of_recording = f'{clean_name_of_recording}.ts'
    run_at(clean_name_of_recording, at_time, dur_seconds, station)
    return my_show


# my_show = record_the_show('11.1', '2345')


# record_the_show('13.1', '2240')


my_days=['Mon','Tue','Wed','Sat']


from datetime import date

def is_today_needed(my_days):
    today = date.today()
    today_weekday = today.strftime('%a')  # Get today's weekday as abbreviated string (e.g., 'Mon')
    if today_weekday in my_days:
        print("Today is one of the specified days.")
        return True
    else:
        print("Today is not one of the specified days.")
        return False


import pandas as pd
df = pd.read_csv('/home/tony/.favorite_tv', sep=',') 

print(df)


dict_without_index = df.to_dict('records')


dict_without_index


for d in dict_without_index:
    # print(d)
    station = str(d['station'])
    start = str(d['start'])
    my_show = record_the_show(station, start)
    print(my_show['title'].values[0])




