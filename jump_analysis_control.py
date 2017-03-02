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

#########################################
workspace_dir = "{}/".format(os.getcwd())
data_dir = workspace_dir + "test_data/"

file_list = os.listdir(data_dir)
print("file_list:{}".format(file_list))

analysis_list = JAM.get_analysis_list(file_list)

# test only section
#analysis_list = ['Lt1']
#analysis_list = ['ULt1']

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

                fly_time_sec, contact_time_sec, TtPF_sec, RFD, jump_height_m, jump_power = JAM.get_statistics(T, time_sec_tick, force_N_join, stable_start, stable_end, stable_start_tick, stable_end_tick, ec_start, ec_start_tick, ec_end, ec_end_tick, ec_low, co_start, co_start_tick, co_end, co_end_tick, co_hight, air_start, air_start_tick, air_end, air_end_tick, a_mss, v_mps, p_watt, p_watt_max, p_watt_max_tick)

                # plot
                fig = DP.get_fig_time_force(time_sec_tick, force_N_1, force_N_2, force_N_join)
                fig.savefig( data_dir + '{}_time_force_raw.png'.format(data_name))
                plt.close(fig)


                fig = DP.get_fig_time_force_notiation(time_sec_tick, force_N_join, stable_start_tick, stable_end_tick, ec_start_tick, ec_end_tick, co_start_tick, co_end_tick, air_start_tick, air_end_tick,
                    fly_time_sec, contact_time_sec, TtPF_sec, RFD, jump_height_m, jump_power)
                fig.savefig( data_dir + '{}_time_force_notation.png'.format(data_name))
                plt.close(fig)

                fig = DP.get_fig_time_f_a_v_p(time_sec_tick, force_N_join, a_mss, v_mps, p_watt, co_end_tick, p_watt_max_tick)
                fig.savefig( data_dir + '{}_time_f_a_v_p.png'.format(data_name))
                plt.close(fig)




