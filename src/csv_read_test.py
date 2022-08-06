
import sys
# this is where python stores modules, yours could be different
# sys.path.append(r"D:/Alessandro/python39/Lib/site-packages")

sys.path.append(
    "C:/Users/MIMS-PC/AppData/Local/Programs/Python/Python39/Lib/site-packages")
sys.path.append(r"E:\school_teams\environment2\Lib\site-packages")
sys.path.append(
    r"D:\ALESSANDRO\MIMS lab-UAV project\Library-encoder-decoder\src")

import csv
import pandas as pd
import time
import math
import numpy as np


csv_path = r"D:\ALESSANDRO\MIMS lab-UAV project\Groundstation\datalog.csv"
count = 0
count_read = 5
def roverDATA():

    data = pd.read_csv(csv_path)
    header = data['header']
    value = data['value']
    header = data['header']
    value = data['value']
    header_length = len(header)
    header_new = header[header_length-1]
    value_new = value[header_length-1]

    return (header_new,value_new)

with open(csv_path, 'r') as FILE:

    while (True):
        if(count<count_read):
            count=count+1
            time.sleep(1)

        if (count%count_read==0):
            reader = csv.reader(FILE)

            title,DATA = roverDATA()
            # now read only the last most updated value to be used later(oculus quest):
            print("header: %s\t value: %s\n" %(str(title), str(DATA)))


