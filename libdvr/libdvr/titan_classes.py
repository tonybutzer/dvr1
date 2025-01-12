import os
import xmltodict

from zoneinfo import ZoneInfo
from datetime import datetime, timezone

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path

def get_files_titan_xml():
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

