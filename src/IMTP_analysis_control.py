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
import IMTP_plot as IMTPP
import jump_analysis_modules as JAM
import IMTP_analysis_modules as IMTPAM

def IMTP_processing(data_dir, data_name, T, time_sec_tick, force_N_1, force_N_2, force_N_join):

    new_error_fig_path = ''
    new_fig_time_force_notiation_path = ''

    stg_num, stable_start, stable_start_tick, stable_end, stable_end_tick, pull_start, pull_start_tick, pf, pf_tick, pull_end, pull_end_tick = IMTPAM.get_IMTP_features_of_join_force(data_name, time_sec_tick, force_N_join)

    if stg_num != 2: # not finish test correctly. should return error message.
        print("stg_num:{}".format(stg_num))
        err_msg = ''
        if stg_num == 0:
            err_msg = "[Analysis Error] Stable time should >= 3sec or no eccentric contraction"

        if stg_num == 1:
            err_msg = "[Analysis Error] Not a correct pull. No release stage detected."

        print(err_msg)
        # plot err msg
        fig = DP.get_fig_time_force_with_err_msg(time_sec_tick, force_N_join, err_msg, data_name)
        fig.savefig( data_dir + '{}_error_message.png'.format(data_name))
        #list_new_error_fig_path += [data_dir + '{}_error_message.png'.format(data_name)]
        new_error_fig_path = data_dir + '{}_error_message.png'.format(data_name)
        #plt.close(fig)

    else:

        TtPF_sec, RFD, RFD_20ms, RFD_30ms, RFD_50ms, RFD_90ms, RFD_100ms, RFD_150ms, RFD_200ms, RFD_250ms, imp_20ms, imp_30ms, imp_50ms, imp_90ms, imp_100ms, imp_150ms, imp_200ms, imp_250ms, imp_total, PF, pRFD, pRFD_sec = IMTPAM.get_IMTP_record_statistics(T, time_sec_tick, force_N_join, stable_start, stable_start_tick, stable_end, stable_end_tick, pull_start, pull_start_tick, pf, pf_tick, pull_end, pull_end_tick)

        # plot
        fig = DP.get_fig_time_force(data_name, time_sec_tick, force_N_1, force_N_2, force_N_join)
        fig.savefig( data_dir + '{}_time_force_raw.png'.format(data_name))
        plt.close(fig)

        fig = IMTPP.get_fig_IMTP_time_force_notiation(data_name, time_sec_tick, force_N_join, stable_start, stable_start_tick, stable_end, stable_end_tick, pull_start, pull_start_tick, pf, pf_tick, pull_end, pull_end_tick, TtPF_sec, RFD, RFD_20ms, RFD_30ms, RFD_50ms, RFD_90ms, RFD_100ms, RFD_150ms, RFD_200ms, RFD_250ms, imp_20ms, imp_30ms, imp_50ms, imp_90ms, imp_100ms, imp_150ms, imp_200ms, imp_250ms, imp_total, PF, pRFD, pRFD_sec)
        fig.savefig( data_dir + '{}_time_force_notation.png'.format(data_name))

        new_fig_time_force_notiation_path = data_dir + '{}_time_force_notation.png'.format(data_name)

        # dump analysis_results
        data_analysis_results_path = data_dir + data_name +"_analysis_results.csv"

        csv_header = []
        csv_header += ["data_name"]

        csv_header += ["TtPF_sec"]
        csv_header += ["RFD"]
        csv_header += ["RFD_20ms"]
        csv_header += ["RFD_30ms"]
        csv_header += ["RFD_50ms"]
        csv_header += ["RFD_90ms"]
        csv_header += ["RFD_100ms"]
        csv_header += ["RFD_150ms"]
        csv_header += ["RFD_200ms"]
        csv_header += ["RFD_250ms"]
        csv_header += ["imp_20ms"]
        csv_header += ["imp_30ms"]
        csv_header += ["imp_50ms"]
        csv_header += ["imp_90ms"]
        csv_header += ["imp_100ms"]
        csv_header += ["imp_150ms"]
        csv_header += ["imp_200ms"]
        csv_header += ["imp_250ms"]
        csv_header += ["imp_total"]
        csv_header += ["PF"]
        csv_header += ["pRFD"]
        csv_header += ["pRFD_sec"]
        
                
        with open(data_analysis_results_path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_header)
            anlysis_result = []
            for col in range(len(csv_header)):
                anlysis_result += [eval(csv_header[col])]
            writer.writerow(anlysis_result)
            csvfile.close()


    return new_error_fig_path, new_fig_time_force_notiation_path













