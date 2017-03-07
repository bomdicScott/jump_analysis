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

def get_analysis_result_list(file_list):
    result_list = []
    for f_name in file_list:
        if 'analysis_results.csv' in f_name:
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

    return data_name,contact_time_sec,TtPF_sec,RFD,jump_height_m,jump_power

def get_epoch_sec(YMD_string):
    epoch_time = dateutil.parser.parse("1970-01-01T00:00:00Z")
    Y = YMD_string[0:4]
    M = YMD_string[5:6]
    D = YMD_string[7:8]
    time = dateutil.parser.parse("{}-{}-{}T00:00:00Z".format(Y,M,D))
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
            s_ULCMJ_contact_time_sec += [s_contact_time_sec[i]]
            s_ULCMJ_TtPF_sec += [s_TtPF_sec[i]]
            s_ULCMJ_RFD += [s_RFD[i]]
            s_ULCMJ_jump_height_m += [s_jump_height_m[i]]
            s_ULCMJ_jump_power += [s_jump_power[i]]
            s_ULCMJ_date += [s_date[i]]
            s_ULCMJ_jump_type += [s_jump_type[i]]
            s_ULCMJ_try_num += [s_try_num[i]]
            s_ULCMJ_epoch_time_sec += [get_epoch_sec(s_date[i])]

    #print("LCMJ_date:{}".format(LCMJ_date))
    #print("LCMJ_epoch_time_sec:{}".format(LCMJ_epoch_time_sec))
    #print("ULCMJ_date:{}".format(ULCMJ_date))
    #print("ULCMJ_epoch_time_sec:{}".format(ULCMJ_epoch_time_sec))

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

    s_ULCMJ_contact_time_sec = t_sorted(s_ULCMJ_contact_time_sec, s_LCMJ_epoch_time_sec)
    s_ULCMJ_TtPF_sec = t_sorted(s_ULCMJ_TtPF_sec, s_LCMJ_epoch_time_sec)
    s_ULCMJ_RFD = t_sorted(s_ULCMJ_RFD, s_LCMJ_epoch_time_sec)
    s_ULCMJ_jump_height_m = t_sorted(s_ULCMJ_jump_height_m, s_LCMJ_epoch_time_sec)
    s_ULCMJ_jump_power = t_sorted(s_ULCMJ_jump_power, s_LCMJ_epoch_time_sec)
    s_ULCMJ_date = t_sorted(s_ULCMJ_date, s_LCMJ_epoch_time_sec)
    s_ULCMJ_jump_type = t_sorted(s_ULCMJ_jump_type, s_LCMJ_epoch_time_sec)
    s_ULCMJ_try_num = t_sorted(s_ULCMJ_try_num, s_LCMJ_epoch_time_sec)
    s_ULCMJ_epoch_time_sec = t_sorted(s_ULCMJ_epoch_time_sec, s_LCMJ_epoch_time_sec)

    print("s_LCMJ_contact_time_sec:{}".format(s_LCMJ_contact_time_sec))
    print("s_LCMJ_date:{}".format(s_LCMJ_date))

    return s_LCMJ_contact_time_sec,s_LCMJ_TtPF_sec,s_LCMJ_RFD,s_LCMJ_jump_height_m,s_LCMJ_jump_power,s_LCMJ_date,s_LCMJ_jump_type,s_LCMJ_try_num,s_LCMJ_epoch_time_sec,s_ULCMJ_contact_time_sec,s_ULCMJ_TtPF_sec,s_ULCMJ_RFD,s_ULCMJ_jump_height_m,s_ULCMJ_jump_power,s_ULCMJ_date,s_ULCMJ_jump_type,s_ULCMJ_try_num,s_ULCMJ_epoch_time_sec

def get_avg_list(data_list, time_list):
    avg_data_list = []
    avg_time_list = []
    for i in range(len(time_list)):
        data_list[i] = float(data_list[i])
        if avg_time_list == []:
            avg_time_list += [time_list[i]] # add time
            avg_temp = data_list[i]
            avg_count = 1
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
    
    print("s_avg_LCMJ_date:{}".format(s_avg_LCMJ_date))
    print("s_avg_LCMJ_epoch_time_sec:{}".format(s_avg_LCMJ_epoch_time_sec))
    print("s_avg_LCMJ_jump_height_m:{}".format(s_avg_LCMJ_jump_height_m))

    return s_avg_LCMJ_contact_time_sec,s_avg_LCMJ_TtPF_sec,s_avg_LCMJ_RFD,s_avg_LCMJ_jump_height_m,s_avg_LCMJ_jump_power,s_avg_LCMJ_date,s_avg_LCMJ_epoch_time_sec,s_avg_ULCMJ_contact_time_sec,s_avg_ULCMJ_TtPF_sec,s_avg_ULCMJ_RFD,s_avg_ULCMJ_jump_height_m,s_avg_ULCMJ_jump_power,s_avg_ULCMJ_date,s_avg_ULCMJ_epoch_time_sec

def update_user_statistics(data_dir):
    
    file_list = os.listdir(data_dir)
    result_list = get_analysis_result_list(file_list)
    user_statistics_path = data_dir + '____user_statistics.csv'

    s_data_name = []
    s_contact_time_sec = []
    s_TtPF_sec = []
    s_RFD = []
    s_jump_height_m = []
    s_jump_power = []
    s_date = []
    s_jump_type = []
    s_try_num = []

    for result_name in result_list:
        result_path = data_dir + result_name

        if os.path.exists(result_path):
            data_name,contact_time_sec,TtPF_sec,RFD,jump_height_m,jump_power = read_analysis_result(result_path)

            s_data_name += [data_name]
            s_contact_time_sec += [contact_time_sec]
            s_TtPF_sec += [TtPF_sec]
            s_RFD += [RFD]
            s_jump_height_m += [jump_height_m]
            s_jump_power += [jump_power]

            # if data_name uses standard format
            data_name_split = data_name.split('_')
            print("data_name_split:{}".format(data_name_split))

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
    csv_header += ["s_TtPF_sec"]
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

        fig = DP.get_fig_CMJ_compare(s_avg_ULCMJ_date, s_avg_ULCMJ_epoch_time_sec, s_avg_ULCMJ_jump_height_m, s_avg_LCMJ_date, s_avg_LCMJ_epoch_time_sec, s_avg_LCMJ_jump_height_m)
        fig.savefig( data_dir + '____CMJ_compare.png'.format(data_name))
        plt.close(fig)




def single_user_analysis(data_dir):

    file_list = os.listdir(data_dir)
    analysis_list = JAM.get_analysis_list(file_list)

    # test only section
    #analysis_list = ['Lt1']
    #analysis_list = ['ULt1']
    #if 'Gaby' in data_dir:
    #    analysis_list = ['Lg1']
    #if 'Tom' in data_dir:
    #    analysis_list = ['Lt1']

    if analysis_list == []:
        print("[No new data waited for analysis] Please copy new force plate csv file into data folder.")
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
                plt.close(fig)

                #sys.exit()
            else:

                stg_num, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_end, ec_end_tick, ec_low, co_start, co_start_tick, co_end, co_end_tick, co_hight, air_start, air_start_tick, air_end, air_end_tick = JAM.get_features_of_join_force(data_name, time_sec_tick, force_N_join)

                a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick = JAM.get_a_v_p(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_end, ec_end_tick, ec_low, co_start, co_start_tick, co_end, co_end_tick, co_hight, air_start, air_start_tick, air_end, air_end_tick)


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
                    plt.close(fig)

                else:    

                    fly_time_sec, contact_time_sec, TtPF_sec, RFD, jump_height_m, jump_power = JAM.get_record_statistics(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_end, ec_end_tick, ec_low, co_start, co_start_tick, co_end, co_end_tick, co_hight, air_start, air_start_tick, air_end, air_end_tick, a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick)

                    # plot
                    fig = DP.get_fig_time_force(data_name, time_sec_tick, force_N_1, force_N_2, force_N_join)
                    fig.savefig( data_dir + '{}_time_force_raw.png'.format(data_name))
                    plt.close(fig)


                    fig = DP.get_fig_time_force_notiation(data_name, time_sec_tick, force_N_join, stable_start_tick, stable_end_tick, ec_start_tick, ec_end_tick, co_start_tick, co_end_tick, air_start_tick, air_end_tick,
                        fly_time_sec, contact_time_sec, TtPF_sec, RFD, jump_height_m, jump_power)
                    fig.savefig( data_dir + '{}_time_force_notation.png'.format(data_name))
                    plt.close(fig)

                    fig = DP.get_fig_time_f_a_v_p(data_name, time_sec_tick, force_N_join, a_mss, v_mps, p_watt, co_end_tick, p_watt_max_tick)
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








