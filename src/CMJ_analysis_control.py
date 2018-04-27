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
import CMJ_analysis_modules as CMJAM


def CMJ_processing(data_dir, data_name, T, time_sec_tick, force_N_1, force_N_2, force_N_join):

    new_error_fig_path = ''
    new_fig_time_force_notiation_path = ''

    stg_num, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_acc_end, ec_acc_end_tick, ec_low, ec_deacc_start, ec_deacc_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick, ec_low_tick = CMJAM.get_CMJ_features_of_join_force(data_name, time_sec_tick, force_N_join)

    a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick, ec_acc_end, ec_acc_end_tick, ec_deacc_start, ec_deacc_start_tick, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick, stable_end, stable_end_tick, ec_start, ec_start_tick, air_start, air_start_tick, air_end, air_end_tick = CMJAM.get_CMJ_a_v_p(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_acc_end, ec_acc_end_tick, ec_low, ec_deacc_start, ec_deacc_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick)


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
        fig = DP.get_fig_time_force_with_err_msg(time_sec_tick, force_N_join, err_msg, data_name)
        fig.savefig( data_dir + '{}_error_message.png'.format(data_name))
        #list_new_error_fig_path += [data_dir + '{}_error_message.png'.format(data_name)]
        new_error_fig_path = data_dir + '{}_error_message.png'.format(data_name)
        #plt.close(fig)

    else:    

        fly_time_sec, contact_time_sec, TtPF_sec, RFD, PF, jump_height_m, jump_power, time_ecc_sec, time_con_sec, total_time_sec, fly_contact_ratio, RSI_mod, mean_co_force, velocity_pf, force_pf, pVelocity, mean_power_con, time_to_pp_sec, min_velocity, force_at_zero_velocity, mean_ec_con_power, velocity_take_off, imp_ec_deacc_con, RNI, imp_ec_acc, area_force_velocity, ec_displacement_cm, vertical_stiffness, RFD_20ms, RFD_30ms, RFD_50ms, RFD_90ms, RFD_100ms, RFD_150ms, RFD_200ms, RFD_250ms, pRFD, pRFD_sec, force_pp, velocity_pp, time_ecc_acc_sec, time_ecc_deacc_sec, imp_ec_deacc, imp_con, jump_height_m_by_v = CMJAM.get_CMJ_record_statistics(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_acc_end, ec_acc_end_tick, ec_low, ec_deacc_start, ec_deacc_start_tick, pf, pf_tick, co_height, air_start, air_start_tick, air_end, air_end_tick, a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick)

        # plot
        fig = DP.get_fig_time_force(data_name, time_sec_tick, force_N_1, force_N_2, force_N_join)
        fig.savefig( data_dir + '{}_time_force_raw.png'.format(data_name))
        plt.close(fig)


        fig = CMJP.get_fig_CMJ_time_force_notiation(data_name, time_sec_tick, force_N_join, stable_start_tick, stable_end_tick, ec_start_tick, ec_acc_end_tick, ec_deacc_start_tick, pf_tick, air_start_tick, air_end_tick,
            fly_time_sec, contact_time_sec, TtPF_sec, RFD, jump_height_m, jump_power, PF, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick, pRFD, pRFD_sec)
        fig.savefig( data_dir + '{}_time_force_notation.png'.format(data_name))
        #plt.show(block=False)
        #plt.ion()
        #plt.show()
        #plt.pause(0.001)

        #list_new_fig_time_force_notiation_path += [data_dir + '{}_time_force_notation.png'.format(data_name)]
        new_fig_time_force_notiation_path = data_dir + '{}_time_force_notation.png'.format(data_name)
        #plt.close(fig)

        fig = CMJP.get_fig_CMJ_time_f_a_v_p(data_name, time_sec_tick, force_N_join, a_mss, v_mps, p_watt, p_watt_max_tick, stable_start_tick, stable_end_tick, ec_start_tick, ec_acc_end_tick, ec_deacc_start_tick, pf_tick, air_start_tick, air_end_tick, ec_deacc_end_tick, co_start_tick, co_end_tick, time_ecc_sec, time_con_sec, total_time_sec, fly_contact_ratio, RSI_mod, mean_co_force, velocity_pf, force_pf, pVelocity, mean_power_con, time_to_pp_sec, min_velocity, force_at_zero_velocity, mean_ec_con_power, velocity_take_off, imp_ec_deacc_con, RNI, imp_ec_acc, area_force_velocity, ec_displacement_cm, vertical_stiffness, RFD_20ms, RFD_30ms, RFD_50ms, RFD_90ms, RFD_100ms, RFD_150ms, RFD_200ms, RFD_250ms, force_pp, velocity_pp, time_ecc_acc_sec, time_ecc_deacc_sec)
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
        csv_header += ["jump_height_m_by_v"]
        csv_header += ["jump_power"]
        csv_header += ["time_ecc_sec"]
        csv_header += ["time_con_sec"]
        csv_header += ["total_time_sec"]
        csv_header += ["fly_contact_ratio"]
        csv_header += ["RSI_mod"]
        csv_header += ["mean_co_force"]
        csv_header += ["velocity_pf"]
        csv_header += ["force_pf"]
        csv_header += ["pVelocity"]
        csv_header += ["mean_power_con"]
        csv_header += ["time_to_pp_sec"]
        csv_header += ["min_velocity"]
        csv_header += ["force_at_zero_velocity"]
        csv_header += ["mean_ec_con_power"]
        csv_header += ["velocity_take_off"]
        csv_header += ["imp_ec_deacc_con"]
        csv_header += ["imp_ec_deacc"]
        csv_header += ["imp_con"]
        csv_header += ["RNI"]
        csv_header += ["imp_ec_acc"]
        csv_header += ["area_force_velocity"]
        csv_header += ["ec_displacement_cm"]
        csv_header += ["vertical_stiffness"]
        csv_header += ["jump_power"]

        csv_header += ["RFD_20ms"]
        csv_header += ["RFD_30ms"]
        csv_header += ["RFD_50ms"]
        csv_header += ["RFD_90ms"]
        csv_header += ["RFD_100ms"]
        csv_header += ["RFD_150ms"]
        csv_header += ["RFD_200ms"]
        csv_header += ["RFD_250ms"]
        csv_header += ["pRFD"]
        csv_header += ["pRFD_sec"]

        csv_header += ["force_pp"]
        csv_header += ["velocity_pp"]
        csv_header += ["time_ecc_acc_sec"]
        csv_header += ["time_ecc_deacc_sec"]

        csv_header += ["ec_low"]
        csv_header += ["ec_low_tick"]

                
        with open(data_analysis_results_path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_header)
            anlysis_result = []
            for col in range(len(csv_header)):
                anlysis_result += [eval(csv_header[col])]
            writer.writerow(anlysis_result)
            csvfile.close()

    return new_error_fig_path, new_fig_time_force_notiation_path 