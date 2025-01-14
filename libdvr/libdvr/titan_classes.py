import os
import xmltodict
import logging

from zoneinfo import ZoneInfo
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

from libdvr.util import run_command

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

def t_schedule_record(a):
    station = a['station']
    ptitle = a['title']
    #etitle = a['episode-title']
    etitle = a.get('episode', 'One')
  
    at_time = a['at_time']
    print(at_time)

    name_of_recording = f'{station}_{ptitle}_{etitle}_{at_time}'
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


class TITAN:
    def _convert_gmt_local(self):
        #print(self.doc)
        self.gmt_start_time= self.doc['tv-program-info']['program']['start-time']
        self.gmt_start_date= self.doc['tv-program-info']['program']['start-date']
        self.gmt_end_time= self.doc['tv-program-info']['program']['end-time']
        self.gmt_end_date= self.doc['tv-program-info']['program']['end-date']
        print (self.gmt_start_date, self.gmt_start_time)
        

    def __init__(self, file):
        # print('init')
        with open(file) as fd:
            self.doc = xmltodict.parse(fd.read())
        self_localtime = self._convert_gmt_local()
        
    def title(self):
        self.title = self.doc['tv-program-info']['program']['program-title'].replace(' ', '_')
        return self.title
    
    def start_time(self):
        self.start_time= self.doc['tv-program-info']['program']['start-time']
        return self.start_time
    
    def start_date(self):
        self.start_date= self.doc['tv-program-info']['program']['start-date']
        return self.start_date
    
    def info(self):
        self.info = self.doc['tv-program-info']['program']
        return self.info
    
    def end_time(self):
        pass
    def end_date(self):
        pass
    def duration(self):
        self.duration= self.doc['tv-program-info']['program']['duration']
        return self.duration


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


import re

def clean_string(string):
  """
  Removes spaces and special characters from a string and replaces them with underscores.

  Args:
    string: The input string.

  Returns:
    The cleaned string with spaces and special characters replaced by underscores.
  """
  return re.sub(r'[^\w\s]', '_', string).replace(' ', '_')

# Example usage
# input_string = "This is a test string with spaces and special characters like !@#"
# cleaned_string = clean_string(input_string)
# print(cleaned_string)  # Output: This_is_a_test_string_with_spaces_and_special_characters_like______

