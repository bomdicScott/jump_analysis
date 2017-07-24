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

        time_ecc_sec = row['time_ecc_sec']
        time_con_sec = row['time_con_sec']
        total_time_sec = row['total_time_sec']
        fly_contact_ratio = row['fly_contact_ratio']
        RSI_mod = row['RSI_mod']
        mean_co_force = row['mean_co_force']
        velocity_pf = row['velocity_pf']
        force_pf = row['force_pf']
        pVelocity = row['pVelocity']
        mean_power_con = row['mean_power_con']
        time_to_pp_sec = row['time_to_pp_sec']
        min_velocity = row['min_velocity']
        force_at_zero_velocity = row['force_at_zero_velocity']
        mean_ec_con_power = row['mean_ec_con_power']
        velocity_take_off = row['velocity_take_off']
        imp_ec_deacc_con = row['imp_ec_deacc_con']
        RNI = row['RNI']
        imp_ec_acc = row['imp_ec_acc']
        area_force_velocity = row['area_force_velocity']
        ec_displacement_cm = row['ec_displacement_cm']
        vertical_stiffness = row['vertical_stiffness']

        RFD_20ms = row['RFD_20ms']
        RFD_30ms = row['RFD_30ms']
        RFD_50ms = row['RFD_50ms']
        RFD_90ms = row['RFD_90ms']
        RFD_100ms = row['RFD_100ms']
        RFD_150ms = row['RFD_150ms']
        RFD_200ms = row['RFD_200ms']
        RFD_250ms = row['RFD_250ms']

        pRFD = row['pRFD']
        pRFD_sec = row['pRFD_sec']
        
        force_pp = row['force_pp']
        velocity_pp = row['velocity_pp']
        time_ecc_acc_sec = row['time_ecc_acc_sec']
        time_ecc_deacc_sec = row['time_ecc_deacc_sec']

    return data_name,contact_time_sec,TtPF_sec,RFD,jump_height_m,jump_power, fly_time_sec, PF, time_ecc_sec, time_con_sec, total_time_sec, fly_contact_ratio, RSI_mod, mean_co_force, velocity_pf, force_pf, pVelocity, mean_power_con, time_to_pp_sec, min_velocity, force_at_zero_velocity, mean_ec_con_power, velocity_take_off, imp_ec_deacc_con, RNI, imp_ec_acc, area_force_velocity, ec_displacement_cm, vertical_stiffness, RFD_20ms, RFD_30ms, RFD_50ms, RFD_90ms, RFD_100ms, RFD_150ms, RFD_200ms, RFD_250ms, pRFD, pRFD_sec, force_pp, velocity_pp, time_ecc_acc_sec, time_ecc_deacc_sec

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

    s_time_ecc_sec = []
    s_time_con_sec = []
    s_total_time_sec = []
    s_fly_contact_ratio = []
    s_RSI_mod = []
    s_mean_co_force = []
    s_velocity_pf = []
    s_force_pf = []
    s_pVelocity = []
    s_mean_power_con = []
    s_time_to_pp_sec = []
    s_min_velocity = []
    s_force_at_zero_velocity = []
    s_mean_ec_con_power = []
    s_velocity_take_off = []
    s_imp_ec_deacc_con = []
    s_RNI = []
    s_imp_ec_acc = []
    s_area_force_velocity = []
    s_ec_displacement_cm = []
    s_vertical_stiffness = []

    s_RFD_20ms = []
    s_RFD_30ms = []
    s_RFD_50ms = []
    s_RFD_90ms = []
    s_RFD_100ms = []
    s_RFD_150ms = []
    s_RFD_200ms = []
    s_RFD_250ms = []

    s_pRFD = []
    s_pRFD_sec = []


    s_force_pp = []
    s_velocity_pp = []
    s_time_ecc_acc_sec = []
    s_time_ecc_deacc_sec = []

    for result_name in result_list:
        result_path = data_dir + result_name

        if os.path.exists(result_path):
            data_name,contact_time_sec,TtPF_sec,RFD,jump_height_m,jump_power, fly_time_sec, PF, time_ecc_sec, time_con_sec, total_time_sec, fly_contact_ratio, RSI_mod, mean_co_force, velocity_pf, force_pf, pVelocity, mean_power_con, time_to_pp_sec, min_velocity, force_at_zero_velocity, mean_ec_con_power, velocity_take_off, imp_ec_deacc_con, RNI, imp_ec_acc, area_force_velocity, ec_displacement_cm, vertical_stiffness, RFD_20ms, RFD_30ms, RFD_50ms, RFD_90ms, RFD_100ms, RFD_150ms, RFD_200ms, RFD_250ms, pRFD, pRFD_sec, force_pp, velocity_pp, time_ecc_acc_sec, time_ecc_deacc_sec = read_analysis_result(result_path)

            s_data_name += [data_name]
            s_contact_time_sec += [contact_time_sec]
            s_TtPF_sec += [TtPF_sec]
            s_RFD += [RFD]
            s_jump_height_m += [jump_height_m]
            s_jump_power += [jump_power]
            s_fly_time_sec += [fly_time_sec]
            s_PF += [PF]

            s_time_ecc_sec += [time_ecc_sec]
            s_time_con_sec += [time_con_sec]
            s_total_time_sec += [total_time_sec]
            s_fly_contact_ratio += [fly_contact_ratio]
            s_RSI_mod += [RSI_mod]
            s_mean_co_force += [mean_co_force]
            s_velocity_pf += [velocity_pf]
            s_force_pf += [force_pf]
            s_pVelocity += [pVelocity]
            s_mean_power_con += [mean_power_con]
            s_time_to_pp_sec += [time_to_pp_sec]
            s_min_velocity += [min_velocity]
            s_force_at_zero_velocity += [force_at_zero_velocity]
            s_mean_ec_con_power += [mean_ec_con_power]
            s_velocity_take_off += [velocity_take_off]
            s_imp_ec_deacc_con += [imp_ec_deacc_con]
            s_RNI += [RNI]
            s_imp_ec_acc += [imp_ec_acc]
            s_area_force_velocity += [area_force_velocity]
            s_ec_displacement_cm += [ec_displacement_cm]
            s_vertical_stiffness += [vertical_stiffness]

            s_RFD_20ms += [RFD_20ms]
            s_RFD_30ms += [RFD_30ms]
            s_RFD_50ms += [RFD_50ms]
            s_RFD_90ms += [RFD_90ms]
            s_RFD_100ms += [RFD_100ms]
            s_RFD_150ms += [RFD_150ms]
            s_RFD_200ms += [RFD_200ms]
            s_RFD_250ms += [RFD_250ms]

            s_pRFD += [pRFD]
            s_pRFD_sec += [pRFD_sec]

            s_force_pp += [force_pp]
            s_velocity_pp += [velocity_pp]
            s_time_ecc_acc_sec += [time_ecc_acc_sec]
            s_time_ecc_deacc_sec += [time_ecc_deacc_sec]

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

    csv_header += ["s_time_ecc_sec"]
    csv_header += ["s_time_con_sec"]
    csv_header += ["s_total_time_sec"]
    csv_header += ["s_fly_contact_ratio"]
    csv_header += ["s_RSI_mod"]
    csv_header += ["s_mean_co_force"]
    csv_header += ["s_velocity_pf"]
    csv_header += ["s_force_pf"]
    csv_header += ["s_pVelocity"]
    csv_header += ["s_mean_power_con"]
    csv_header += ["s_time_to_pp_sec"]
    csv_header += ["s_min_velocity"]
    csv_header += ["s_force_at_zero_velocity"]
    csv_header += ["s_mean_ec_con_power"]
    csv_header += ["s_velocity_take_off"]
    csv_header += ["s_imp_ec_deacc_con"]
    csv_header += ["s_RNI"]
    csv_header += ["s_imp_ec_acc"]
    csv_header += ["s_area_force_velocity"]
    csv_header += ["s_ec_displacement_cm"]
    csv_header += ["s_vertical_stiffness"]

    csv_header += ["s_RFD_20ms"]
    csv_header += ["s_RFD_30ms"]
    csv_header += ["s_RFD_50ms"]
    csv_header += ["s_RFD_90ms"]
    csv_header += ["s_RFD_100ms"]
    csv_header += ["s_RFD_150ms"]
    csv_header += ["s_RFD_200ms"]
    csv_header += ["s_RFD_250ms"]
    csv_header += ["s_pRFD"]
    csv_header += ["s_pRFD_sec"]

    csv_header += ["s_force_pp"]
    csv_header += ["s_velocity_pp"]
    csv_header += ["s_time_ecc_acc_sec"]
    csv_header += ["s_time_ecc_deacc_sec"]

        
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
        fig = CMJP.get_fig_LCMJ_analysis(s_LCMJ_contact_time_sec,
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
        fig = CMJP.get_fig_ULCMJ_analysis(s_ULCMJ_contact_time_sec,
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
        fig = CMJP.get_fig_CMJ_compare(s_avg_ULCMJ_date, s_avg_ULCMJ_epoch_time_sec, s_avg_ULCMJ_jump_height_m, s_avg_LCMJ_date, s_avg_LCMJ_epoch_time_sec, s_avg_LCMJ_jump_height_m)
        fig.savefig( data_dir + '____CMJ_compare.png'.format(data_name))
        plt.close(fig)

