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
import DJ_analysis_modules as DJAM

def DJ_processing(data_dir, data_name, T, time_sec_tick, force_N_1, force_N_2, force_N_join):

    new_error_fig_path = ''
    new_fig_time_force_notiation_path = ''

    stg_num, landing_start, landing_start_tick, landing_end, landing_end_tick, air_start, air_start_tick, air_end, air_end_tick = DJAM.get_DJ_features_of_join_force(data_name, time_sec_tick, force_N_join)

    if stg_num != 3: # not finish test correctly. should return error message.
        print("stg_num:{}".format(stg_num))
        err_msg = ''
        if stg_num == 0:
            err_msg = "[Analysis Error] load is detected before landing"

        if stg_num == 1:
            err_msg = "[Analysis Error] Not a correct DJ. No jump signal detected."

        if stg_num == 2:
            err_msg = "[Analysis Error] Not a correct DJ. No landing signal detected."
            #print("[Analysis Error] Not a correct CMJ. No jump signal detected.")

        print(err_msg)
        # plot err msg
        fig = DP.get_fig_time_force_with_err_msg(time_sec_tick, force_N_join, err_msg)
        fig.savefig( data_dir + '{}_error_message.png'.format(data_name))
        #list_new_error_fig_path += [data_dir + '{}_error_message.png'.format(data_name)]
        new_error_fig_path = data_dir + '{}_error_message.png'.format(data_name)
        #plt.close(fig)

    else:  

    	fly_time_sec, contact_time_sec, fly_contact_ratio, RSI_mod, jump_height_m = DJAM.get_DJ_record_statistics(T, time_sec_tick, force_N_join, landing_start, landing_start_tick, landing_end, landing_end_tick, air_start, air_start_tick, air_end, air_end_tick)

	    # plot
        fig = DP.get_fig_time_force(data_name, time_sec_tick, force_N_1, force_N_2, force_N_join)
        fig.savefig( data_dir + '{}_time_force_raw.png'.format(data_name))
        plt.close(fig)

        fig = DJP.get_fig_DJ_time_force_notiation(data_name, time_sec_tick, force_N_join, landing_start, landing_start_tick, landing_end, landing_end_tick, air_start, air_start_tick, air_end, air_end_tick, fly_time_sec, contact_time_sec, fly_contact_ratio, RSI_mod, jump_height_m)
        fig.savefig( data_dir + '{}_time_force_notation.png'.format(data_name))

        #list_new_fig_time_force_notiation_path += [data_dir + '{}_time_force_notation.png'.format(data_name)]
        new_fig_time_force_notiation_path = data_dir + '{}_time_force_notation.png'.format(data_name)
        #plt.close(fig)

        # dump analysis_results
        data_analysis_results_path = data_dir + data_name +"_analysis_results.csv"

        csv_header = []
        csv_header += ["data_name"]
        csv_header += ["fly_time_sec"]
        csv_header += ["contact_time_sec"]
        csv_header += ["fly_contact_ratio"]
        csv_header += ["RSI_mod"]
        csv_header += ["jump_height_m"]
                
        with open(data_analysis_results_path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_header)
            anlysis_result = []
            for col in range(len(csv_header)):
                anlysis_result += [eval(csv_header[col])]
            writer.writerow(anlysis_result)
            csvfile.close()

    return new_error_fig_path, new_fig_time_force_notiation_path















