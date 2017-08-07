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
import jump_analysis_modules as JAM
import CMJ_analysis_control as CMJAC
import CMJ_statistics_control as CMJSC
import SJ_analysis_control as SJAC
import SJ_statistics_control as SJSC
import DJ_analysis_control as DJAC
import DJ_statistics_control as DJSC
import IMTP_analysis_control as IMTPAC
import IMTP_statistics_control as IMTPSC

def update_user_IMTP_statistics(data_dir):

    IMTPSC.update_user_IMTP_statistics(data_dir)

def update_user_DJ_statistics(data_dir):

    DJSC.update_user_DJ_statistics(data_dir)

def update_user_SJ_statistics(data_dir):

    SJSC.update_user_SJ_statistics(data_dir)


def update_user_CMJ_statistics(data_dir):
    
    CMJSC.update_user_CMJ_statistics(data_dir)


def single_user_analysis(data_dir):

    file_list = os.listdir(data_dir)
    analysis_list = JAM.get_analysis_list(file_list)

    list_new_fig_time_force_notiation_path = []
    list_new_error_fig_path = []

    # test only section
    #analysis_list = ['Lt1']
    #analysis_list = ['ULt1']
    #if 'Gaby' in data_dir:
    #    analysis_list = ['Lg1']
    #if 'Tom' in data_dir:
    #    analysis_list = ['Lt1']
    #if 'user1' in data_dir:
    #    analysis_list = ['benson']
    #    analysis_list = ['user1_20170629_ULCMJ_t1-1']
    #if 'user1' in data_dir:
    #    analysis_list = ['user1_20170329_ULSJ_t1','user1_20170329_ULSJ_t2']
    #    analysis_list = ['user1_20170329_ULSJ_t2']
    #    analysis_list = ['user1_20170428_ULSJ_t1']
    #    analysis_list = ['user1_20170530_ULCMJ_t1']
    #    analysis_list = ['user1_20170530_ULCMJ_t8']
    #    analysis_list = ['user1_20170530_ULCMJ_t44']
    #    analysis_list = ['user1_20170530_ULCMJ_t28']
    #if 'user2' in data_dir:
    #    analysis_list = ['user2_20170428_LSJ_t1']
    #if 'user12' in data_dir:
    #    analysis_list = ['user12_20170428_LSJ_t3']
    # test only section end
    #if 'scott' in data_dir:
    #    analysis_list = ['scott_20170525_ULSJ_t1'] # uneven floor ?
    #if 'scott' in data_dir:
    #    analysis_list = ['scott_20170525_LCMJ_t1']
    #    analysis_list = ['scott_20170525_LCMJ_t1', 'scott_20170525_LCMJ_t2']
    #    analysis_list += ['scott_20170525_ULSJ_t1'] # one air force error
    #    analysis_list += ['scott_20170525_ULSJ_t2']
    
    # if 'userA' in data_dir:
    #     analysis_list = ['userA_20170621_ULDJ_t1']
    #     analysis_list += ['userA_20170621_ULDJ_t2']
    #     analysis_list += ['userA_20170621_LDJ_t1']
    #     analysis_list += ['userA_20170621_LDJ_t2']
    
    #if 'userM' in data_dir:
    #    analysis_list = ['userM_20170622_IMTP_t1']

    #if 'userProblem' in data_dir:
    #    analysis_list = ['userProblem_20170626_ULSJ_t64-3']
    #    analysis_list = ['userProblem_20170623_ULSJ_t2']
    
    #if 'userGroupULSJ' in data_dir:
    #    analysis_list = ['ULSJ_20170622_user3_t5-3']

    #if 'userGroupDJ' in data_dir:
    #    analysis_list = ['ULDJ_20170622_user5_t6-1']
    #if 'userGroupIMTP' in data_dir:
    #    analysis_list = ['IMTP_20170713_user6_t1-1']
    #    analysis_list += ['IMTP_20170713_user6_t1-2']
    #if 'userGroupLSJ' in data_dir:
    #    analysis_list = ['LSJ_20170622_user4_t1-2']

    #if 'userGroupULCMJ' in data_dir:
    #    analysis_list = ['ULCMJ_20170622_user1_t5-1']
    #if 'basketIMTP' in data_dir:
    #    analysis_list = ['20170801_IMTP_user1_t4-4']

    if analysis_list == []:
        print("[No new data waited for analysis] Please copy new force plate csv file into data folder:[{}]".format(data_dir))
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
                list_new_error_fig_path += [data_dir + '{}_error_message.png'.format(data_name)]
                #plt.close(fig)

                #sys.exit()
            elif not('CMJ' in data_name or 'SJ' in data_name or 'DJ' in data_name or 'IMTP' in data_name):
                err_msg = "[Input Name Error] Unrecognized Jump Type. Valid types: CMJ / SJ / DJ / IMTP"
                error_code = 10201
                print("error_code:{}".format(error_code))
                print(err_msg)
                # plot err msg
                fig = DP.get_fig_no_data_with_err_msg(error_code,err_msg)
                fig.savefig( data_dir + '{}_error_message.png'.format(data_name))
                list_new_error_fig_path += [data_dir + '{}_error_message.png'.format(data_name)]
                #plt.close(fig)

            elif 'CMJ' in data_name:
                new_error_fig_path, new_fig_time_force_notiation_path = CMJAC.CMJ_processing(data_dir, data_name, T, time_sec_tick, force_N_1, force_N_2, force_N_join)

                if new_fig_time_force_notiation_path != '':
                    list_new_fig_time_force_notiation_path += [new_fig_time_force_notiation_path]
                if new_error_fig_path != '':
                    list_new_error_fig_path += [new_error_fig_path]

                
            elif 'SJ' in data_name:
                new_error_fig_path, new_fig_time_force_notiation_path = SJAC.SJ_processing(data_dir, data_name, T, time_sec_tick, force_N_1, force_N_2, force_N_join)

                if new_fig_time_force_notiation_path != '':
                    list_new_fig_time_force_notiation_path += [new_fig_time_force_notiation_path]
                if new_error_fig_path != '':
                    list_new_error_fig_path += [new_error_fig_path]

            elif 'DJ' in data_name:
                new_error_fig_path, new_fig_time_force_notiation_path = DJAC.DJ_processing(data_dir, data_name, T, time_sec_tick, force_N_1, force_N_2, force_N_join)

                if new_fig_time_force_notiation_path != '':
                    list_new_fig_time_force_notiation_path += [new_fig_time_force_notiation_path]
                if new_error_fig_path != '':
                    list_new_error_fig_path += [new_error_fig_path]

            elif 'IMTP' in data_name:
                new_error_fig_path, new_fig_time_force_notiation_path = IMTPAC.IMTP_processing(data_dir, data_name, T, time_sec_tick, force_N_1, force_N_2, force_N_join)

                if new_fig_time_force_notiation_path != '':
                    list_new_fig_time_force_notiation_path += [new_fig_time_force_notiation_path]
                if new_error_fig_path != '':
                    list_new_error_fig_path += [new_error_fig_path]


    return list_new_error_fig_path, list_new_fig_time_force_notiation_path, analysis_list








