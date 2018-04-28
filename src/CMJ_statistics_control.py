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
import copy as cp
from collections import defaultdict

import data_parsing_modules as DPM
import data_plot as DP
import CMJ_plot as CMJP
import jump_analysis_modules as JAM

def t_sorted(to_be_sorted_list, time_sec_list):

    return [sorted_result for (sorted_total_secs, sorted_result) in sorted(zip(time_sec_list, to_be_sorted_list), key=lambda pair: pair[0])]

def get_CMJ_analysis_result_list(file_list):
    result_list = []
    for f_name in file_list:
        if 'analysis_results.csv' in f_name and 'CMJ' in f_name:
            result_list += [f_name]
    #print("result_list:{}".format(result_list))

    return result_list

def read_analysis_result_d(result_path, feature_list):

    feature_d = {}
    f = open(result_path, 'rU')
    for row in csv.DictReader(f): 
        for feature in feature_list:
            if (
                feature != 'date' and 
                feature != 'jump_type' and 
                feature != 'try_num'
               ):
                feature_d[feature] = row[feature]
    
    data_name_split = feature_d['data_name'].split('_')
    if len(data_name_split) == 4 and len(data_name_split[1]) == 8 and data_name_split[1][0:2] == '20' and 't' in data_name_split[3]:
        feature_d['date'] = data_name_split[1]
        feature_d['jump_type'] = data_name_split[2]
        feature_d['try_num'] = data_name_split[3]
    else:
        feature_d['date'] = ['NA']
        feature_d['jump_type'] = ['NA']
        feature_d['try_num'] = ['NA']

    return feature_d

def get_epoch_sec(YMD_string):
    epoch_time = dateutil.parser.parse("1970-01-01T00:00:00Z")
    Y = YMD_string[0:4]
    M = YMD_string[4:6]
    D = YMD_string[6:8]
    time = dateutil.parser.parse("{}-{}-{}T00:00:00Z".format(Y,M,D))
    #print("YMD_string:{}".format(YMD_string))
    #print("time:{}".format(time))
    return int((time - epoch_time).total_seconds())

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
    print("data_list:{}".format(data_list))
    print("time_list:{}".format(time_list))
    for i in range(len(time_list)):
        data_list[i] = float(data_list[i])
        if avg_time_list == []:
            #print("[f]avg_data_list:{}".format(avg_data_list))
            #print("[f]avg_time_list:{}".format(avg_time_list))
            avg_time_list += [time_list[i]] # add time
            avg_temp = data_list[i]
            avg_count = 1
            if len(time_list) == 1: # has only one element
                avg_data_list += [avg_temp] # add avg and quit for
        else:
            #print("[p]avg_data_list:{}".format(avg_data_list))
            #print("[p]avg_time_list:{}".format(avg_time_list))
            if time_list[i] == avg_time_list[-1]:
                avg_count += 1
                avg_temp = (avg_temp * (avg_count-1) + data_list[i])/avg_count
            else:
                avg_time_list += [time_list[i]] # add time
                avg_data_list += [avg_temp] # add avg
                avg_temp = data_list[i]
                avg_count = 1
            if i == len(time_list)-1:
                    avg_data_list += [avg_temp] # add avg

    print("avg_data_list:{}".format(avg_data_list))
    print("avg_time_list:{}".format(avg_time_list))
    assert len(avg_time_list) == len(avg_data_list)

    return avg_data_list

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

def update_user_CMJ_statistics(data_dir):

    file_list = os.listdir(data_dir)
    result_list = get_CMJ_analysis_result_list(file_list)
    user_statistics_path = data_dir + '____user_CMJ_statistics.csv'

    feature_list = ['data_name', 'contact_time_sec', 'TtPF_sec', 'RFD', 'jump_height_m', 'jump_height_m_by_v', 'jump_power', 'date', 'jump_type', 'try_num', 'fly_time_sec', 'PF', 'time_ecc_sec', 'time_con_sec', 'total_time_sec', 'fly_contact_ratio', 'RSI_mod', 'mean_co_force', 'velocity_pf', 'force_pf', 'pVelocity', 'mean_power_con', 'time_to_pp_sec', 'min_velocity', 'force_at_zero_velocity', 'mean_ec_con_power', 'velocity_take_off', 'imp_ec_deacc_con', 'imp_ec_deacc','imp_con', 'RNI', 'imp_ec_acc', 'area_force_velocity', 'ec_displacement_cm', 'vertical_stiffness', 'RFD_20ms', 'RFD_30ms', 'RFD_50ms', 'RFD_90ms', 'RFD_100ms', 'RFD_150ms', 'RFD_200ms', 'RFD_250ms', 'pRFD', 'pRFD_sec', 'force_pp', 'velocity_pp', 'time_ecc_acc_sec', 'time_ecc_deacc_sec', 'ec_low', 'ec_low_tick', 'ec_start_tick', 'air_start_tick']

    s_feature_d = defaultdict(list)
    for feature in feature_list:
        s_feature_d['s_'+feature] = []
    print("s_feature_d:{}".format(s_feature_d))

    for result_name in result_list:
        result_path = data_dir + result_name

        if os.path.exists(result_path):
            feature_d = read_analysis_result_d(result_path, feature_list)
            print("feature_d:{}".format(feature_d))

            for feature in feature_list:
                #print("s_feature_d['s_'+feature]:{}".format(s_feature_d['s_'+feature]))
                s_feature_d['s_'+feature] += [feature_d[feature]]

    print("s_feature_d:{}".format(s_feature_d))

    csv_header = []
    for feature in feature_list:
        csv_header += ['s_'+feature]

    with open(user_statistics_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(s_feature_d['s_data_name'])+1):
            data = []
            if row == 0:
                data = csv_header
            else:
                for col in range(len(csv_header)):
                    #print("csv_header[col]:{}".format((csv_header[col])))
                    #print("len:{}".format(len(eval(csv_header[col]))))
                    data += [s_feature_d[csv_header[col]][row-1]]
            writer.writerow(data)
        csvfile.close()


