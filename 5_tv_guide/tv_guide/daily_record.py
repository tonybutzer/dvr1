#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from datetime import datetime
from datetime import date
import pytz


from libdvr.zap import the_show
from libdvr.titan_classes import clean_string, run_at, init_dvr, record_the_show


init_dvr()


def is_today_needed(my_days):
    today = date.today()
    today_weekday = today.strftime('%a')  # Get today's weekday as abbreviated string (e.g., 'Mon')
    if today_weekday in my_days:
        print("Today is one of the specified days.")
        return True
    else:
        print("Today is not one of the specified days.")
        return False


df = pd.read_csv('/home/tony/.favorite_tv', sep=',') 

print(df)

dict_without_index = df.to_dict('records')


for d in dict_without_index:
    # print(d)
    station = str(d['station'])
    start = str(d['start'])
    days = str(d['days'])
    if days.startswith('#'):
        break
    #my_show = record_the_show(station, start)
    my_days = days.split('-')
    if is_today_needed(my_days):
        #my_show = the_show(station, start)
        my_show = record_the_show(station, start)
        print(my_show['title'].values[0])
