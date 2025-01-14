#!/usr/bin/env python
# coding: utf-8

# %load_ext autoreload
# %autoreload 2 


# %load watch_now
#!/usr/bin/env python


import os
import xmltodict


from libdvr.titan_classes import get_files_titan_tvpi, get_xml_tvpi, t_schedule_record
from libdvr.titan_classes import init_dvr


logger = init_dvr()

to_be_recorded = get_files_titan_tvpi()
print(to_be_recorded)


for show_file in to_be_recorded:
    my_record = get_xml_tvpi(show_file)
    t_schedule_record(my_record)
    
# clean up tvpi files
for xml_file in to_be_recorded:
    print('deleteing:', xml_file)
    os.remove(xml_file)




