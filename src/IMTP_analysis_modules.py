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

def get_IMTP_record_statistics(T, time_sec_tick, force_N_join, stable_start, stable_start_tick, stable_end, stable_end_tick, pull_start, pull_start_tick, pf, pf_tick, pull_end, pull_end_tick):

    # statistics
    TtPF_sec = pf - pull_start     # time to peak force
    RFD = (force_N_join[pf_tick] - force_N_join[pull_start_tick]) / TtPF_sec

    # extended RFD calculation
    RFD_20ms = -1
    RFD_30ms = -1
    RFD_50ms = -1
    RFD_90ms = -1
    RFD_100ms = -1
    RFD_150ms = -1
    RFD_200ms = -1
    RFD_250ms = -1
    if (pf_tick - pull_start_tick) >= 20: # 20ms
        RFD_20ms = (force_N_join[pull_start_tick+20] - force_N_join[pull_start_tick]) / (20.0 * 0.001)
    if (pf_tick - pull_start_tick) >= 30: # 30ms
        RFD_30ms = (force_N_join[pull_start_tick+30] - force_N_join[pull_start_tick]) / (30.0 * 0.001)
    if (pf_tick - pull_start_tick) >= 50: # 50ms
        RFD_50ms = (force_N_join[pull_start_tick+50] - force_N_join[pull_start_tick]) / (50.0 * 0.001)
    if (pf_tick - pull_start_tick) >= 90: # 90ms
        RFD_90ms = (force_N_join[pull_start_tick+90] - force_N_join[pull_start_tick]) / (90.0 * 0.001)
    if (pf_tick - pull_start_tick) >= 100: # 100ms
        RFD_100ms = (force_N_join[pull_start_tick+100] - force_N_join[pull_start_tick]) / (100.0 * 0.001)
    if (pf_tick - pull_start_tick) >= 150: # 150ms
        RFD_150ms = (force_N_join[pull_start_tick+150] - force_N_join[pull_start_tick]) / (150.0 * 0.001)
    if (pf_tick - pull_start_tick) >= 200: # 200ms
        RFD_200ms = (force_N_join[pull_start_tick+200] - force_N_join[pull_start_tick]) / (200.0 * 0.001)
    if (pf_tick - pull_start_tick) >= 250: # 250ms
        RFD_250ms = (force_N_join[pull_start_tick+250] - force_N_join[pull_start_tick]) / (250.0 * 0.001)

    PF = force_N_join[pf_tick]

    # peak RFD
    pRFD = -1
    pRFD_sec = -1
    avg_ticks = 20 # ms

    for i in range(pull_start_tick, pf_tick - avg_ticks, 1):
        instant_RFD = (force_N_join[i+avg_ticks] - force_N_join[i])/float(avg_ticks)*1000.0
        if instant_RFD > pRFD:
            pRFD = instant_RFD
            pRFD_sec = time_sec_tick[i]
    print("pRFD:{}".format(pRFD))
    print("pRFD_sec:{}".format(pRFD_sec))
    print("pull_start_tick:{}".format(pull_start_tick))

    # impulse calculation
    imp_20ms = -1
    imp_30ms = -1
    imp_50ms = -1
    imp_90ms = -1
    imp_100ms = -1
    imp_150ms = -1
    imp_200ms = -1
    imp_250ms = -1

    body_weight_N = np.mean(force_N_join[stable_start_tick:stable_end_tick])
    print("T:{}, body_weight_N:{}".format(T, body_weight_N))

    #force_per_kg = (PF - body_weight_N) / (body_weight_N/9.8)

    if (pull_end_tick - pull_start_tick) >= 20: # 20ms
        imp_20ms = 0
        for i in range(pull_start_tick, pull_start_tick+20, 1):
            imp_20ms += (force_N_join[i] - body_weight_N) * T
         
    if (pull_end_tick - pull_start_tick) >= 30: # 30ms
        imp_30ms = 0
        for i in range(pull_start_tick, pull_start_tick+30, 1):
            imp_30ms += (force_N_join[i] - body_weight_N) * T

    if (pull_end_tick - pull_start_tick) >= 50: # 50ms
        imp_50ms = 0
        for i in range(pull_start_tick, pull_start_tick+50, 1):
            imp_50ms += (force_N_join[i] - body_weight_N) * T

    if (pull_end_tick - pull_start_tick) >= 90: # 90ms
        imp_90ms = 0
        for i in range(pull_start_tick, pull_start_tick+90, 1):
            imp_90ms += (force_N_join[i] - body_weight_N) * T

    if (pull_end_tick - pull_start_tick) >= 100: # 100ms
        imp_100ms = 0
        for i in range(pull_start_tick, pull_start_tick+100, 1):
            imp_100ms += (force_N_join[i] - body_weight_N) * T

    if (pull_end_tick - pull_start_tick) >= 150: # 150ms
        imp_150ms = 0
        for i in range(pull_start_tick, pull_start_tick+150, 1):
            imp_150ms += (force_N_join[i] - body_weight_N) * T

    if (pull_end_tick - pull_start_tick) >= 200: # 200ms
        imp_200ms = 0
        for i in range(pull_start_tick, pull_start_tick+200, 1):
            imp_200ms += (force_N_join[i] - body_weight_N) * T

    if (pull_end_tick - pull_start_tick) >= 250: # 250ms
        imp_250ms = 0
        for i in range(pull_start_tick, pull_start_tick+250, 1):
            imp_250ms += (force_N_join[i] - body_weight_N) * T

    imp_total = 0
    for i in range(pull_start_tick, pull_end_tick, 1):
            imp_total += (force_N_join[i] - body_weight_N) * T
    
    print("TtPF_sec:{}".format(TtPF_sec))
    print("RFD:{}".format(RFD))
    print("RFD_20ms:{}".format(RFD_20ms))
    print("RFD_30ms:{}".format(RFD_30ms))
    print("RFD_50ms:{}".format(RFD_50ms))
    print("RFD_90ms:{}".format(RFD_90ms))
    print("RFD_100ms:{}".format(RFD_100ms))
    print("RFD_150ms:{}".format(RFD_150ms))
    print("RFD_200ms:{}".format(RFD_200ms))
    print("RFD_250ms:{}".format(RFD_250ms))
    print("PF:{}".format(PF))
    #print("force_per_kg:{}".format(force_per_kg))


    print("imp_20ms:{}".format(imp_20ms))
    print("imp_30ms:{}".format(imp_30ms))
    print("imp_50ms:{}".format(imp_50ms))
    print("imp_90ms:{}".format(imp_90ms))
    print("imp_100ms:{}".format(imp_100ms))
    print("imp_150ms:{}".format(imp_150ms))
    print("imp_200ms:{}".format(imp_200ms))
    print("imp_250ms:{}".format(imp_250ms)) 
    print("imp_total:{}".format(imp_total))    

    return TtPF_sec, RFD, RFD_20ms, RFD_30ms, RFD_50ms, RFD_90ms, RFD_100ms, RFD_150ms, RFD_200ms, RFD_250ms, imp_20ms, imp_30ms, imp_50ms, imp_90ms, imp_100ms, imp_150ms, imp_200ms, imp_250ms, imp_total, PF, pRFD, pRFD_sec


def get_IMTP_features_of_join_force(data_name, time_sec_tick, force_N_join):
    print("get_IMTP_features_of_join_force")

    # calculate force slop
    force_slope = [0]
    for i in range(1,len(force_N_join)):
        force_slope += [force_N_join[i]-force_N_join[i-1]]

    stages = ['stand_by', 'pull_stage', 'release_stage']
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
    stable_end_fix = -1
    stable_end_fix_tick = -1

    pull_start = -1
    pull_start_tick = -1
    pf = -1
    pf_tick = -1
    pull_height = -1
    goback_condition_count = 0

    pull_end = -1
    pull_end_tick = -1

    print("data_name:{}".format(data_name))
    print("[Stage:{}]".format(stages[stg_num]))
    for i in range(len(time_sec_tick)):
        #print("i:{}, time_sec_tick[i]:{}, force_N_join[i]:{}, [Stage:{}], stg_num:{}, std:{}, stable_start:{}, stable_end:{}, mean:{}, stable_length:{}, pf_tick:{}".format(i,time_sec_tick[i], force_N_join[i], stages[stg_num], stg_num, std, stable_start, stable_end, mean, stable_length, pf_tick))
        # find the starting point of stabd_by stage
        # conditions:
        # 1. force > 100N
        # 2. force moving std < 10N ?
        if force_N_join[i] > 100.0 and stg_num == 0: 
            
            #print("stable_start_tick:{}, stable_end_tick:{}, std:{}, stable_length:{}, mean:{}, stable_start:{}, stable_end:{}".format(stable_start_tick, stable_end_tick, std, stable_length, mean, stable_start, stable_end))

            if std < 30.0:
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
                #print("i:{}, force_slope[i]:{}".format(i, force_slope[i]))
                if force_slope[i] <= 1:
                    stable_end_fix = time_sec_tick[i]
                    stable_end_fix_tick = i
                    #print("stable_end_fix:{}".format(stable_end_fix))

            else:
                
                stable_time = stable_end - stable_start
                if stable_time > 0.5 and stable_start >= time_sec_tick[0]:
                    #print("stable_start:{}, stable_end:{}, stable_start_tick:{}, stable_end_tick:{}".format(stable_start, stable_end, stable_start_tick, stable_end_tick))
                    # stage change
                    stg_num = 1
                    print("[Stage:{}]".format(stages[stg_num]))
                    pull_start = stable_end
                    pull_start_tick = stable_end_tick
                    pull_height = force_N_join[pull_start_tick]
                    pf = time_sec_tick[i]
                    pf_tick = i

                else:

                    mean = force_N_join[i]
                    stable_length = 1
                    stable_time = 0
                    diff_pow2_mean = 0
                    std = 0
                    stable_start = time_sec_tick[i]
                    stable_start_tick = i
                    stable_end_fix = stable_start
                    stable_end_fix_tick = stable_start_tick
        elif stg_num == 0:
            mean = force_N_join[i]
            stable_length = 1
            stable_time = 0
            diff_pow2_mean = 0
            std = 0
            stable_start = time_sec_tick[i]
            stable_start_tick = i
            stable_end_fix = stable_start
            stable_end_fix_tick = stable_start_tick

        # find the end point of pull_stage
        if stg_num == 1:
            #print("mean:{}, abs(force_N_join[i] - mean):{}".format(mean, abs(force_N_join[i] - mean)))
            # go back to stg_num 0 ?
            if abs(force_N_join[i] - mean) < 50:

                goback_condition_count += 1
                print("goback_condition_count:{}".format(goback_condition_count))
                if goback_condition_count >= 100:
                    stg_num = 0
                    mean = force_N_join[i]
                    stable_length = 1
                    stable_time = 0
                    diff_pow2_mean = 0
                    std = 0
                    stable_start = time_sec_tick[i]
                    stable_start_tick = i
                    stable_end_fix = stable_start
                    stable_end_fix_tick = stable_start_tick
                    goback_condition_count = 0
                    print("[go back to stg_num 0] stable_start:{}, stable_start_tick:{}".format(stable_start, stable_start_tick))
            else:
                goback_condition_count = 0
            
            # go back to stg_num 0 ? condition 2 should not have ec on SJ
            #print("force_N_join[i]:{}, mean:{}, i:{}, pf_tick:{}".format(force_N_join[i], mean, i, pf_tick))
            if (
                (force_N_join[i] - mean) < -50 # detect ec  
                #and i <= pf_tick
               ): # make sure force drop happens before pf or pull_height point
                
                stg_num = 0
                mean = force_N_join[i]
                stable_length = 1
                stable_time = 0
                diff_pow2_mean = 0
                std = 0
                stable_start = time_sec_tick[i]
                stable_start_tick = i
                stable_end_fix = stable_start
                stable_end_fix_tick = stable_start_tick
                print("[go back to stg_num 0][EC detected] stable_start:{}, stable_start_tick:{}".format(stable_start, stable_start_tick))


            #print("time_sec_tick[i]:{}, force_N_join[i]:{}".format(time_sec_tick[i], force_N_join[i]))
            if force_N_join[i] >= pull_height:
                pull_height = force_N_join[i]
                pf = time_sec_tick[i]
                pf_tick = i
            #elif force_N_join[i] <= force_N_join[ec_deacc_start_tick]: # keep searching
            #    co_height = force_N_join[ec_deacc_start_tick]
            if abs(force_N_join[i] - mean) < 10 and (pull_height - mean) > 200: # condition of leaving pull_stage
                    stg_num = 2
                    #print("[Stage:{}]".format(stages[stg_num]))
                    pull_end = time_sec_tick[i]
                    pull_end_tick = i

    print("stable_start_tick:{}, stable_end_tick:{}".format(stable_start_tick, stable_end_tick))
    print("stable_start:{}, stable_end:{}".format(stable_start, stable_end))
    print("stable_end_fix:{}, stable_end_fix_tick:{}".format(stable_end_fix, stable_end_fix_tick))
    print("pull_start_tick:{}, pf_tick:{}".format(pull_start_tick, pf_tick))
    print("pull_end_tick:{}, pf_tick:{}".format(pull_end_tick, pf_tick))

    # fix stable end position
    stable_end = stable_end_fix
    stable_end_tick = stable_end_fix_tick
    pull_start = stable_end
    pull_start_tick = stable_end_tick

    return stg_num, stable_start, stable_start_tick, stable_end, stable_end_tick, pull_start, pull_start_tick, pf, pf_tick, pull_end, pull_end_tick







