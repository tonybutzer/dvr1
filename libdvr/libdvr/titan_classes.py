import os
import re
import xmltodict
import logging
import pytz

from zoneinfo import ZoneInfo
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

from libdvr.util import run_command
from libdvr.zap import the_show

def init_dvr():
    global TUNER_ID
    global TUNER_IP
    global RECORDINGS
    global DVR_HOME
    global logger
    
    load_dotenv()

    TUNER_ID = os.getenv('TUNER_ID')
    TUNER_IP = os.getenv('TUNER_IP')
    RECORDINGS = os.getenv('DVR_RECORDINGS')
    DVR_HOME = '/home/tony/DVR'
 
    # # LOGGING

    # Configure logging
    logging.basicConfig(
        filename="/home/tony/DVR/log/dvr.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Create a logger
    logger = logging.getLogger(__name__)

    # Log some messages
    logger.info("DVR application started.")
    return logger
    
def run_at(name, time, dur_seconds, vchan):
    global RECORDINGS
    global TUNER_IP
    cmd=f'echo curl -so {RECORDINGS}/{name} {TUNER_IP}:5004/auto/{vchan}?duration={dur_seconds}| at -t {time}'
    logger.info(cmd)
    print(cmd)
    run_command(cmd)


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path

def get_files_titan_tvpi():
    dir_path = '/home/tony/Downloads'
    res = os.listdir(dir_path)
    results = [i for i in res 
              if i.endswith('tvpi')]
    fresults = []
    for file in results:
        fresults.append(f'{dir_path}/{file}')
    return fresults


def get_files_titan_tvvi():
    dir_path = '/home/tony/Downloads'
    res = os.listdir(dir_path)
    results = [i for i in res 
              if i.endswith('tvvi')]
    fresults = []
    for file in results:
        fresults.append(f'{dir_path}/{file}')
    return fresults


def get_xml_tvvi(file):
    my_fields={}
    with open(file) as fd:
        doc = xmltodict.parse(fd.read())
    my_fields['title'] = doc['tv-viewer-info']['program']['program-title']
    a = doc['tv-viewer-info']['program']
    my_fields['episode'] = a.get('episode-title', 'One')
    my_fields['station'] = doc['tv-viewer-info']['program']['station']
    chan = my_fields['major'] = doc['tv-viewer-info']['program']['psip-major']
    minor = my_fields['minor'] = doc['tv-viewer-info']['program']['psip-minor']
    my_fields['duration'] = doc['tv-viewer-info']['program']['duration']
    #my_fields['title'] = doc['tv-program-info']['program']['program-title']
    my_fields['vchan'] = f'v{chan}.{minor}'

    now = datetime.now()
    future_time = now + timedelta(seconds=10)
    current_time = future_time.strftime('%Y%m%d%H%M')
    at_time = current_time
    print(at_time)
    my_fields['at_time'] = at_time

    return (my_fields)

def get_xml_tvpi(file):
    my_fields={}
    with open(file) as fd:
        doc = xmltodict.parse(fd.read())
    my_fields['title'] = doc['tv-program-info']['program']['program-title']
    a = doc['tv-program-info']['program']
    my_fields['episode'] = a.get('episode-title', 'One')
    my_fields['station'] = doc['tv-program-info']['program']['station']
    chan = my_fields['major'] = doc['tv-program-info']['program']['psip-major']
    minor = my_fields['minor'] = doc['tv-program-info']['program']['psip-minor']
    my_fields['duration'] = doc['tv-program-info']['program']['duration']
    #my_fields['title'] = doc['tv-program-info']['program']['program-title']
    my_fields['vchan'] = f'v{chan}.{minor}'

    at_time = make_at_time(a['start-date'], a['start-time'])


    # now = datetime.now()
    # future_time = now + timedelta(seconds=10)
    # current_time = future_time.strftime('%Y%m%d%H%M')
    # at_time = current_time
    # print(at_time)
    my_fields['at_time'] = at_time

    return (my_fields)

def t_schedule_record(a):
    station = a['station']
    ptitle = a['title']
    #etitle = a['episode-title']
    etitle = a.get('episode', 'One')
  
    at_time = a['at_time']
    print(at_time)

    name_of_recording = f'{ptitle}_{etitle}_{station}_{at_time}'
    clean_name_of_recording = clean_string(name_of_recording)
    clean_name_of_recording = f'{clean_name_of_recording}.ts'
    print(clean_name_of_recording)
    # process duration
    dur = a['duration']
    print(dur)
    dur_seconds = duration(dur)
    print(dur_seconds)
    print(at_time)
    vchan = a['vchan']
    print(vchan)
    run_at(clean_name_of_recording, at_time, dur_seconds, vchan)


def duration_to_hms(duration_str):
  """
  Converts a duration string (e.g., "02:45") to hours, minutes, and seconds.
  Args:
    duration_str: The duration string in the format "HH:MM" or "MM:SS".
  Returns:
    A tuple containing hours, minutes, and seconds as integers.
  """
  try:
    if ':' not in duration_str:
      raise ValueError("Invalid duration format. Expected 'HH:MM' or 'MM:SS'.")

    parts = duration_str.split(':')
    if len(parts) == 2:
      hours = int(parts[0]) if parts[0] else 0
      minutes = int(parts[1])
      seconds = 0
    elif len(parts) == 1:
      hours = 0
      minutes = int(parts[0])
      seconds = 0
    else:
      raise ValueError("Invalid duration format. Expected 'HH:MM' or 'MM:SS'.")

    seconds = (hours * 60 + minutes) * 60

    return hours, minutes, seconds

  except ValueError as e:
    print(f"Error: {e}")
    return None

def duration(dur):
    hours, minutes, seconds = duration_to_hms(dur)
    if seconds > 3600 * 2 - 1:
        seconds += 3600 + 1800 - 3
    return seconds


def examine_dates_titan(programs):
    for program in programs:
        print(program)
        t=TITAN(program)
        title = t.title()
        print(title)
        print(t.duration())
        print(t.start_date())
        print(t.start_time())
        #t.info()
    
        

# time = "Jun 2012 14:03:10 GMT"
# time = "20250111 21:00 GMT"


def convert_gmt_utc(date_str):
    time = date_str
    
    # parse to datetime, using %Z for the time zone abbreviation
    dtobj = datetime.strptime(time, '%Y%m%d %H:%M %Z')
    
    # ...so let's correct that:
    dtobj = dtobj.replace(tzinfo=timezone.utc)
    
    dtobj = dtobj.astimezone(ZoneInfo('US/Central'))
    a = dtobj

    at_time = a.strftime('%Y%m%d%H%M')
    # print(a.strftime('%Y%m%d%H%M'))
    # print(a.strftime('%Y %m %d %H%M'))
    return(at_time)

def build_record_titan_df(programs):
    p_list=[]
    for program in programs:
        # print(program)
        t=TITAN(program)
        title = t.title()
        # print(title)
        # print(t.duration())
        # print(t.start_date())
        # print(t.start_time())
        # print(t.info())
        info = t.info()
        p_list.append(info)
    return(p_list)

def make_at_time(sdate, stime, zone='GMT'):
    date_str = f'{sdate} {stime} {zone}'
    #print(date_str)
    at = convert_gmt_utc(date_str)
    return(at)



def clean_string(string):
  """
  Removes spaces and special characters from a string and replaces them with underscores.

  Args:
    string: The input string.

  Returns:
    The cleaned string with spaces and special characters replaced by underscores.
  """
  return re.sub(r'[^\w\s]', '_', string).replace(' ', '_')


def record_the_show(station, start_time):
    my_show = the_show(station, start_time)
    dur_seconds = my_show['length'].values[0]
    dur_seconds = int(dur_seconds) * 60
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

def record_the_show_no_guide(station, start_time):
    # my_show = the_show(station, start_time)
    dur_seconds = 60
    dur_seconds = int(dur_seconds) * 60
    #station = my_show['vchan'].values[0]
    #station = f'v{station}'
    #a = my_show['start'].values[0]
    #a1 = a.astype('datetime64[us]').astype(datetime) 
    #b1 = a1.astimezone() 
    #title = my_show['title'].values[0]
    #episode = my_show['sub-title'].values[0]
    #now = datetime.now()
    #local_timezone = now.astimezone().tzinfo
    #local_datetime = b1.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    #at_time = local_datetime.strftime('%Y%m%d%H%M')
    #name_of_recording = f'{title}_{episode}_{station}_{at_time}'
    #clean_name_of_recording = clean_string(name_of_recording)
    #clean_name_of_recording = f'{clean_name_of_recording}.ts'
    #run_at(clean_name_of_recording, at_time, dur_seconds, station)
    #return my_show


