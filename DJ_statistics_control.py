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


def read_analysis_result(result_path):
    
    #print("result_path:{}".format(result_path))

    f = open(result_path, 'rU')
    for row in csv.DictReader(f): 
        data_name = row['data_name']
        contact_time_sec = row['contact_time_sec']
        fly_contact_ratio = row['fly_contact_ratio']
        RSI_mod = row['RSI_mod']
        fly_time_sec = row['fly_time_sec']

    return data_name,contact_time_sec,fly_contact_ratio,RSI_mod, fly_time_sec

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
            #if len(time_list) == 1: # has only one element
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

    s_data_name = []
    s_contact_time_sec = []
    s_fly_contact_ratio = []
    s_RSI_mod = []
    s_date = []
    s_jump_type = []
    s_try_num = []
    s_fly_time_sec = []

    for result_name in result_list:
        result_path = data_dir + result_name

        if os.path.exists(result_path):
            data_name,contact_time_sec,fly_contact_ratio,RSI_mod, fly_time_sec = read_analysis_result(result_path)

            s_data_name += [data_name]
            s_contact_time_sec += [contact_time_sec]
            s_fly_contact_ratio += [fly_contact_ratio]
            s_RSI_mod += [RSI_mod]
            s_fly_time_sec += [fly_time_sec]

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
    csv_header += ["s_fly_contact_ratio"]
    csv_header += ["s_RSI_mod"]
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


    # LDJ / ULDJ list
    s_LDJ_contact_time_sec,s_LDJ_fly_contact_ratio,s_LDJ_RSI_mod,s_LDJ_date,s_LDJ_jump_type,s_LDJ_try_num,s_LDJ_epoch_time_sec,s_ULDJ_contact_time_sec,s_ULDJ_fly_contact_ratio,s_ULDJ_RSI_mod,s_ULDJ_date,s_ULDJ_jump_type,s_ULDJ_try_num,s_ULDJ_epoch_time_sec = get_sorted_LDJ_ULDJ_list(s_contact_time_sec,
                               s_fly_contact_ratio,
                               s_RSI_mod,
                               s_date,
                               s_jump_type,
                               s_try_num)

    #print("s_date:{}".format(s_date))
    #print("s_ULDJ_epoch_time_sec:{}".format(s_ULDJ_epoch_time_sec))

    # get avg LDJ / ULDJ list
    s_avg_LDJ_contact_time_sec,s_avg_LDJ_fly_contact_ratio,s_avg_LDJ_RSI_mod,s_avg_LDJ_date,s_avg_LDJ_epoch_time_sec,s_avg_ULDJ_contact_time_sec,s_avg_ULDJ_fly_contact_ratio,s_avg_ULDJ_RSI_mod,s_avg_ULDJ_date,s_avg_ULDJ_epoch_time_sec = get_avg_LDJ_ULDJ_list(s_LDJ_contact_time_sec,s_LDJ_fly_contact_ratio,s_LDJ_RSI_mod,s_LDJ_date,s_LDJ_jump_type,s_LDJ_try_num,s_LDJ_epoch_time_sec,s_ULDJ_contact_time_sec,s_ULDJ_fly_contact_ratio,s_ULDJ_RSI_mod,s_ULDJ_date,s_ULDJ_jump_type,s_ULDJ_try_num,s_ULDJ_epoch_time_sec)
    




    # plot fig
    if s_LDJ_epoch_time_sec != []:
        fig = DJP.get_fig_LDJ_analysis(s_LDJ_contact_time_sec,
                              s_LDJ_fly_contact_ratio,
                              s_LDJ_RSI_mod,
                              s_LDJ_date,
                              s_LDJ_epoch_time_sec,
                              s_avg_LDJ_contact_time_sec,
                              s_avg_LDJ_fly_contact_ratio,
                              s_avg_LDJ_RSI_mod,
                              s_avg_LDJ_date,
                              s_avg_LDJ_epoch_time_sec)
        fig.savefig( data_dir + '____LDJ_analysis.png'.format(data_name))
        plt.close(fig)
    #print("s_ULDJ_epoch_time_sec:{}".format(s_ULDJ_epoch_time_sec))
    if s_ULDJ_epoch_time_sec != []:
        fig = DJP.get_fig_ULDJ_analysis(s_ULDJ_contact_time_sec,
                           s_ULDJ_fly_contact_ratio,
                           s_ULDJ_RSI_mod,
                           s_ULDJ_date,
                           s_ULDJ_epoch_time_sec,
                           s_avg_ULDJ_contact_time_sec,
                           s_avg_ULDJ_fly_contact_ratio,
                           s_avg_ULDJ_RSI_mod,
                           s_avg_ULDJ_date,
                           s_avg_ULDJ_epoch_time_sec)
        fig.savefig( data_dir + '____ULDJ_analysis.png'.format(data_name))
        plt.close(fig)


























