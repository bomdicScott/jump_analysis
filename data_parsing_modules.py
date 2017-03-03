# -*- coding: utf-8 -*-

import csv
import numpy as np
import json
import math
import os, sys
import itertools
import dateutil
import datetime
import matplotlib.pyplot as plt
from shutil import copyfile

def parsing_force_plate_raw_data(force_plate_raw_data_path):

    print("[parsing_force_plate_raw_data] force_plate_raw_data_path:{}".format(force_plate_raw_data_path))

    time_sec_tick = []
    force_N_1 = []
    force_N_2 = []
    force_N_join = []

    # [TODO] detect file comes from pasco or other brands

    # read csv
    f = open(force_plate_raw_data_path, 'rU')
    idx = 0
    error_code = 0
    for row in csv.reader(f):
        #print('row[0]:{}'.format(row[0]))
        if (
            idx >=2 and 
            row[0] != '' and 
            row[1] != '' and 
            row[2] != '' and
            row[3] != ''
           ):
            
            # format detection
            try:
                val = float(row[0])
                time_sec_tick += [float(row[0])]
                force_N_1 += [float(row[1])]
                force_N_2 += [float(row[2])]
                force_N_join += [float(row[3])]
            except:
                #print("Input is not a standard CSV file")
                error_code = 10001
        idx += 1
    #print("idx:{}".format(idx))
    if time_sec_tick[0] != 0:
        error_code = 10002

    return time_sec_tick, force_N_1, force_N_2, force_N_join, error_code




