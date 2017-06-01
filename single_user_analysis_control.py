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

import data_parsing_modules as DPM
import data_plot as DP
import jump_analysis_modules as JAM

def t_sorted(to_be_sorted_list, time_sec_list):

    return [sorted_result for (sorted_total_secs, sorted_result) in sorted(zip(time_sec_list, to_be_sorted_list), key=lambda pair: pair[0])]

def get_SJ_analysis_result_list(file_list):
    result_list = []
    for f_name in file_list:
        if 'analysis_results.csv' in f_name and 'SJ' in f_name:
            result_list += [f_name]
    #print("result_list:{}".format(result_list))

    return result_list

def get_CMJ_analysis_result_list(file_list):
    result_list = []
    for f_name in file_list:
        if 'analysis_results.csv' in f_name and 'CMJ' in f_name:
            result_list += [f_name]
    #print("result_list:{}".format(result_list))

    return result_list

def read_analysis_result(result_path):
    
    #print("result_path:{}".format(result_path))

    f = open(result_path, 'rU')
    for row in csv.DictReader(f): 
        data_name = row['data_name']
        contact_time_sec = row['contact_time_sec']
        TtPF_sec = row['TtPF_sec']
        RFD = row['RFD']
        jump_height_m = row['jump_height_m']
        jump_power = row['jump_power']
        fly_time_sec = row['fly_time_sec']
        PF = row['PF']

    return data_name,contact_time_sec,TtPF_sec,RFD,jump_height_m,jump_power, fly_time_sec, PF

def get_epoch_sec(YMD_string):
    epoch_time = dateutil.parser.parse("1970-01-01T00:00:00Z")
    Y = YMD_string[0:4]
    M = YMD_string[4:6]
    D = YMD_string[6:8]
    time = dateutil.parser.parse("{}-{}-{}T00:00:00Z".format(Y,M,D))
    #print("YMD_string:{}".format(YMD_string))
    #print("time:{}".format(time))
    return int((time - epoch_time).total_seconds())

def get_sorted_LSJ_ULSJ_list(s_contact_time_sec,
                               s_TtPF_sec,
                               s_RFD,
                               s_jump_height_m,
                               s_jump_power,
                               s_date,
                               s_jump_type,
                               s_try_num):
    #print("s_date:{}".format(s_date))
    #print("s_jump_type:{}".format(s_jump_type))
    s_LSJ_contact_time_sec = []
    s_LSJ_TtPF_sec = []
    s_LSJ_RFD = []
    s_LSJ_jump_height_m = []
    s_LSJ_jump_power = []
    s_LSJ_date = []
    s_LSJ_jump_type = []
    s_LSJ_try_num = []
    s_LSJ_epoch_time_sec = []

    s_ULSJ_contact_time_sec = []
    s_ULSJ_TtPF_sec = []
    s_ULSJ_RFD = []
    s_ULSJ_jump_height_m = []
    s_ULSJ_jump_power = []
    s_ULSJ_date = []
    s_ULSJ_jump_type = []
    s_ULSJ_try_num = []
    s_ULSJ_epoch_time_sec = []

    for i in range(len(s_date)):
        #print("s_jump_type[i]:{}".format(s_jump_type[i]))
        if s_jump_type[i] == 'LSJ':
            s_LSJ_contact_time_sec += [s_contact_time_sec[i]]
            s_LSJ_TtPF_sec += [s_TtPF_sec[i]]
            s_LSJ_RFD += [s_RFD[i]]
            s_LSJ_jump_height_m += [s_jump_height_m[i]]
            s_LSJ_jump_power += [s_jump_power[i]]
            s_LSJ_date += [s_date[i]]
            s_LSJ_jump_type += [s_jump_type[i]]
            s_LSJ_try_num += [s_try_num[i]]
            s_LSJ_epoch_time_sec += [get_epoch_sec(s_date[i])]

        elif s_jump_type[i] == 'ULSJ':
            #print("s_ULSJ_epoch_time_sec:{}".format(s_ULSJ_epoch_time_sec))
            s_ULSJ_contact_time_sec += [s_contact_time_sec[i]]
            s_ULSJ_TtPF_sec += [s_TtPF_sec[i]]
            s_ULSJ_RFD += [s_RFD[i]]
            s_ULSJ_jump_height_m += [s_jump_height_m[i]]
            s_ULSJ_jump_power += [s_jump_power[i]]
            s_ULSJ_date += [s_date[i]]
            s_ULSJ_jump_type += [s_jump_type[i]]
            s_ULSJ_try_num += [s_try_num[i]]
            #print("get_epoch_sec(s_date[i]):{}".format(get_epoch_sec(s_date[i])))
            s_ULSJ_epoch_time_sec += [get_epoch_sec(s_date[i])]

    #print("LSJ_date:{}".format(LSJ_date))
    #print("LSJ_epoch_time_sec:{}".format(LSJ_epoch_time_sec))
    #print("ULSJ_date:{}".format(ULSJ_date))
    #print("ULSJ_epoch_time_sec:{}".format(ULSJ_epoch_time_sec))
    #print("s_LSJ_date:{}".format(s_LSJ_date))
    #print("[c1]s_LSJ_epoch_time_sec:{}".format(s_LSJ_epoch_time_sec))
    #print("s_ULSJ_date:{}".format(s_ULSJ_date))
    #print("[c1]s_ULSJ_epoch_time_sec:{}".format(s_ULSJ_epoch_time_sec))

    # sort data
    # t_sorted(to_be_sorted_list, time_sec_list)
    s_LSJ_contact_time_sec = t_sorted(s_LSJ_contact_time_sec, s_LSJ_epoch_time_sec)
    s_LSJ_TtPF_sec = t_sorted(s_LSJ_TtPF_sec, s_LSJ_epoch_time_sec)
    s_LSJ_RFD = t_sorted(s_LSJ_RFD, s_LSJ_epoch_time_sec)
    s_LSJ_jump_height_m = t_sorted(s_LSJ_jump_height_m, s_LSJ_epoch_time_sec)
    s_LSJ_jump_power = t_sorted(s_LSJ_jump_power, s_LSJ_epoch_time_sec)
    s_LSJ_date = t_sorted(s_LSJ_date, s_LSJ_epoch_time_sec)
    s_LSJ_jump_type = t_sorted(s_LSJ_jump_type, s_LSJ_epoch_time_sec)
    s_LSJ_try_num = t_sorted(s_LSJ_try_num, s_LSJ_epoch_time_sec)
    s_LSJ_epoch_time_sec = t_sorted(s_LSJ_epoch_time_sec, s_LSJ_epoch_time_sec)

    s_ULSJ_contact_time_sec = t_sorted(s_ULSJ_contact_time_sec, s_ULSJ_epoch_time_sec)
    s_ULSJ_TtPF_sec = t_sorted(s_ULSJ_TtPF_sec, s_ULSJ_epoch_time_sec)
    s_ULSJ_RFD = t_sorted(s_ULSJ_RFD, s_ULSJ_epoch_time_sec)
    s_ULSJ_jump_height_m = t_sorted(s_ULSJ_jump_height_m, s_ULSJ_epoch_time_sec)
    s_ULSJ_jump_power = t_sorted(s_ULSJ_jump_power, s_ULSJ_epoch_time_sec)
    s_ULSJ_date = t_sorted(s_ULSJ_date, s_ULSJ_epoch_time_sec)
    s_ULSJ_jump_type = t_sorted(s_ULSJ_jump_type, s_ULSJ_epoch_time_sec)
    s_ULSJ_try_num = t_sorted(s_ULSJ_try_num, s_ULSJ_epoch_time_sec)
    s_ULSJ_epoch_time_sec = t_sorted(s_ULSJ_epoch_time_sec, s_ULSJ_epoch_time_sec)

    #print("s_LSJ_contact_time_sec:{}".format(s_LSJ_contact_time_sec))
    #print("s_LSJ_date:{}".format(s_LSJ_date))
    #print("s_LSJ_epoch_time_sec:{}".format(s_LSJ_epoch_time_sec))
    #print("s_ULSJ_epoch_time_sec:{}".format(s_ULSJ_epoch_time_sec))

    return s_LSJ_contact_time_sec,s_LSJ_TtPF_sec,s_LSJ_RFD,s_LSJ_jump_height_m,s_LSJ_jump_power,s_LSJ_date,s_LSJ_jump_type,s_LSJ_try_num,s_LSJ_epoch_time_sec,s_ULSJ_contact_time_sec,s_ULSJ_TtPF_sec,s_ULSJ_RFD,s_ULSJ_jump_height_m,s_ULSJ_jump_power,s_ULSJ_date,s_ULSJ_jump_type,s_ULSJ_try_num,s_ULSJ_epoch_time_sec

def get_sorted_LCMJ_ULCMJ_list(s_contact_time_sec,
                               s_TtPF_sec,
                               s_RFD,
                               s_jump_height_m,
                               s_jump_power,
                               s_date,
                               s_jump_type,
                               s_try_num):
    #print("s_date:{}".format(s_date))
    #print("s_jump_type:{}".format(s_jump_type))
    s_LCMJ_contact_time_sec = []
    s_LCMJ_TtPF_sec = []
    s_LCMJ_RFD = []
    s_LCMJ_jump_height_m = []
    s_LCMJ_jump_power = []
    s_LCMJ_date = []
    s_LCMJ_jump_type = []
    s_LCMJ_try_num = []
    s_LCMJ_epoch_time_sec = []

    s_ULCMJ_contact_time_sec = []
    s_ULCMJ_TtPF_sec = []
    s_ULCMJ_RFD = []
    s_ULCMJ_jump_height_m = []
    s_ULCMJ_jump_power = []
    s_ULCMJ_date = []
    s_ULCMJ_jump_type = []
    s_ULCMJ_try_num = []
    s_ULCMJ_epoch_time_sec = []

    for i in range(len(s_date)):
        #print("s_jump_type[i]:{}".format(s_jump_type[i]))
        if s_jump_type[i] == 'LCMJ':
            s_LCMJ_contact_time_sec += [s_contact_time_sec[i]]
            s_LCMJ_TtPF_sec += [s_TtPF_sec[i]]
            s_LCMJ_RFD += [s_RFD[i]]
            s_LCMJ_jump_height_m += [s_jump_height_m[i]]
            s_LCMJ_jump_power += [s_jump_power[i]]
            s_LCMJ_date += [s_date[i]]
            s_LCMJ_jump_type += [s_jump_type[i]]
            s_LCMJ_try_num += [s_try_num[i]]
            s_LCMJ_epoch_time_sec += [get_epoch_sec(s_date[i])]

        elif s_jump_type[i] == 'ULCMJ':
            #print("s_ULCMJ_epoch_time_sec:{}".format(s_ULCMJ_epoch_time_sec))
            s_ULCMJ_contact_time_sec += [s_contact_time_sec[i]]
            s_ULCMJ_TtPF_sec += [s_TtPF_sec[i]]
            s_ULCMJ_RFD += [s_RFD[i]]
            s_ULCMJ_jump_height_m += [s_jump_height_m[i]]
            s_ULCMJ_jump_power += [s_jump_power[i]]
            s_ULCMJ_date += [s_date[i]]
            s_ULCMJ_jump_type += [s_jump_type[i]]
            s_ULCMJ_try_num += [s_try_num[i]]
            #print("get_epoch_sec(s_date[i]):{}".format(get_epoch_sec(s_date[i])))
            s_ULCMJ_epoch_time_sec += [get_epoch_sec(s_date[i])]

    #print("LCMJ_date:{}".format(LCMJ_date))
    #print("LCMJ_epoch_time_sec:{}".format(LCMJ_epoch_time_sec))
    #print("ULCMJ_date:{}".format(ULCMJ_date))
    #print("ULCMJ_epoch_time_sec:{}".format(ULCMJ_epoch_time_sec))
    #print("s_LCMJ_date:{}".format(s_LCMJ_date))
    #print("[c1]s_LCMJ_epoch_time_sec:{}".format(s_LCMJ_epoch_time_sec))
    #print("s_ULCMJ_date:{}".format(s_ULCMJ_date))
    #print("[c1]s_ULCMJ_epoch_time_sec:{}".format(s_ULCMJ_epoch_time_sec))

    # sort data
    # t_sorted(to_be_sorted_list, time_sec_list)
    s_LCMJ_contact_time_sec = t_sorted(s_LCMJ_contact_time_sec, s_LCMJ_epoch_time_sec)
    s_LCMJ_TtPF_sec = t_sorted(s_LCMJ_TtPF_sec, s_LCMJ_epoch_time_sec)
    s_LCMJ_RFD = t_sorted(s_LCMJ_RFD, s_LCMJ_epoch_time_sec)
    s_LCMJ_jump_height_m = t_sorted(s_LCMJ_jump_height_m, s_LCMJ_epoch_time_sec)
    s_LCMJ_jump_power = t_sorted(s_LCMJ_jump_power, s_LCMJ_epoch_time_sec)
    s_LCMJ_date = t_sorted(s_LCMJ_date, s_LCMJ_epoch_time_sec)
    s_LCMJ_jump_type = t_sorted(s_LCMJ_jump_type, s_LCMJ_epoch_time_sec)
    s_LCMJ_try_num = t_sorted(s_LCMJ_try_num, s_LCMJ_epoch_time_sec)
    s_LCMJ_epoch_time_sec = t_sorted(s_LCMJ_epoch_time_sec, s_LCMJ_epoch_time_sec)

    s_ULCMJ_contact_time_sec = t_sorted(s_ULCMJ_contact_time_sec, s_ULCMJ_epoch_time_sec)
    s_ULCMJ_TtPF_sec = t_sorted(s_ULCMJ_TtPF_sec, s_ULCMJ_epoch_time_sec)
    s_ULCMJ_RFD = t_sorted(s_ULCMJ_RFD, s_ULCMJ_epoch_time_sec)
    s_ULCMJ_jump_height_m = t_sorted(s_ULCMJ_jump_height_m, s_ULCMJ_epoch_time_sec)
    s_ULCMJ_jump_power = t_sorted(s_ULCMJ_jump_power, s_ULCMJ_epoch_time_sec)
    s_ULCMJ_date = t_sorted(s_ULCMJ_date, s_ULCMJ_epoch_time_sec)
    s_ULCMJ_jump_type = t_sorted(s_ULCMJ_jump_type, s_ULCMJ_epoch_time_sec)
    s_ULCMJ_try_num = t_sorted(s_ULCMJ_try_num, s_ULCMJ_epoch_time_sec)
    s_ULCMJ_epoch_time_sec = t_sorted(s_ULCMJ_epoch_time_sec, s_ULCMJ_epoch_time_sec)

    #print("s_LCMJ_contact_time_sec:{}".format(s_LCMJ_contact_time_sec))
    #print("s_LCMJ_date:{}".format(s_LCMJ_date))
    #print("s_LCMJ_epoch_time_sec:{}".format(s_LCMJ_epoch_time_sec))
    #print("s_ULCMJ_epoch_time_sec:{}".format(s_ULCMJ_epoch_time_sec))

    return s_LCMJ_contact_time_sec,s_LCMJ_TtPF_sec,s_LCMJ_RFD,s_LCMJ_jump_height_m,s_LCMJ_jump_power,s_LCMJ_date,s_LCMJ_jump_type,s_LCMJ_try_num,s_LCMJ_epoch_time_sec,s_ULCMJ_contact_time_sec,s_ULCMJ_TtPF_sec,s_ULCMJ_RFD,s_ULCMJ_jump_height_m,s_ULCMJ_jump_power,s_ULCMJ_date,s_ULCMJ_jump_type,s_ULCMJ_try_num,s_ULCMJ_epoch_time_sec

def get_avg_list(data_list, time_list):
    avg_data_list = []
    avg_time_list = []
    #print("data_list:{}".format(data_list))
    #print("time_list:{}".format(time_list))
    for i in range(len(time_list)):
        data_list[i] = float(data_list[i])
        if avg_time_list == []:
            avg_time_list += [time_list[i]] # add time
            avg_temp = data_list[i]
            avg_count = 1
            if len(time_list) == 1: # has only one element
                avg_data_list += [avg_temp] # add avg and quit for
        else:
            if time_list[i] == avg_time_list[-1]:
                avg_count += 1
                avg_temp = (avg_temp * (avg_count-1) + data_list[i])/avg_count
                if i == len(time_list)-1:
                    avg_data_list += [avg_temp] # add avg
            else:
                avg_time_list += [time_list[i]] # add time
                avg_data_list += [avg_temp] # add avg
                avg_temp = data_list[i]
                avg_count = 1

    #print("avg_data_list:{}".format(avg_data_list))
    #print("avg_time_list:{}".format(avg_time_list))
    assert len(avg_time_list) == len(avg_data_list)

    return avg_data_list

def get_avg_LSJ_ULSJ_list(s_LSJ_contact_time_sec,s_LSJ_TtPF_sec,s_LSJ_RFD,s_LSJ_jump_height_m,s_LSJ_jump_power,s_LSJ_date,s_LSJ_jump_type,s_LSJ_try_num,s_LSJ_epoch_time_sec,s_ULSJ_contact_time_sec,s_ULSJ_TtPF_sec,s_ULSJ_RFD,s_ULSJ_jump_height_m,s_ULSJ_jump_power,s_ULSJ_date,s_ULSJ_jump_type,s_ULSJ_try_num,s_ULSJ_epoch_time_sec):

    s_avg_LSJ_contact_time_sec = get_avg_list(s_LSJ_contact_time_sec, s_LSJ_date)
    s_avg_LSJ_TtPF_sec = get_avg_list(s_LSJ_TtPF_sec, s_LSJ_date)
    s_avg_LSJ_RFD = get_avg_list(s_LSJ_RFD, s_LSJ_date)
    s_avg_LSJ_jump_height_m = get_avg_list(s_LSJ_jump_height_m, s_LSJ_date)
    s_avg_LSJ_jump_power = get_avg_list(s_LSJ_jump_power, s_LSJ_date)
    s_avg_LSJ_date = get_avg_list(s_LSJ_date, s_LSJ_date)
    s_avg_LSJ_epoch_time_sec = get_avg_list(s_LSJ_epoch_time_sec, s_LSJ_date)

    s_avg_ULSJ_contact_time_sec = get_avg_list(s_ULSJ_contact_time_sec, s_ULSJ_date)
    s_avg_ULSJ_TtPF_sec = get_avg_list(s_ULSJ_TtPF_sec, s_ULSJ_date)
    s_avg_ULSJ_RFD = get_avg_list(s_ULSJ_RFD, s_ULSJ_date)
    s_avg_ULSJ_jump_height_m = get_avg_list(s_ULSJ_jump_height_m, s_ULSJ_date)
    s_avg_ULSJ_jump_power = get_avg_list(s_ULSJ_jump_power, s_ULSJ_date)
    s_avg_ULSJ_date = get_avg_list(s_ULSJ_date, s_ULSJ_date)
    s_avg_ULSJ_epoch_time_sec = get_avg_list(s_ULSJ_epoch_time_sec, s_ULSJ_date)
    
    #print("s_avg_LSJ_date:{}".format(s_avg_LSJ_date))
    #print("s_avg_LSJ_epoch_time_sec:{}".format(s_avg_LSJ_epoch_time_sec))
    #print("s_avg_LSJ_jump_height_m:{}".format(s_avg_LSJ_jump_height_m))

    return s_avg_LSJ_contact_time_sec,s_avg_LSJ_TtPF_sec,s_avg_LSJ_RFD,s_avg_LSJ_jump_height_m,s_avg_LSJ_jump_power,s_avg_LSJ_date,s_avg_LSJ_epoch_time_sec,s_avg_ULSJ_contact_time_sec,s_avg_ULSJ_TtPF_sec,s_avg_ULSJ_RFD,s_avg_ULSJ_jump_height_m,s_avg_ULSJ_jump_power,s_avg_ULSJ_date,s_avg_ULSJ_epoch_time_sec

def get_avg_LCMJ_ULCMJ_list(s_LCMJ_contact_time_sec,s_LCMJ_TtPF_sec,s_LCMJ_RFD,s_LCMJ_jump_height_m,s_LCMJ_jump_power,s_LCMJ_date,s_LCMJ_jump_type,s_LCMJ_try_num,s_LCMJ_epoch_time_sec,s_ULCMJ_contact_time_sec,s_ULCMJ_TtPF_sec,s_ULCMJ_RFD,s_ULCMJ_jump_height_m,s_ULCMJ_jump_power,s_ULCMJ_date,s_ULCMJ_jump_type,s_ULCMJ_try_num,s_ULCMJ_epoch_time_sec):

    s_avg_LCMJ_contact_time_sec = get_avg_list(s_LCMJ_contact_time_sec, s_LCMJ_date)
    s_avg_LCMJ_TtPF_sec = get_avg_list(s_LCMJ_TtPF_sec, s_LCMJ_date)
    s_avg_LCMJ_RFD = get_avg_list(s_LCMJ_RFD, s_LCMJ_date)
    s_avg_LCMJ_jump_height_m = get_avg_list(s_LCMJ_jump_height_m, s_LCMJ_date)
    s_avg_LCMJ_jump_power = get_avg_list(s_LCMJ_jump_power, s_LCMJ_date)
    s_avg_LCMJ_date = get_avg_list(s_LCMJ_date, s_LCMJ_date)
    s_avg_LCMJ_epoch_time_sec = get_avg_list(s_LCMJ_epoch_time_sec, s_LCMJ_date)

    s_avg_ULCMJ_contact_time_sec = get_avg_list(s_ULCMJ_contact_time_sec, s_ULCMJ_date)
    s_avg_ULCMJ_TtPF_sec = get_avg_list(s_ULCMJ_TtPF_sec, s_ULCMJ_date)
    s_avg_ULCMJ_RFD = get_avg_list(s_ULCMJ_RFD, s_ULCMJ_date)
    s_avg_ULCMJ_jump_height_m = get_avg_list(s_ULCMJ_jump_height_m, s_ULCMJ_date)
    s_avg_ULCMJ_jump_power = get_avg_list(s_ULCMJ_jump_power, s_ULCMJ_date)
    s_avg_ULCMJ_date = get_avg_list(s_ULCMJ_date, s_ULCMJ_date)
    s_avg_ULCMJ_epoch_time_sec = get_avg_list(s_ULCMJ_epoch_time_sec, s_ULCMJ_date)
    
    #print("s_avg_LCMJ_date:{}".format(s_avg_LCMJ_date))
    #print("s_avg_LCMJ_epoch_time_sec:{}".format(s_avg_LCMJ_epoch_time_sec))
    #print("s_avg_LCMJ_jump_height_m:{}".format(s_avg_LCMJ_jump_height_m))

    return s_avg_LCMJ_contact_time_sec,s_avg_LCMJ_TtPF_sec,s_avg_LCMJ_RFD,s_avg_LCMJ_jump_height_m,s_avg_LCMJ_jump_power,s_avg_LCMJ_date,s_avg_LCMJ_epoch_time_sec,s_avg_ULCMJ_contact_time_sec,s_avg_ULCMJ_TtPF_sec,s_avg_ULCMJ_RFD,s_avg_ULCMJ_jump_height_m,s_avg_ULCMJ_jump_power,s_avg_ULCMJ_date,s_avg_ULCMJ_epoch_time_sec

def update_user_SJ_statistics(data_dir):
    
    file_list = os.listdir(data_dir)
    result_list = get_SJ_analysis_result_list(file_list)
    user_statistics_path = data_dir + '____user_SJ_statistics.csv'

    s_data_name = []
    s_contact_time_sec = []
    s_TtPF_sec = []
    s_RFD = []
    s_jump_height_m = []
    s_jump_power = []
    s_date = []
    s_jump_type = []
    s_try_num = []
    s_fly_time_sec = []
    s_PF = []

    for result_name in result_list:
        result_path = data_dir + result_name

        if os.path.exists(result_path):
            data_name,contact_time_sec,TtPF_sec,RFD,jump_height_m,jump_power, fly_time_sec, PF = read_analysis_result(result_path)

            s_data_name += [data_name]
            s_contact_time_sec += [contact_time_sec]
            s_TtPF_sec += [TtPF_sec]
            s_RFD += [RFD]
            s_jump_height_m += [jump_height_m]
            s_jump_power += [jump_power]
            s_fly_time_sec += [fly_time_sec]
            s_PF += [PF]

            # if data_name uses standard format
            data_name_split = data_name.split('_')
            #print("data_name_split:{}".format(data_name_split))

            if len(data_name_split) == 4 and len(data_name_split[1]) == 8 and data_name_split[1][0:2] == '20' and 't' in data_name_split[3]:
                s_date += [data_name_split[1]]
                s_jump_type += [data_name_split[2]]
                s_try_num += [data_name_split[3]]
            else:
                s_date += ['NA']
                s_jump_type += ['NA']
                s_try_num += ['NA']

    csv_header = []
    csv_header += ["s_data_name"]
    csv_header += ["s_contact_time_sec"]
    csv_header += ["s_fly_time_sec"]
    csv_header += ["s_TtPF_sec"]
    csv_header += ["s_PF"]
    csv_header += ["s_RFD"]
    csv_header += ["s_jump_height_m"]
    csv_header += ["s_jump_power"]
    csv_header += ["s_date"]
    csv_header += ["s_jump_type"]
    csv_header += ["s_try_num"]

    with open(user_statistics_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(s_data_name)+1):
            data = []
            if row == 0:
                data = csv_header
            else:
                for col in range(len(csv_header)):
                    #print("csv_header[col]:{}".format((csv_header[col])))
                    #print("len:{}".format(len(eval(csv_header[col]))))
                    data += [eval(csv_header[col])[row-1]]
            writer.writerow(data)
        csvfile.close()


    # LSJ / ULSJ list
    s_LSJ_contact_time_sec,s_LSJ_TtPF_sec,s_LSJ_RFD,s_LSJ_jump_height_m,s_LSJ_jump_power,s_LSJ_date,s_LSJ_jump_type,s_LSJ_try_num,s_LSJ_epoch_time_sec,s_ULSJ_contact_time_sec,s_ULSJ_TtPF_sec,s_ULSJ_RFD,s_ULSJ_jump_height_m,s_ULSJ_jump_power,s_ULSJ_date,s_ULSJ_jump_type,s_ULSJ_try_num,s_ULSJ_epoch_time_sec = get_sorted_LSJ_ULSJ_list(s_contact_time_sec,
                               s_TtPF_sec,
                               s_RFD,
                               s_jump_height_m,
                               s_jump_power,
                               s_date,
                               s_jump_type,
                               s_try_num)

    #print("s_date:{}".format(s_date))
    #print("s_ULSJ_epoch_time_sec:{}".format(s_ULSJ_epoch_time_sec))

    # get avg LSJ / ULSJ list
    s_avg_LSJ_contact_time_sec,s_avg_LSJ_TtPF_sec,s_avg_LSJ_RFD,s_avg_LSJ_jump_height_m,s_avg_LSJ_jump_power,s_avg_LSJ_date,s_avg_LSJ_epoch_time_sec,s_avg_ULSJ_contact_time_sec,s_avg_ULSJ_TtPF_sec,s_avg_ULSJ_RFD,s_avg_ULSJ_jump_height_m,s_avg_ULSJ_jump_power,s_avg_ULSJ_date,s_avg_ULSJ_epoch_time_sec = get_avg_LSJ_ULSJ_list(s_LSJ_contact_time_sec,s_LSJ_TtPF_sec,s_LSJ_RFD,s_LSJ_jump_height_m,s_LSJ_jump_power,s_LSJ_date,s_LSJ_jump_type,s_LSJ_try_num,s_LSJ_epoch_time_sec,s_ULSJ_contact_time_sec,s_ULSJ_TtPF_sec,s_ULSJ_RFD,s_ULSJ_jump_height_m,s_ULSJ_jump_power,s_ULSJ_date,s_ULSJ_jump_type,s_ULSJ_try_num,s_ULSJ_epoch_time_sec)
    




    # plot fig
    if s_LSJ_epoch_time_sec != []:
        fig = DP.get_fig_LSJ_analysis(s_LSJ_contact_time_sec,
                              s_LSJ_TtPF_sec,
                              s_LSJ_RFD,
                              s_LSJ_jump_height_m,
                              s_LSJ_jump_power,
                              s_LSJ_date,
                              s_LSJ_epoch_time_sec,
                              s_avg_LSJ_contact_time_sec,
                              s_avg_LSJ_TtPF_sec,
                              s_avg_LSJ_RFD,
                              s_avg_LSJ_jump_height_m,
                              s_avg_LSJ_jump_power,
                              s_avg_LSJ_date,
                              s_avg_LSJ_epoch_time_sec)
        fig.savefig( data_dir + '____LSJ_analysis.png'.format(data_name))
        plt.close(fig)
    #print("s_ULSJ_epoch_time_sec:{}".format(s_ULSJ_epoch_time_sec))
    if s_ULSJ_epoch_time_sec != []:
        fig = DP.get_fig_ULSJ_analysis(s_ULSJ_contact_time_sec,
                           s_ULSJ_TtPF_sec,
                           s_ULSJ_RFD,
                           s_ULSJ_jump_height_m,
                           s_ULSJ_jump_power,
                           s_ULSJ_date,
                           s_ULSJ_epoch_time_sec,
                           s_avg_ULSJ_contact_time_sec,
                           s_avg_ULSJ_TtPF_sec,
                           s_avg_ULSJ_RFD,
                           s_avg_ULSJ_jump_height_m,
                           s_avg_ULSJ_jump_power,
                           s_avg_ULSJ_date,
                           s_avg_ULSJ_epoch_time_sec)
        fig.savefig( data_dir + '____ULSJ_analysis.png'.format(data_name))
        plt.close(fig)
    if s_avg_ULSJ_epoch_time_sec != [] and s_avg_LSJ_epoch_time_sec != []:
        fig = DP.get_fig_SJ_compare(s_avg_ULSJ_date, s_avg_ULSJ_epoch_time_sec, s_avg_ULSJ_jump_height_m, s_avg_LSJ_date, s_avg_LSJ_epoch_time_sec, s_avg_LSJ_jump_height_m)
        fig.savefig( data_dir + '____SJ_compare.png'.format(data_name))
        plt.close(fig)

def update_user_CMJ_statistics(data_dir):
    
    file_list = os.listdir(data_dir)
    result_list = get_CMJ_analysis_result_list(file_list)
    user_statistics_path = data_dir + '____user_CMJ_statistics.csv'

    s_data_name = []
    s_contact_time_sec = []
    s_TtPF_sec = []
    s_RFD = []
    s_jump_height_m = []
    s_jump_power = []
    s_date = []
    s_jump_type = []
    s_try_num = []
    s_fly_time_sec = []
    s_PF = []

    for result_name in result_list:
        result_path = data_dir + result_name

        if os.path.exists(result_path):
            data_name,contact_time_sec,TtPF_sec,RFD,jump_height_m,jump_power, fly_time_sec, PF = read_analysis_result(result_path)

            s_data_name += [data_name]
            s_contact_time_sec += [contact_time_sec]
            s_TtPF_sec += [TtPF_sec]
            s_RFD += [RFD]
            s_jump_height_m += [jump_height_m]
            s_jump_power += [jump_power]
            s_fly_time_sec += [fly_time_sec]
            s_PF += [PF]

            # if data_name uses standard format
            data_name_split = data_name.split('_')
            #print("data_name_split:{}".format(data_name_split))

            if len(data_name_split) == 4 and len(data_name_split[1]) == 8 and data_name_split[1][0:2] == '20' and 't' in data_name_split[3]:
                s_date += [data_name_split[1]]
                s_jump_type += [data_name_split[2]]
                s_try_num += [data_name_split[3]]
            else:
                s_date += ['NA']
                s_jump_type += ['NA']
                s_try_num += ['NA']

    csv_header = []
    csv_header += ["s_data_name"]
    csv_header += ["s_contact_time_sec"]
    csv_header += ["s_fly_time_sec"]
    csv_header += ["s_TtPF_sec"]
    csv_header += ["s_PF"]
    csv_header += ["s_RFD"]
    csv_header += ["s_jump_height_m"]
    csv_header += ["s_jump_power"]
    csv_header += ["s_date"]
    csv_header += ["s_jump_type"]
    csv_header += ["s_try_num"]
            
    with open(user_statistics_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(s_data_name)+1):
            data = []
            if row == 0:
                data = csv_header
            else:
                for col in range(len(csv_header)):
                    #print("csv_header[col]:{}".format((csv_header[col])))
                    #print("len:{}".format(len(eval(csv_header[col]))))
                    data += [eval(csv_header[col])[row-1]]
            writer.writerow(data)
        csvfile.close()

    # LCMJ / ULCMJ list
    s_LCMJ_contact_time_sec,s_LCMJ_TtPF_sec,s_LCMJ_RFD,s_LCMJ_jump_height_m,s_LCMJ_jump_power,s_LCMJ_date,s_LCMJ_jump_type,s_LCMJ_try_num,s_LCMJ_epoch_time_sec,s_ULCMJ_contact_time_sec,s_ULCMJ_TtPF_sec,s_ULCMJ_RFD,s_ULCMJ_jump_height_m,s_ULCMJ_jump_power,s_ULCMJ_date,s_ULCMJ_jump_type,s_ULCMJ_try_num,s_ULCMJ_epoch_time_sec = get_sorted_LCMJ_ULCMJ_list(s_contact_time_sec,
                               s_TtPF_sec,
                               s_RFD,
                               s_jump_height_m,
                               s_jump_power,
                               s_date,
                               s_jump_type,
                               s_try_num)

    #print("s_date:{}".format(s_date))
    #print("s_ULCMJ_epoch_time_sec:{}".format(s_ULCMJ_epoch_time_sec))

    # get avg LCMJ / ULCMJ list
    s_avg_LCMJ_contact_time_sec,s_avg_LCMJ_TtPF_sec,s_avg_LCMJ_RFD,s_avg_LCMJ_jump_height_m,s_avg_LCMJ_jump_power,s_avg_LCMJ_date,s_avg_LCMJ_epoch_time_sec,s_avg_ULCMJ_contact_time_sec,s_avg_ULCMJ_TtPF_sec,s_avg_ULCMJ_RFD,s_avg_ULCMJ_jump_height_m,s_avg_ULCMJ_jump_power,s_avg_ULCMJ_date,s_avg_ULCMJ_epoch_time_sec = get_avg_LCMJ_ULCMJ_list(s_LCMJ_contact_time_sec,s_LCMJ_TtPF_sec,s_LCMJ_RFD,s_LCMJ_jump_height_m,s_LCMJ_jump_power,s_LCMJ_date,s_LCMJ_jump_type,s_LCMJ_try_num,s_LCMJ_epoch_time_sec,s_ULCMJ_contact_time_sec,s_ULCMJ_TtPF_sec,s_ULCMJ_RFD,s_ULCMJ_jump_height_m,s_ULCMJ_jump_power,s_ULCMJ_date,s_ULCMJ_jump_type,s_ULCMJ_try_num,s_ULCMJ_epoch_time_sec)

    # plot fig
    if s_LCMJ_epoch_time_sec != []:
        fig = DP.get_fig_LCMJ_analysis(s_LCMJ_contact_time_sec,
                              s_LCMJ_TtPF_sec,
                              s_LCMJ_RFD,
                              s_LCMJ_jump_height_m,
                              s_LCMJ_jump_power,
                              s_LCMJ_date,
                              s_LCMJ_epoch_time_sec,
                              s_avg_LCMJ_contact_time_sec,
                              s_avg_LCMJ_TtPF_sec,
                              s_avg_LCMJ_RFD,
                              s_avg_LCMJ_jump_height_m,
                              s_avg_LCMJ_jump_power,
                              s_avg_LCMJ_date,
                              s_avg_LCMJ_epoch_time_sec)
        fig.savefig( data_dir + '____LCMJ_analysis.png'.format(data_name))
        plt.close(fig)
    #print("s_ULCMJ_epoch_time_sec:{}".format(s_ULCMJ_epoch_time_sec))
    if s_ULCMJ_epoch_time_sec != []:
        fig = DP.get_fig_ULCMJ_analysis(s_ULCMJ_contact_time_sec,
                           s_ULCMJ_TtPF_sec,
                           s_ULCMJ_RFD,
                           s_ULCMJ_jump_height_m,
                           s_ULCMJ_jump_power,
                           s_ULCMJ_date,
                           s_ULCMJ_epoch_time_sec,
                           s_avg_ULCMJ_contact_time_sec,
                           s_avg_ULCMJ_TtPF_sec,
                           s_avg_ULCMJ_RFD,
                           s_avg_ULCMJ_jump_height_m,
                           s_avg_ULCMJ_jump_power,
                           s_avg_ULCMJ_date,
                           s_avg_ULCMJ_epoch_time_sec)
        fig.savefig( data_dir + '____ULCMJ_analysis.png'.format(data_name))
        plt.close(fig)
    if s_avg_ULCMJ_epoch_time_sec != [] and s_avg_LCMJ_epoch_time_sec != []:
        fig = DP.get_fig_CMJ_compare(s_avg_ULCMJ_date, s_avg_ULCMJ_epoch_time_sec, s_avg_ULCMJ_jump_height_m, s_avg_LCMJ_date, s_avg_LCMJ_epoch_time_sec, s_avg_LCMJ_jump_height_m)
        fig.savefig( data_dir + '____CMJ_compare.png'.format(data_name))
        plt.close(fig)




def single_user_analysis(data_dir):

    file_list = os.listdir(data_dir)
    analysis_list = JAM.get_analysis_list(file_list)

    list_new_fig_time_force_notiation_path = []
    list_new_error_fig_path = []

    # test only section
    #analysis_list = ['Lt1']
    #analysis_list = ['ULt1']
    #if 'Gaby' in data_dir:
    #    analysis_list = ['Lg1']
    #if 'Tom' in data_dir:
    #    analysis_list = ['Lt1']
    #if 'user1' in data_dir:
    #    analysis_list = ['benson']
    #if 'user1' in data_dir:
    #    analysis_list = ['user1_20170329_ULSJ_t1','user1_20170329_ULSJ_t2']
    #    analysis_list = ['user1_20170329_ULSJ_t2']
    #    analysis_list = ['user1_20170428_ULSJ_t1']
    #    analysis_list = ['user1_20170530_ULCMJ_t1']
    #if 'user2' in data_dir:
    #    analysis_list = ['user2_20170428_LSJ_t1']
    #if 'user12' in data_dir:
    #    analysis_list = ['user12_20170428_LSJ_t3']
    # test only section end
    #if 'scott' in data_dir:
    #    analysis_list = ['scott_20170525_ULSJ_t1'] # uneven floor ?
    #if 'scott' in data_dir:
        #analysis_list = ['scott_20170525_LCMJ_t1']
        #analysis_list = ['scott_20170525_ULSJ_t1'] # one air force error

    if analysis_list == []:
        print("[No new data waited for analysis] Please copy new force plate csv file into data folder:[{}]".format(data_dir))
    else:
        for data_name in analysis_list:

            #data_name = 'benson'
            #body_weight = 77.5

            force_plate_raw_data_path = data_dir + data_name +".csv"
            T = 0.001

            time_sec_tick, force_N_1, force_N_2, force_N_join, error_code = DPM.parsing_force_plate_raw_data(force_plate_raw_data_path)
            # error handling
            if error_code != 0:
                err_msg = "[Analysis Error] Input file does not have correct CSV format."
                print("error_code:{}".format(error_code))
                print(err_msg)
                # plot err msg
                fig = DP.get_fig_no_data_with_err_msg(error_code,err_msg)
                fig.savefig( data_dir + '{}_error_message.png'.format(data_name))
                list_new_error_fig_path += [data_dir + '{}_error_message.png'.format(data_name)]
                plt.close(fig)

                #sys.exit()
            elif not('CMJ' in data_name or 'SJ' in data_name):
                err_msg = "[Input Name Error] Unrecognized Jump Type. Valid types: CMJ / SJ"
                error_code = 10201
                print("error_code:{}".format(error_code))
                print(err_msg)
                # plot err msg
                fig = DP.get_fig_no_data_with_err_msg(error_code,err_msg)
                fig.savefig( data_dir + '{}_error_message.png'.format(data_name))
                list_new_error_fig_path += [data_dir + '{}_error_message.png'.format(data_name)]
                plt.close(fig)

            elif 'CMJ' in data_name:

                stg_num, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_acc_end, ec_acc_end_tick, ec_low, ec_deacc_start, ec_deacc_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick = JAM.get_CMJ_features_of_join_force(data_name, time_sec_tick, force_N_join)

                a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick, ec_acc_end, ec_acc_end_tick, ec_deacc_start, ec_deacc_start_tick, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick = JAM.get_CMJ_a_v_p(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_acc_end, ec_acc_end_tick, ec_low, ec_deacc_start, ec_deacc_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick)


                if stg_num != 4: # not finish test correctly. should return error message.
                    print("stg_num:{}".format(stg_num))
                    err_msg = ''
                    if stg_num == 0:
                        err_msg = "[Analysis Error] Initial stable time should be larger than 3sec"
                        #print("[Analysis Error] Stable time should be larger than 3sec")  

                    if stg_num == 1 or stg_num == 2:
                        err_msg = "[Analysis Error] Not a correct CMJ. No eccentric signal detected."
                        #print("[Analysis Error] Not a correct CMJ. No eccentric signal detected.")

                    if stg_num == 3:
                        err_msg = "[Analysis Error] Not a correct CMJ. No jump signal detected."
                        #print("[Analysis Error] Not a correct CMJ. No jump signal detected.")

                    if stg_num == 4:
                        err_msg = "[Analysis Error] Might land outside of force plate. No landing signal detected."
                        #print("[Analysis Error] Might land outside of force plate. No landing signal detected.")

                    print(err_msg)
                    # plot err msg
                    fig = DP.get_fig_time_force_with_err_msg(time_sec_tick, force_N_join, err_msg)
                    fig.savefig( data_dir + '{}_error_message.png'.format(data_name))
                    list_new_error_fig_path += [data_dir + '{}_error_message.png'.format(data_name)]
                    plt.close(fig)

                else:    

                    fly_time_sec, contact_time_sec, TtPF_sec, RFD, PF, jump_height_m, jump_power, time_ecc_sec, time_con_sec, total_time_sec, fly_contact_ratio, RSI_mod, mean_co_force, velocity_pf, force_pf, pVelocity, mean_power_con, time_to_pp_sec, min_velocity, force_at_zero_velocity, mean_ec_con_power, velocity_take_off, imp_ec_deacc_con, RNI, imp_ec_acc, area_force_velocity, ec_displacement_cm, vertical_stiffness = JAM.get_CMJ_record_statistics(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_acc_end, ec_acc_end_tick, ec_low, ec_deacc_start, ec_deacc_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick)

                    # plot
                    fig = DP.get_fig_time_force(data_name, time_sec_tick, force_N_1, force_N_2, force_N_join)
                    fig.savefig( data_dir + '{}_time_force_raw.png'.format(data_name))
                    plt.close(fig)


                    fig = DP.get_fig_CMJ_time_force_notiation(data_name, time_sec_tick, force_N_join, stable_start_tick, stable_end_tick, ec_start_tick, ec_acc_end_tick, ec_deacc_start_tick, pf_tick, air_start_tick, air_end_tick,
                        fly_time_sec, contact_time_sec, TtPF_sec, RFD, jump_height_m, jump_power, PF, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick)
                    fig.savefig( data_dir + '{}_time_force_notation.png'.format(data_name))
                    #plt.show(block=False)
                    #plt.ion()
                    #plt.show()
                    #plt.pause(0.001)

                    list_new_fig_time_force_notiation_path += [data_dir + '{}_time_force_notation.png'.format(data_name)]

                    plt.close(fig)

                    fig = DP.get_fig_CMJ_time_f_a_v_p(data_name, time_sec_tick, force_N_join, a_mss, v_mps, p_watt, p_watt_max_tick, stable_start_tick, stable_end_tick, ec_start_tick, ec_acc_end_tick, ec_deacc_start_tick, pf_tick, air_start_tick, air_end_tick, ec_deacc_end_tick, co_start_tick, co_end_tick)
                    fig.savefig( data_dir + '{}_time_f_a_v_p.png'.format(data_name))
                    plt.close(fig)

                    # dump analysis_results
                    data_analysis_results_path = data_dir + data_name +"_analysis_results.csv"

                    csv_header = []
                    csv_header += ["data_name"]
                    csv_header += ["fly_time_sec"]
                    csv_header += ["contact_time_sec"]
                    csv_header += ["TtPF_sec"]
                    csv_header += ["RFD"]
                    csv_header += ["PF"]
                    csv_header += ["jump_height_m"]
                    csv_header += ["jump_power"]
                            
                    with open(data_analysis_results_path, 'w') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(csv_header)
                        anlysis_result = []
                        for col in range(len(csv_header)):
                            anlysis_result += [eval(csv_header[col])]
                        writer.writerow(anlysis_result)
                        csvfile.close()

            elif 'SJ' in data_name:
                #print("get_SJ_features_of_join_force")
                stg_num, stable_start, stable_end, stable_start_tick, stable_end_tick, co_start, co_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, co_end, co_end_tick = JAM.get_SJ_features_of_join_force(data_name, time_sec_tick, force_N_join)

                a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick, co_end, co_end_tick = JAM.get_SJ_a_v_p(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, co_start, co_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, co_end, co_end_tick)

                if stg_num != 3: # not finish test correctly. should return error message.
                    print("stg_num:{}".format(stg_num))
                    err_msg = ''
                    if stg_num == 0:
                        err_msg = "[Analysis Error] Stable time should >= 3sec or no eccentric contraction"

                    if stg_num == 1:
                        err_msg = "[Analysis Error] Not a correct CMJ. No concentric signal detected."

                    if stg_num == 2:
                        err_msg = "[Analysis Error] Not a correct CMJ. No jump signal detected."
                        #print("[Analysis Error] Not a correct CMJ. No jump signal detected.")

                    if stg_num == 3:
                        err_msg = "[Analysis Error] Might land outside of force plate. No landing signal detected."
                        #print("[Analysis Error] Might land outside of force plate. No landing signal detected.")

                    print(err_msg)
                    # plot err msg
                    fig = DP.get_fig_time_force_with_err_msg(time_sec_tick, force_N_join, err_msg)
                    fig.savefig( data_dir + '{}_error_message.png'.format(data_name))
                    list_new_error_fig_path += [data_dir + '{}_error_message.png'.format(data_name)]
                    plt.close(fig)

                else:    

                    fly_time_sec, contact_time_sec, TtPF_sec, RFD, PF, jump_height_m, jump_power = JAM.get_SJ_record_statistics(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, co_start, co_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick, co_end, co_end_tick)

                    # plot
                    fig = DP.get_fig_time_force(data_name, time_sec_tick, force_N_1, force_N_2, force_N_join)
                    fig.savefig( data_dir + '{}_time_force_raw.png'.format(data_name))
                    plt.close(fig)

                    fig = DP.get_fig_SJ_time_force_notiation(data_name, time_sec_tick, force_N_join, stable_start_tick, stable_end_tick, co_start_tick, pf_tick, air_start_tick, air_end_tick,
                        fly_time_sec, contact_time_sec, TtPF_sec, RFD, jump_height_m, jump_power, PF, co_end_tick)
                    fig.savefig( data_dir + '{}_time_force_notation.png'.format(data_name))

                    list_new_fig_time_force_notiation_path += [data_dir + '{}_time_force_notation.png'.format(data_name)]

                    plt.close(fig)

                    fig = DP.get_fig_SJ_time_f_a_v_p(data_name, time_sec_tick, force_N_join, a_mss, v_mps, p_watt, p_watt_max_tick, stable_start_tick, stable_end_tick, co_start_tick, pf_tick, co_end_tick, air_start_tick, air_end_tick)
                    fig.savefig( data_dir + '{}_time_f_a_v_p.png'.format(data_name))
                    plt.close(fig)
                    
                    # dump analysis_results
                    data_analysis_results_path = data_dir + data_name +"_analysis_results.csv"

                    csv_header = []
                    csv_header += ["data_name"]
                    csv_header += ["fly_time_sec"]
                    csv_header += ["contact_time_sec"]
                    csv_header += ["TtPF_sec"]
                    csv_header += ["RFD"]
                    csv_header += ["PF"]
                    csv_header += ["jump_height_m"]
                    csv_header += ["jump_power"]
                            
                    with open(data_analysis_results_path, 'w') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(csv_header)
                        anlysis_result = []
                        for col in range(len(csv_header)):
                            anlysis_result += [eval(csv_header[col])]
                        writer.writerow(anlysis_result)
                        csvfile.close()


    return list_new_error_fig_path, list_new_fig_time_force_notiation_path, analysis_list








