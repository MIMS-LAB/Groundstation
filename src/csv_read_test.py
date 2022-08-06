import sys
# this is where python stores modules, yours could be different
#sys.path.append(r"D:/Alessandro/python39/Lib/site-packages")

sys.path.append(
    "C:/Users/MIMS-PC/AppData/Local/Programs/Python/Python39/Lib/site-packages")
sys.path.append(r"E:\school_teams\environment2\Lib\site-packages")
sys.path.append(r"D:\ALESSANDRO\MIMS lab-UAV project\Library-encoder-decoder\src")

import numpy as np
import math
import time
import pandas as pd
import csv

csv_path = r"D:\ALESSANDRO\MIMS lab-UAV project\Groundstation\datalog.csv"

with open(csv_path, 'r') as FILE:

    while (True):
        reader = csv.reader(FILE)
        for row in reader:
            data = pd.read_csv(csv_path)
            print("reading csv file %s\n" % str(row))
            print("pd data is : %s \n" % str(data))
