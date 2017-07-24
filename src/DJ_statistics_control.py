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
import DJ_plot as DJP
import jump_analysis_modules as JAM

def t_sorted(to_be_sorted_list, time_sec_list):

    return [sorted_result for (sorted_total_secs, sorted_result) in sorted(zip(time_sec_list, to_be_sorted_list), key=lambda pair: pair[0])]

def get_DJ_analysis_result_list(file_list):
    result_list = []
    for f_name in file_list:
        if 'analysis_results.csv' in f_name and 'DJ' in f_name:
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

def get_sorted_LDJ_ULDJ_list(s_contact_time_sec,
                               s_fly_contact_ratio,
                               s_RSI_mod,
                               s_date,
                               s_jump_type,
                               s_try_num):
    #print("s_date:{}".format(s_date))
    #print("s_jump_type:{}".format(s_jump_type))
    s_LDJ_contact_time_sec = []
    s_LDJ_fly_contact_ratio = []
    s_LDJ_RSI_mod = []
    s_LDJ_date = []
    s_LDJ_jump_type = []
    s_LDJ_try_num = []
    s_LDJ_epoch_time_sec = []

    s_ULDJ_contact_time_sec = []
    s_ULDJ_fly_contact_ratio = []
    s_ULDJ_RSI_mod = []
    s_ULDJ_date = []
    s_ULDJ_jump_type = []
    s_ULDJ_try_num = []
    s_ULDJ_epoch_time_sec = []

    for i in range(len(s_date)):
        #print("s_jump_type[i]:{}".format(s_jump_type[i]))
        if s_jump_type[i] == 'LDJ':
            s_LDJ_contact_time_sec += [s_contact_time_sec[i]]
            s_LDJ_fly_contact_ratio += [s_fly_contact_ratio[i]]
            s_LDJ_RSI_mod += [s_RSI_mod[i]]
            s_LDJ_date += [s_date[i]]
            s_LDJ_jump_type += [s_jump_type[i]]
            s_LDJ_try_num += [s_try_num[i]]
            s_LDJ_epoch_time_sec += [get_epoch_sec(s_date[i])]

        elif s_jump_type[i] == 'ULDJ':
            #print("s_ULDJ_epoch_time_sec:{}".format(s_ULDJ_epoch_time_sec))
            s_ULDJ_contact_time_sec += [s_contact_time_sec[i]]
            s_ULDJ_fly_contact_ratio += [s_fly_contact_ratio[i]]
            s_ULDJ_RSI_mod += [s_RSI_mod[i]]
            s_ULDJ_date += [s_date[i]]
            s_ULDJ_jump_type += [s_jump_type[i]]
            s_ULDJ_try_num += [s_try_num[i]]
            #print("get_epoch_sec(s_date[i]):{}".format(get_epoch_sec(s_date[i])))
            s_ULDJ_epoch_time_sec += [get_epoch_sec(s_date[i])]

    #print("LDJ_date:{}".format(LDJ_date))
    #print("LDJ_epoch_time_sec:{}".format(LDJ_epoch_time_sec))
    #print("ULDJ_date:{}".format(ULDJ_date))
    #print("ULDJ_epoch_time_sec:{}".format(ULDJ_epoch_time_sec))
    #print("s_LDJ_date:{}".format(s_LDJ_date))
    #print("[c1]s_LDJ_epoch_time_sec:{}".format(s_LDJ_epoch_time_sec))
    #print("s_ULDJ_date:{}".format(s_ULDJ_date))
    #print("[c1]s_ULDJ_epoch_time_sec:{}".format(s_ULDJ_epoch_time_sec))

    # sort data
    # t_sorted(to_be_sorted_list, time_sec_list)
    s_LDJ_contact_time_sec = t_sorted(s_LDJ_contact_time_sec, s_LDJ_epoch_time_sec)
    s_LDJ_fly_contact_ratio = t_sorted(s_LDJ_fly_contact_ratio, s_LDJ_epoch_time_sec)
    s_LDJ_RSI_mod = t_sorted(s_LDJ_RSI_mod, s_LDJ_epoch_time_sec)
    s_LDJ_date = t_sorted(s_LDJ_date, s_LDJ_epoch_time_sec)
    s_LDJ_jump_type = t_sorted(s_LDJ_jump_type, s_LDJ_epoch_time_sec)
    s_LDJ_try_num = t_sorted(s_LDJ_try_num, s_LDJ_epoch_time_sec)
    s_LDJ_epoch_time_sec = t_sorted(s_LDJ_epoch_time_sec, s_LDJ_epoch_time_sec)

    s_ULDJ_contact_time_sec = t_sorted(s_ULDJ_contact_time_sec, s_ULDJ_epoch_time_sec)
    s_ULDJ_fly_contact_ratio = t_sorted(s_ULDJ_fly_contact_ratio, s_ULDJ_epoch_time_sec)
    s_ULDJ_RSI_mod = t_sorted(s_ULDJ_RSI_mod, s_ULDJ_epoch_time_sec)
    s_ULDJ_date = t_sorted(s_ULDJ_date, s_ULDJ_epoch_time_sec)
    s_ULDJ_jump_type = t_sorted(s_ULDJ_jump_type, s_ULDJ_epoch_time_sec)
    s_ULDJ_try_num = t_sorted(s_ULDJ_try_num, s_ULDJ_epoch_time_sec)
    s_ULDJ_epoch_time_sec = t_sorted(s_ULDJ_epoch_time_sec, s_ULDJ_epoch_time_sec)

    #print("s_LDJ_contact_time_sec:{}".format(s_LDJ_contact_time_sec))
    #print("s_LDJ_date:{}".format(s_LDJ_date))
    #print("s_LDJ_epoch_time_sec:{}".format(s_LDJ_epoch_time_sec))
    #print("s_ULDJ_epoch_time_sec:{}".format(s_ULDJ_epoch_time_sec))

    return s_LDJ_contact_time_sec,s_LDJ_fly_contact_ratio,s_LDJ_RSI_mod,s_LDJ_date,s_LDJ_jump_type,s_LDJ_try_num,s_LDJ_epoch_time_sec,s_ULDJ_contact_time_sec,s_ULDJ_fly_contact_ratio,s_ULDJ_RSI_mod,s_ULDJ_date,s_ULDJ_jump_type,s_ULDJ_try_num,s_ULDJ_epoch_time_sec


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
            else:
                avg_time_list += [time_list[i]] # add time
                avg_data_list += [avg_temp] # add avg
                avg_temp = data_list[i]
                avg_count = 1
            if i == len(time_list)-1:
                    avg_data_list += [avg_temp] # add avg

    #print("avg_data_list:{}".format(avg_data_list))
    #print("avg_time_list:{}".format(avg_time_list))
    assert len(avg_time_list) == len(avg_data_list)

    return avg_data_list

def get_avg_LDJ_ULDJ_list(s_LDJ_contact_time_sec,s_LDJ_fly_contact_ratio,s_LDJ_RSI_mod,s_LDJ_date,s_LDJ_jump_type,s_LDJ_try_num,s_LDJ_epoch_time_sec,s_ULDJ_contact_time_sec,s_ULDJ_fly_contact_ratio,s_ULDJ_RSI_mod,s_ULDJ_date,s_ULDJ_jump_type,s_ULDJ_try_num,s_ULDJ_epoch_time_sec):

    s_avg_LDJ_contact_time_sec = get_avg_list(s_LDJ_contact_time_sec, s_LDJ_date)
    s_avg_LDJ_fly_contact_ratio = get_avg_list(s_LDJ_fly_contact_ratio, s_LDJ_date)
    s_avg_LDJ_RSI_mod = get_avg_list(s_LDJ_RSI_mod, s_LDJ_date)
    s_avg_LDJ_date = get_avg_list(s_LDJ_date, s_LDJ_date)
    s_avg_LDJ_epoch_time_sec = get_avg_list(s_LDJ_epoch_time_sec, s_LDJ_date)

    s_avg_ULDJ_contact_time_sec = get_avg_list(s_ULDJ_contact_time_sec, s_ULDJ_date)
    s_avg_ULDJ_fly_contact_ratio = get_avg_list(s_ULDJ_fly_contact_ratio, s_ULDJ_date)
    s_avg_ULDJ_RSI_mod = get_avg_list(s_ULDJ_RSI_mod, s_ULDJ_date)
    s_avg_ULDJ_date = get_avg_list(s_ULDJ_date, s_ULDJ_date)
    s_avg_ULDJ_epoch_time_sec = get_avg_list(s_ULDJ_epoch_time_sec, s_ULDJ_date)
    
    #print("s_avg_LDJ_date:{}".format(s_avg_LDJ_date))
    #print("s_avg_LDJ_epoch_time_sec:{}".format(s_avg_LDJ_epoch_time_sec))

    return s_avg_LDJ_contact_time_sec,s_avg_LDJ_fly_contact_ratio,s_avg_LDJ_RSI_mod,s_avg_LDJ_date,s_avg_LDJ_epoch_time_sec,s_avg_ULDJ_contact_time_sec,s_avg_ULDJ_fly_contact_ratio,s_avg_ULDJ_RSI_mod,s_avg_ULDJ_date,s_avg_ULDJ_epoch_time_sec

def update_user_DJ_statistics(data_dir):

    file_list = os.listdir(data_dir)
    result_list = get_DJ_analysis_result_list(file_list)
    user_statistics_path = data_dir + '____user_DJ_statistics.csv'

    feature_list = ['data_name', 'contact_time_sec', 'fly_contact_ratio', 'RSI_mod', 'date', 'jump_type', 'try_num', 'fly_time_sec', 'jump_height_m']

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



























