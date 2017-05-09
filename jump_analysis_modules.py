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

def get_record_statistics(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_end, ec_end_tick, ec_low, co_start, co_start_tick, co_end, co_end_tick, co_hight, air_start, air_start_tick, air_end, air_end_tick, a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick):

    # statistics
    fly_time_sec = air_end - air_start
    contact_time_sec = air_start - ec_start
    TtPF_sec = co_end - co_start     # time to peak force
    RFD = force_N_join[co_end_tick] / TtPF_sec
    #jump_height = 9.8 * (0.5 * fly_time)**2 + -9.8 * 0.5 * (0.5 * fly_time)**2
    PF = force_N_join[co_end_tick]
    jump_height_m = 0.5 * 9.8 * (0.5 * fly_time_sec)**2
    jump_power = p_watt_max
    #print("co_end_tick:{}".format(co_end_tick))


    print("fly_time_sec:{}".format(fly_time_sec))
    print("contact_time_sec:{}".format(contact_time_sec))
    print("TtPF_sec:{}".format(TtPF_sec))
    print("RFD:{}".format(RFD))
    print("PF:{}".format(PF))
    print("jump_height_m:{}".format(jump_height_m))
    print("jump_power:{}".format(jump_power))

    return fly_time_sec, contact_time_sec, TtPF_sec, RFD, PF, jump_height_m, jump_power

def get_a_v_p(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_end, ec_end_tick, ec_low, co_start, co_start_tick, co_end, co_end_tick, co_hight, air_start, air_start_tick, air_end, air_end_tick):

    # calculate a / v / p # using stable start
    #body_weight = force_N_join[stable_start_tick] / 9.81
    body_weight = np.mean(force_N_join[stable_start_tick:stable_end_tick]) / 9.81
    a_mss = []
    v_mps = []
    p_watt = []

    p_watt_max = -1
    p_watt_max_tick = -1

    for i in range(len(time_sec_tick)):
        
        if i >= stable_start_tick:

            a_mss += [(force_N_join[i] - 9.81*body_weight)/body_weight]

            if len(v_mps) == 0 or i >= air_end_tick:
                v_mps += [0]
            else:
                v_mps += [v_mps[-1] + a_mss[i]*T]

            if len(p_watt) == 0:
                p_watt += [0]
            else:
                p_watt += [(force_N_join[i] - 9.81*body_weight) * v_mps[i]]
        else:
            a_mss += [0]
            v_mps += [0]
            p_watt += [0]

        if p_watt[i] > p_watt_max:
            p_watt_max = p_watt[i]
            p_watt_max_tick = i

        #print("time_sec_tick:{}, force_N_join:{}, a_mss:{}, v_mps:{}, p_watt:{}".format(time_sec_tick[i], force_N_join[i], a_mss[i], v_mps[i], p_watt[i]))

    return a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick


def get_features_of_join_force(data_name, time_sec_tick, force_N_join):

    # start find the special points
    stages = ['stand_by', 'eccentric_stage', 'concetric_stage', 'on_air','landing']
    stg_num = 0

    mean = -1
    stable_length = 1
    stable_time = -1
    diff_pow2_mean = -1
    std = -1

    stable_start = time_sec_tick[0]
    stable_end = -1
    stable_start_tick = 0
    stable_end_tick = -1

    ec_start = -1
    ec_start_tick = -1
    ec_end = -1
    ec_end_tick = -1
    ec_low = -1
    goback_condition_count = 0

    co_start = -1
    co_start_tick = -1
    co_end = -1
    co_end_tick = -1
    co_hight = -1

    air_start = -1
    air_start_tick = -1
    air_end = -1
    air_end_tick = -1

    print("data_name:{}".format(data_name))
    print("[Stage:{}]".format(stages[stg_num]))
    for i in range(len(time_sec_tick)):
        
        # find the starting point of stabd_by stage
        # conditions:
        # 1. force > 100N
        # 2. force moving std < 10N ?
        if force_N_join[i] > 100.0 and stg_num == 0: 
            
            #print("i:{}, time_sec_tick[i]:{}, force_N_join[i]:{}".format(i,time_sec_tick[i], force_N_join[i]))
            #print("stable_start_tick:{}, stable_end_tick:{}, std:{}, stable_length:{}, mean:{}, stable_start:{}, stable_end:{}".format(stable_start_tick, stable_end_tick, std, stable_length, mean, stable_start, stable_end))

            if std < 15.0:
                mean = (force_N_join[i] + mean*(stable_length-1))/stable_length
                diff_pow2_mean = (math.pow(abs(force_N_join[i] - mean), 2) + diff_pow2_mean*(stable_length-1))/stable_length
                if diff_pow2_mean > 0:
                    std = math.sqrt(diff_pow2_mean)
                else:
                    std = -1
                stable_length += 1

                if (mean - force_N_join[i])  < 20 :
                #if True:
                    #stable_max = force_N_join[i]
                    stable_end = time_sec_tick[i]
                    stable_end_tick = i

            else:
                
                stable_time = stable_end - stable_start
                if stable_time > 0.5 and stable_start >= time_sec_tick[0]:
                    #print("stable_start:{}, stable_end:{}, stable_start_tick:{}, stable_end_tick:{}".format(stable_start, stable_end, stable_start_tick, stable_end_tick))
                    # stage change
                    stg_num = 1
                    print("[Stage:{}]".format(stages[stg_num]))
                    ec_start = stable_end
                    ec_start_tick = stable_end_tick
                    ec_low = force_N_join[ec_start_tick]

                else:

                    mean = force_N_join[i]
                    stable_length = 1
                    stable_time = 0
                    diff_pow2_mean = 0
                    std = 0
                    stable_start = time_sec_tick[i]
                    stable_start_tick = i
        elif stg_num == 0:
            mean = force_N_join[i]
            stable_length = 1
            stable_time = 0
            diff_pow2_mean = 0
            std = 0
            stable_start = time_sec_tick[i]
            stable_start_tick = i


        # find the end point of eccentric_stage
        if stg_num == 1:

            # go back to stg_num 0 ?
            if abs(force_N_join[i] - mean) < 10:

                goback_condition_count += 1

                if goback_condition_count >= 100:
                    stg_num = 0
                    mean = force_N_join[i]
                    stable_length = 1
                    stable_time = 0
                    diff_pow2_mean = 0
                    std = 0
                    stable_start = time_sec_tick[i]
                    stable_start_tick = i
                    goback_condition_count = 0
                    print("[go back to stg_num 0] stable_start:{}, stable_start_tick:{}".format(stable_start, stable_start_tick))
            else:
                goback_condition_count = 0

            if force_N_join[i] <= ec_low:
                ec_low = force_N_join[i]
                ec_end = time_sec_tick[i]
                ec_end_tick = i
            elif force_N_join[i] >= force_N_join[ec_start_tick]: # keep searching
                ec_low = force_N_join[ec_start_tick]
            elif force_N_join[i] >= ec_low + 100: # condition of leaving eccentric_stage
                # stage change
                stg_num = 2
                print("[Stage:{}]".format(stages[stg_num]))
                co_start = ec_end
                co_start_tick = ec_end_tick
                co_hight = force_N_join[co_start_tick]

        # find the end point of concetric_stage
        if stg_num == 2:
            #print("time_sec_tick[i]:{}, force_N_join[i]:{}".format(time_sec_tick[i], force_N_join[i]))
            if force_N_join[i] >= co_hight:
                co_hight = force_N_join[i]
                co_end = time_sec_tick[i]
                co_end_tick = i
            #elif force_N_join[i] <= force_N_join[co_start_tick]: # keep searching
            #    co_hight = force_N_join[co_start_tick]
            elif force_N_join[i] <= 20: # condition of leaving concetric_stage
                stg_num = 3
                print("[Stage:{}]".format(stages[stg_num]))
                air_start = time_sec_tick[i]
                air_start_tick = i

        # find the end point of on air stage
        if stg_num == 3:
            #print("time_sec_tick[i]:{}, force_N_join[i]:{}".format(time_sec_tick[i], force_N_join[i]))
            if force_N_join[i] <= 100:
                air_end = time_sec_tick[i]
                air_end_tick = i
            else: # condition of leaving air stage
                stg_num = 4
                print("[Stage:{}]".format(stages[stg_num]))

    print("stable_start_tick:{}, stable_end_tick:{}".format(stable_start_tick, stable_end_tick))
    print("stable_start:{}, stable_end:{}".format(stable_start, stable_end))
    print("ec_start_tick:{}, ec_end_tick:{}".format(ec_start_tick, ec_end_tick))
    print("co_start_tick:{}, co_end_tick:{}".format(co_start_tick, co_end_tick))
    print("air_start_tick:{}, air_end_tick:{}".format(air_start_tick, air_end_tick))

    return stg_num, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_end, ec_end_tick, ec_low, co_start, co_start_tick, co_end, co_end_tick, co_hight, air_start, air_start_tick, air_end, air_end_tick



def get_analysis_list(file_list):

    csv_list = []
    plot_list = []
    for f in file_list:
        if ('.csv' in f )and ('analysis_results' not in f) and ('user_statistics' not in f) and ('dual_input' not in f):
            csv_list += [f.replace('.csv','')]

        if '.png' in f:
            plot_list += [f]

    #print("[Jump Analysis Modules] csv_list:{}".format(csv_list))
    #print("[Jump Analysis Modules] plot_list:{}".format(plot_list))

    analysis_list = []
    for c_name in csv_list:
        output_detected = 0
        for p_name in plot_list:
            if c_name in p_name:
                output_detected = 1
        if output_detected == 0:
            analysis_list += [c_name]
    print("[Jump Analysis Modules] analysis_list:{}".format(analysis_list))

    return analysis_list


