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

def get_SJ_record_statistics(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, co_start, co_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick, co_end, co_end_tick):

    # statistics
    fly_time_sec = air_end - air_start
    contact_time_sec = air_start - co_start
    TtPF_sec = pf - co_start     # time to peak force
    RFD = force_N_join[pf_tick] / TtPF_sec
    #jump_height = 9.8 * (0.5 * fly_time)**2 + -9.8 * 0.5 * (0.5 * fly_time)**2
    PF = force_N_join[pf_tick]
    jump_height_m = 0.5 * 9.8 * (0.5 * fly_time_sec)**2
    jump_power = p_watt_max
    #print("pf_tick:{}".format(pf_tick))


    print("fly_time_sec:{}".format(fly_time_sec))
    print("contact_time_sec:{}".format(contact_time_sec))
    print("TtPF_sec:{}".format(TtPF_sec))
    print("RFD:{}".format(RFD))
    print("PF:{}".format(PF))
    print("jump_height_m:{}".format(jump_height_m))
    print("jump_power:{}".format(jump_power))

    return fly_time_sec, contact_time_sec, TtPF_sec, RFD, PF, jump_height_m, jump_power

def get_CMJ_record_statistics(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_acc_end, ec_acc_end_tick, ec_low, ec_deacc_start, ec_deacc_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick):

    # statistics
    fly_time_sec = air_end - air_start
    contact_time_sec = air_start - ec_start
    TtPF_sec = pf - ec_deacc_start     # time to peak force
    RFD = force_N_join[pf_tick] / TtPF_sec
    #jump_height = 9.8 * (0.5 * fly_time)**2 + -9.8 * 0.5 * (0.5 * fly_time)**2
    PF = force_N_join[pf_tick]
    jump_height_m = 0.5 * 9.8 * (0.5 * fly_time_sec)**2
    jump_power = p_watt_max
    #print("pf_tick:{}".format(pf_tick))

    time_ecc_sec = ec_deacc_end - ec_start
    time_con_sec = co_end - co_start
    total_time_sec = time_ecc_sec + time_con_sec
    fly_contact_ratio = fly_time_sec / contact_time_sec
    if fly_time_sec == 0:
        RSI_mod = 0
    else:
        RSI_mod = contact_time_sec / fly_time_sec
    mean_co_force = np.mean(force_N_join[co_start_tick:co_end_tick])
    velocity_pf = v_mps[pf_tick]
    force_pf = force_N_join[pf_tick]
    pVelocity = v_mps[co_end_tick]
    mean_power_con = np.mean(p_watt[co_start_tick:co_end_tick])
    time_to_pp_sec = time_sec_tick[p_watt_max_tick] - ec_start
    min_velocity = v_mps[ec_deacc_start_tick]
    force_at_zero_velocity = force_N_join[co_start_tick]
    mean_ec_con_power = np.mean(p_watt[ec_start_tick:co_end_tick])
    velocity_take_off = v_mps[air_start_tick]

    # impulse calculation
    imp_ec_deacc_con = 0
    body_weight_N = np.mean(force_N_join[stable_start_tick:stable_end_tick])
    print("T:{}, body_weight_N:{}".format(T, body_weight_N))
    for i in range(ec_deacc_start_tick, co_end_tick, 1):
        #print("i:{}, force_N_join[i]:{}".format(i, force_N_join[i]))
        imp_ec_deacc_con += (force_N_join[i] - body_weight_N) * T
    RNI = imp_ec_deacc_con / body_weight_N # check definition ??

    imp_ec_acc = 0
    for i in range(ec_start_tick, ec_acc_end_tick, 1):
        imp_ec_acc += (force_N_join[i] - body_weight_N) * T

    # area_force_velocity calculation
    area_force_velocity = 0
    for i in range(ec_start_tick+1, co_start_tick, 1): # v < 0m/s
        delta_v = v_mps[i] - v_mps[i-1]
        f_delta_mean = (force_N_join[i] + force_N_join[i-1])/2.0
        area_force_velocity += delta_v * f_delta_mean
        #print("i:{}, area_force_velocity:{}, delta_v:{}, f_delta_mean:{}".format(i, area_force_velocity, delta_v, f_delta_mean))

    # stiffness calculation
    pos_cm = [0]
    for i in range(1,len(v_mps)):
        delta_pos_cm = ( v_mps[i-1]*T + 0.5*a_mss[i-1]*T**2 ) * 100
        pos_cm += [pos_cm[-1] + delta_pos_cm]
        #print("i:{}, pos_cm[i]:{}".format(i,pos_cm[i]))
    ec_displacement_cm = pos_cm[ec_start_tick] - pos_cm[ec_deacc_end_tick]
    vertical_stiffness = force_pf / ec_displacement_cm
    


    print("fly_time_sec:{}".format(fly_time_sec))
    print("contact_time_sec:{}".format(contact_time_sec))
    print("TtPF_sec:{}".format(TtPF_sec))
    print("RFD:{}".format(RFD))
    print("PF:{}".format(PF))
    print("jump_height_m:{}".format(jump_height_m))
    print("jump_power:{}".format(jump_power))

    print("time_ecc_sec:{}".format(time_ecc_sec))
    print("time_con_sec:{}".format(time_con_sec))
    print("total_time_sec:{}".format(total_time_sec))
    print("fly_contact_ratio:{}".format(fly_contact_ratio))
    print("RSI_mod:{}".format(RSI_mod))
    print("mean_co_force:{}".format(mean_co_force))
    print("velocity_pf:{}".format(velocity_pf))
    print("force_pf:{}".format(force_pf))
    print("pVelocity:{}".format(pVelocity))
    print("mean_power_con:{}".format(mean_power_con))
    print("time_to_pp_sec:{}".format(time_to_pp_sec))
    print("min_velocity:{}".format(min_velocity))
    print("force_at_zero_velocity:{}".format(force_at_zero_velocity))
    print("mean_ec_con_power:{}".format(mean_ec_con_power))
    print("velocity_take_off:{}".format(velocity_take_off))  
    print("imp_ec_deacc_con:{}".format(imp_ec_deacc_con))  
    print("RNI:{}".format(RNI))
    print("imp_ec_acc:{}".format(imp_ec_acc))
    print("area_force_velocity:{}".format(area_force_velocity))
    print("ec_displacement_cm:{}".format(ec_displacement_cm))
    print("vertical_stiffness:{}".format(vertical_stiffness))

    return fly_time_sec, contact_time_sec, TtPF_sec, RFD, PF, jump_height_m, jump_power, time_ecc_sec, time_con_sec, total_time_sec, fly_contact_ratio, RSI_mod, mean_co_force, velocity_pf, force_pf, pVelocity, mean_power_con, time_to_pp_sec, min_velocity, force_at_zero_velocity, mean_ec_con_power, velocity_take_off, imp_ec_deacc_con, RNI, imp_ec_acc, area_force_velocity, ec_displacement_cm, vertical_stiffness

def get_SJ_a_v_p(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, co_start, co_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, co_end, co_end_tick):

    # calculate a / v / p # using stable start
    #body_weight = force_N_join[stable_start_tick] / 9.81
    body_weight = np.mean(force_N_join[stable_start_tick:stable_end_tick]) / 9.81
    print("body_weight:{}".format(body_weight))
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

    find_start_tick = pf_tick
    for i in range(len(time_sec_tick)):
        if find_start_tick < i < air_start_tick:
            #print("a_mss[i]:{}".format(a_mss[i]))
            if -0.5 <= a_mss[i] <= 0.5:
                co_end_tick = i
                co_end = time_sec_tick[i]
    print("pf_tick:{}, air_start_tick:{}, co_end_tick:{}".format(pf_tick, air_start_tick, co_end_tick))

        #print("time_sec_tick:{}, force_N_join:{}, a_mss:{}, v_mps:{}, p_watt:{}".format(time_sec_tick[i], force_N_join[i], a_mss[i], v_mps[i], p_watt[i]))

    return a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick, co_end, co_end_tick

def get_CMJ_a_v_p(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_acc_end, ec_acc_end_tick, ec_low, ec_deacc_start, ec_deacc_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick):

    # calculate a / v / p # using stable start
    #body_weight = force_N_join[stable_start_tick] / 9.81
    body_weight = np.mean(force_N_join[stable_start_tick:stable_end_tick]) / 9.81
    print("body_weight:{}".format(body_weight))
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

    # search true ec_acc_end, ec_deacc_end, and co_end?
    v_low = 0
    find_start_tick = ec_acc_end_tick
    for i in range(len(time_sec_tick)):
        if find_start_tick < i < co_end_tick:
            #print("time_sec_tick:{}, force_N_join:{}, a_mss:{}, v_mps:{}, p_watt:{}".format(time_sec_tick[i], force_N_join[i], a_mss[i], v_mps[i], p_watt[i]))
            if v_mps[i] < v_low:
                v_low = v_mps[i]
                ec_acc_end_tick = i
                ec_acc_end = time_sec_tick[i]
                ec_deacc_start_tick = i
                ec_deacc_start = time_sec_tick[i]
            if -0.05 <= v_mps[i] <= 0.05:
                ec_deacc_end_tick = i
                ec_deacc_end = time_sec_tick[i]
                co_start_tick = i
                co_start = time_sec_tick[i]
    
    find_start_tick = pf_tick
    for i in range(len(time_sec_tick)):
        if find_start_tick < i < air_start_tick:
            #print("time_sec_tick:{}, force_N_join:{}, a_mss:{}, v_mps:{}, p_watt:{}".format(time_sec_tick[i], force_N_join[i], a_mss[i], v_mps[i], p_watt[i]))
            if -0.5 <= a_mss[i] <= 0.5:
                co_end_tick = i
                co_end = time_sec_tick[i]

        #print("time_sec_tick:{}, force_N_join:{}, a_mss:{}, v_mps:{}, p_watt:{}".format(time_sec_tick[i], force_N_join[i], a_mss[i], v_mps[i], p_watt[i]))

    return a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick, ec_acc_end, ec_acc_end_tick, ec_deacc_start, ec_deacc_start_tick, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick

def get_SJ_features_of_join_force(data_name, time_sec_tick, force_N_join):
    print("get_SJ_features_of_join_force")

    # calculate force slop
    force_slope = [0]
    for i in range(1,len(force_N_join)):
        force_slope += [force_N_join[i]-force_N_join[i-1]]

    stages = ['stand_by', 'concetric_stage', 'on_air','landing']
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

    co_start = -1
    co_start_tick = -1
    pf = -1
    pf_tick = -1
    co_height = -1
    goback_condition_count = 0

    co_end = -1
    co_end_tick = -1

    air_start = -1
    air_start_tick = -1
    air_end = -1
    air_end_tick = -1

    print("data_name:{}".format(data_name))
    print("[Stage:{}]".format(stages[stg_num]))
    for i in range(len(time_sec_tick)):
        #print("i:{}, time_sec_tick[i]:{}, force_N_join[i]:{}, [Stage:{}], stg_num:{}".format(i,time_sec_tick[i], force_N_join[i], stages[stg_num], stg_num))
        # find the starting point of stabd_by stage
        # conditions:
        # 1. force > 100N
        # 2. force moving std < 10N ?
        if force_N_join[i] > 100.0 and stg_num == 0: 
            
            #print("stable_start_tick:{}, stable_end_tick:{}, std:{}, stable_length:{}, mean:{}, stable_start:{}, stable_end:{}".format(stable_start_tick, stable_end_tick, std, stable_length, mean, stable_start, stable_end))

            if std < 20.0:
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
                if stable_time > 0.25 and stable_start >= time_sec_tick[0]:
                    #print("stable_start:{}, stable_end:{}, stable_start_tick:{}, stable_end_tick:{}".format(stable_start, stable_end, stable_start_tick, stable_end_tick))
                    # stage change
                    stg_num = 1
                    print("[Stage:{}]".format(stages[stg_num]))
                    co_start = stable_end
                    co_start_tick = stable_end_tick
                    co_height = force_N_join[co_start_tick]
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

        # find the end point of concentric_stage
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
                    stable_end_fix = stable_start
                    stable_end_fix_tick = stable_start_tick
                    goback_condition_count = 0
                    print("[go back to stg_num 0] stable_start:{}, stable_start_tick:{}".format(stable_start, stable_start_tick))
            else:
                goback_condition_count = 0
            # go back to stg_num 0 ? condition 2 should not have ec on SJ
            #print("force_N_join[i]:{}, mean:{}, i:{}, pf_tick:{}".format(force_N_join[i], mean, i, pf_tick))
            if (
                (force_N_join[i] - mean) < -50 and # detect ec  
                i <= pf_tick): # make sure force drop happens before pf or co_height point
                
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
            if force_N_join[i] >= co_height:
                co_height = force_N_join[i]
                pf = time_sec_tick[i]
                pf_tick = i
            #elif force_N_join[i] <= force_N_join[ec_deacc_start_tick]: # keep searching
            #    co_height = force_N_join[ec_deacc_start_tick]
            elif force_N_join[i] <= 100: # condition of leaving ec_deacc_and_concetric_stage
                stg_num = 2
                print("[Stage:{}]".format(stages[stg_num]))
                co_end = time_sec_tick[i]
                co_end_tick = i
                air_start = time_sec_tick[i]
                air_start_tick = i
        # find the end point of on air stage
        if stg_num == 2:
            #print("time_sec_tick[i]:{}, force_N_join[i]:{}".format(time_sec_tick[i], force_N_join[i]))
            if force_N_join[i] <= 100:
                air_end = time_sec_tick[i]
                air_end_tick = i
            else: # condition of leaving air stage
                stg_num = 3
                print("[Stage:{}]".format(stages[stg_num]))

    print("stable_start_tick:{}, stable_end_tick:{}".format(stable_start_tick, stable_end_tick))
    print("stable_start:{}, stable_end:{}".format(stable_start, stable_end))
    print("stable_end_fix:{}, stable_end_fix_tick:{}".format(stable_end_fix, stable_end_fix_tick))
    #print("ec_start_tick:{}, ec_acc_end_tick:{}".format(ec_start_tick, ec_acc_end_tick))
    print("co_start_tick:{}, pf_tick:{}".format(co_start_tick, pf_tick))
    print("air_start_tick:{}, air_end_tick:{}".format(air_start_tick, air_end_tick))

    # fix stable end position
    stable_end = stable_end_fix
    stable_end_tick = stable_end_fix_tick
    co_start = stable_end
    co_start_tick = stable_end_tick

    return stg_num, stable_start, stable_end, stable_start_tick, stable_end_tick, co_start, co_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, co_end, co_end_tick


def get_CMJ_features_of_join_force(data_name, time_sec_tick, force_N_join):

    # start find the special points
    stages = ['stand_by', 'eccentric_acc_stage', 'ec_deacc_and_ec_deacc_and_concetric_stage', 'on_air','landing']
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
    ec_acc_end = -1
    ec_acc_end_tick = -1
    ec_low = -1
    goback_condition_count = 0

    ec_deacc_start = -1 
    ec_deacc_start_tick = -1

    ec_deacc_end = -1
    ec_deacc_end_tick = -1

    co_start = -1
    co_start_tick = -1

    pf = -1
    pf_tick = -1
    co_height = -1

    co_end = -1
    co_end_tick = -1

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


        # find the end point of eccentric_acc_stage
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
                ec_acc_end = time_sec_tick[i]
                ec_acc_end_tick = i
            elif force_N_join[i] >= force_N_join[ec_start_tick]: # keep searching
                ec_low = force_N_join[ec_start_tick]
            elif force_N_join[i] >= ec_low + 100: # condition of leaving eccentric_acc_stage
                # stage change
                stg_num = 2
                print("[Stage:{}]".format(stages[stg_num]))
                ec_deacc_start = ec_acc_end
                ec_deacc_start_tick = ec_acc_end_tick
                co_height = force_N_join[ec_deacc_start_tick]

        # find the end point of ec_deacc_and_concetric_stage
        if stg_num == 2:
            #print("time_sec_tick[i]:{}, force_N_join[i]:{}, mean:{}, pf_tick:{}".format(time_sec_tick[i], force_N_join[i], mean, pf_tick))

            if force_N_join[i] >= co_height:
                co_height = force_N_join[i]
                pf = time_sec_tick[i]
                pf_tick = i

            if mean-15 <= force_N_join[i] <= mean+15 and i <= pf_tick:
                ec_deacc_end = time_sec_tick[i]
                ec_deacc_end_tick = i
                co_start = ec_deacc_end
                co_start_tick = ec_deacc_end_tick

            #elif force_N_join[i] <= force_N_join[ec_deacc_start_tick]: # keep searching
            #    co_height = force_N_join[ec_deacc_start_tick]
            elif force_N_join[i] <= 100 and force_N_join[pf_tick] > mean: # condition of leaving ec_deacc_and_concetric_stage
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
    
    ec_deacc_start = ec_acc_end
    ec_deacc_start_tick = ec_acc_end_tick
    co_end = air_start #
    co_end_tick = air_start_tick

    print("stable_start_tick:{}, stable_end_tick:{}".format(stable_start_tick, stable_end_tick))
    print("ec_start_tick:{}, ec_acc_end_tick:{}".format(ec_start_tick, ec_acc_end_tick))
    print("ec_deacc_start_tick:{}, ec_deacc_end_tick:{}".format(ec_deacc_start_tick, ec_deacc_end_tick))
    print("co_start_tick:{}, pf_tick:{}".format(co_start_tick, pf_tick))

    print("pf_tick:{}, co_end_tick:{}".format(pf_tick, co_end_tick))

    print("air_start_tick:{}, air_end_tick:{}".format(air_start_tick, air_end_tick))
    

    return stg_num, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_acc_end, ec_acc_end_tick, ec_low, ec_deacc_start, ec_deacc_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick


def get_analysis_list(file_list):

    csv_list = []
    plot_list = []
    for f in file_list:
        if ('.csv' in f )and ('analysis_results' not in f) and ('_statistics' not in f) and ('dual_input' not in f):
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


