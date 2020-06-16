# Python program to convert
# date to timestamp


import time
import datetime

def str_to_timestamp(string):
    return time.mktime(datetime.datetime.strptime(string,"%d/%m/%Y %H:%M").timetuple())
