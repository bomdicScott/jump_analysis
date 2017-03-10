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

def copy_txt_as_csv(data_dir): # for KISLER data
    
    file_list = os.listdir(data_dir)
    csv_list = []
    txt_list = []
    for f in file_list:
        if '.csv' in f:
            csv_list += [f.replace('.csv','')]
        if '.txt' in f:
            txt_list += [f]

    copy_list = []
    for t_name in txt_list:
        copied_detected = 0
        for c_name in csv_list:
            if c_name == t_name.replace('.txt',''):
                copied_detected = 1
        if copied_detected == 0:
            copy_list += [t_name]
    print("copy_list:{} in [{}]".format(copy_list, data_dir))
    
    for f in copy_list:
        copyfile(data_dir+f, data_dir+f.replace('.txt','.csv'))



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

    is_KISLER_file = 0
    KISLER_abs_idx = -1
    #is_KISLER_type_no_row_1 = 0 # no row [1]

    for row in csv.reader(f):
        #print('row[0]:{}'.format(row[0]))
        
        if (idx <=1):
            if 'Device:' in row[0]:
                is_KISLER_file = 1

        if is_KISLER_file != 1:
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

                if idx == 3:
                    try:
                        assert float(row[0]) == 0.001
                    except:
                        error_code = 10003   
        elif is_KISLER_file == 1:
            #print("is_KISLER_file")
            # serach abs key word
            if 'abs' in row[0]:
                KISLER_abs_idx = idx

            # found key word
            if KISLER_abs_idx != -1:
                #print("found key word")
                data_start_idx = KISLER_abs_idx + 2
                if (
                    idx >=data_start_idx and 
                    len(row) == 1 and 
                    row[0] != ''                
                   ):
                    split_list = row[0].split()
                    #print("split_list:{}").format(split_list)

                    #assert False
                    try:
                        time_sec_tick += [float(split_list[0])]
                        force_N_1 += [-1]
                        force_N_2 += [-1]
                        force_N_join += [float(split_list[1])]
                    except:
                        error_code = 10005
                elif (
                      idx >=data_start_idx and 
                      len(row) >= 2 and 
                      row[0] != '' and
                      row[1] != ''               
                    ):
                    #print("two column KISLER")
                    try:
                        time_sec_tick += [float(row[0])]
                        force_N_1 += [-1]
                        force_N_2 += [-1]
                        force_N_join += [float(row[1])]
                    except:
                        error_code = 10004


        idx += 1
    #print("idx:{}".format(idx))
    if time_sec_tick[0] != 0:
        error_code = 10002

    return time_sec_tick, force_N_1, force_N_2, force_N_join, error_code




