import xml.etree.ElementTree as ET

import pandas as pd
from datetime import datetime, time


def tv_df_make():
    xml_file = '/home/tony/opt/dvr1/5_tv_guide/xmltv.xml'
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # create channel lookup table
    chans_list = []
    for chan_elem in root.findall('.//channel'):
        chan_dict = {}
        chan_dict['id'] = chan_elem.get('id')
        i=0
        for child_elem in chan_elem.findall('display-name'):
            #print (child_elem.text)
            tag=child_elem.tag+str(i)
            chan_dict[tag] = child_elem.text
            i += 1
        chans_list.append(chan_dict)
    CHAN_DF = pd.DataFrame(chans_list)
    CHAN_DICT = CHAN_DF.to_dict('records')
    CHAN_LOOKUP={}
    for rec in CHAN_DICT:
        CHAN_LOOKUP[rec['id']] = rec['display-name1']
    
    # Create a list to store dictionaries representing each book
    progr_list = []
    # Iterate through each <book> element
    for progr_elem in root.findall('.//programme'):
        progr_dict = {}
        progr_dict['start'] = progr_elem.get('start')
        progr_dict['stop'] = progr_elem.get('stop')
        progr_dict['channel'] = progr_elem.get('channel')
        #progr_dict['title'] = progr_elem.get('title')
    
        i=0
        for child_elem in progr_elem.findall('title'):
            # print (child_elem.text)
            tag=child_elem.tag
            progr_dict[tag] = child_elem.text
            i += 1
            
        for child_elem in progr_elem.findall('sub-title'):
            # print (child_elem.text)
            tag=child_elem.tag
            progr_dict[tag] = child_elem.text
            
        for child_elem in progr_elem.findall('length'):
            # print (child_elem.text)
            tag=child_elem.tag
            progr_dict[tag] = child_elem.text
    
        progr_list.append(progr_dict)
    pdf = pd.DataFrame(progr_list)
    pdf['vchan'] = pdf['channel'].map(CHAN_LOOKUP)
    pdf['start'] = pd.to_datetime(pdf['start'])
    pdf['stop'] = pd.to_datetime(pdf['stop'])
    pdf['vchan'] = pdf['vchan'].astype(float) 

    now = datetime.now()
    local_timezone = now.astimezone().tzinfo
    # print("Current timezone:", local_timezone)
    
    pdf['start'] = pdf['start'].dt.tz_convert(local_timezone)
    pdf['stop'] = pdf['stop'].dt.tz_convert(local_timezone)

    pdf['sub-title'] = pdf['sub-title'].fillna('ONE')
    pdf = pdf.sort_values(by='vchan')
    pdf['vchan'] = pdf['vchan'].astype(str) 
    pdf = pdf[['vchan', 'start', 'stop', 'title', 'sub-title', 'length']]

    return pdf
    

def return_whats_on():
    df = tv_df_make()

    now = datetime.now()
    local_timezone = now.astimezone().tzinfo
    now_aware = datetime.now(local_timezone)
    now = now_aware

# Filter DataFrame to find rows with 'now' between 'start' and 'stop'
    filtered_df = df[(df['start'] <= now) & (now <= df['stop'])]
    df = filtered_df
    df_no_duplicates = df.drop_duplicates() 

    sdf = df_no_duplicates


def get_datetime_for_today_at_time(time_str):
  """
  Gets the datetime object for today at the specified time.

  Args:
    time_str: A string representing the time in the format 'HHMM' (e.g., '1700').

  Returns:
    A datetime object representing today's date with the specified time.
  """
  try:
    hour = int(time_str[:2])
    minute = int(time_str[2:])
    today = datetime.today()
    return datetime.combine(today, time(hour, minute))
  except ValueError:
    raise ValueError(f"Invalid time format: {time_str}. Expected format: 'HHMM'")


def the_show(vchan, time_str):
    df = tv_df_make()
    df = df[df['vchan'] == vchan]
    
    now = datetime.now()
    local_timezone = now.astimezone().tzinfo
    datetime_today = get_datetime_for_today_at_time(time_str)
    aware_dt = datetime_today.replace(tzinfo=local_timezone) 
    now = aware_dt
    # print(now)
    adf = df[(df['start'] <= now)]
    adf = adf[(adf['stop'] > now)]
    return adf


    return sdf


def whats_on_filtered(fav_chans):
    #fav_chans = [11,13,46]

    sdf = return_whats_on()

    dfs=[]
    df = sdf
    for chan in fav_chans:
        vmatch = f'{chan}.'
        print(vmatch)
        fdf = df[df['vchan'].str.startswith(vmatch)]
        #print(fdf)
        dfs.append(fdf)

    bdf = pd.concat(dfs)
    return bdf
