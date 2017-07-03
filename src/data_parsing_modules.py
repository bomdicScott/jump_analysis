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

import data_plot as DP

def copy_txt_as_csv(data_dir): # for KISLER single input data
    
    file_list = os.listdir(data_dir)
    csv_list = []
    txt_list = []
    for f in file_list:
        if '.csv' in f:
            csv_list += [f.replace('.csv','')]
        if '.txt' in f:
            txt_list += [f]

    copy_list = []
    for t_name in txt_list:
        copied_detected = 0
        for c_name in csv_list:
            if c_name == t_name.replace('.txt',''):
                copied_detected = 1
        if copied_detected == 0:
            copy_list += [t_name]
    print("copy_list:{} in [{}]".format(copy_list, data_dir))
    
    for f in copy_list:
        copyfile(data_dir+f, data_dir+f.replace('.txt','.csv'))

def dispatch_daul_input(dual_input_dir, users_dir):

    file_list = os.listdir(dual_input_dir)
    txt_list = []
    list_new_error_fig_path = []

    for f in file_list:
        if (
            '.txt' in f and 
            'AND' in f and 
            len(f.split('_')) == 8 and 
            '20' in f.split('_')[0]
           ): # make sure the dual data has standard format
            txt_list += [f]
        elif (not os.path.isdir(f)) and '.txt' in f and (not 'ERROR' in f):
            err_msg = 'not_a_correct_dual_input_format'
            error_code = 10101
            fig = DP.get_fig_no_data_with_err_msg(error_code,err_msg)
            fig.savefig( dual_input_dir+'{}_ERROR_{}.png'.format(f,err_msg))
            list_new_error_fig_path += [dual_input_dir+'{}_ERROR_{}.png'.format(f,err_msg)]
            #plt.close(fig)

            '''
            with open(dual_input_dir+'{}_ERROR_{}'.format(f,err_msg), 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([err_msg])                    
                csvfile.close()
            '''


    for f_name in txt_list:
        # file name split
        f_name_units = f_name.replace('.txt','').split('_')
        print("f_name_units:{}".format(f_name_units))
        date = f_name_units[0]
        user1_name = f_name_units[1]
        user2_name = f_name_units[5]
        user1_jump_type = f_name_units[2]
        user2_jump_type = f_name_units[6]
        user1_jump_try = f_name_units[3]
        user2_jump_try = f_name_units[7]

        user1_raw = []
        user2_raw = []
        # load raw
        has_two_force_data = 1
        idx = 0
        f = open(dual_input_dir + f_name, 'rU')
        for row in csv.reader(f):
            #print("row:{}".format(row))
            if idx <= 18: # device infos
                user1_raw += [row[0]]
                user2_raw += [row[0]]
            else:
                split_list = row[0].split()
                #print("split_list:{}, len(split_list):{}".format(split_list, len(split_list)))
                if len(split_list) >= 3:
                    user1_raw += ['{}    {}'.format(split_list[0], split_list[1])]
                    user2_raw += ['{}    {}'.format(split_list[0], split_list[2])]
                else:
                    has_two_force_data = 0

            idx += 1
        f.close()

        if has_two_force_data == 1:
            #print("user1_raw:{}".format(user1_raw))
            #print("user2_raw:{}".format(user2_raw))

            # write data into corresponding files
            # check user folder
            user1_folder = users_dir + '{}/'.format(user1_name)
            user2_folder = users_dir + '{}/'.format(user2_name)
            if not os.path.exists(user1_folder):
                os.makedirs(user1_folder)
            if not os.path.exists(user2_folder):
                os.makedirs(user2_folder)


            user1_file_path = user1_folder + '{}_{}_{}_{}.csv'.format(user1_name, date, user1_jump_type, user1_jump_try)
            user2_file_path = user2_folder + '{}_{}_{}_{}.csv'.format(user2_name, date, user2_jump_type, user2_jump_try)

            #print("user1_raw:{}".format(user1_raw))

            with open(user1_file_path, 'w') as csvfile:
                writer = csv.writer(csvfile)
                for row in user1_raw:
                    writer.writerow([row])
                csvfile.close()
            
            with open(user2_file_path, 'w') as csvfile:
                writer = csv.writer(csvfile)
                for row in user2_raw:
                    writer.writerow([row])
                csvfile.close()
            
            # put original input txt into processed folder
            processed_folder_dir = dual_input_dir + 'processed/'
            if not os.path.exists(processed_folder_dir):
                os.makedirs(processed_folder_dir)
            copyfile(dual_input_dir+f_name, processed_folder_dir+f_name)
            os.remove(dual_input_dir+f_name)
        else:
            err_msg = 'does not have two force data'
            error_code = 10102
            fig = DP.get_fig_no_data_with_err_msg(error_code,err_msg)
            fig.savefig( dual_input_dir+'{}_ERROR_{}.png'.format(f_name,err_msg))
            list_new_error_fig_path += [dual_input_dir+'{}_ERROR_{}.png'.format(f_name,err_msg)]
            #plt.close(fig)


    return list_new_error_fig_path





def parsing_force_plate_raw_data(force_plate_raw_data_path):

    print("[parsing_force_plate_raw_data] force_plate_raw_data_path:{}".format(force_plate_raw_data_path))

    time_sec_tick = []
    force_N_1 = []
    force_N_2 = []
    force_N_join = []

    # [TODO] detect file comes from pasco or other brands

    # read csv
    f = open(force_plate_raw_data_path, 'rU')
    
    error_code = 0

    is_KISLER_file = 0
    KISLER_abs_idx = -1
    #is_KISLER_type_no_row_1 = 0 # no row [1]
    idx = 0
    for row in csv.reader(f):
        #print("row:{}, idx:{}".format(row, idx))
        #print('row[0]:{}'.format(row[0]))
        
        if row != []:
            if (idx <=1):
                if 'Device:' in row[0]:
                    is_KISLER_file = 1
                    print("[is_KISLER_file = 1]")

            if is_KISLER_file != 1:
                if (
                    len(row) == 4 and
                    idx >=2 and 
                    row[0] != '' and 
                    row[1] != '' and 
                    row[2] != '' and
                    row[3] != ''
                   ):
                    
                    # format detection
                    try:
                        val = float(row[0])
                        time_sec_tick += [float(row[0])]
                        force_N_1 += [float(row[1])]
                        force_N_2 += [float(row[2])]
                        force_N_join += [float(row[3])]
                    except:
                        #print("Input is not a standard CSV file")
                        error_code = 10001

                    if idx == 3:
                        try:
                            assert float(row[0]) == 0.001
                        except:
                            error_code = 10003
                elif idx >=2 and len(row) != 4:
                    error_code = 10006   
                    print("[error_code = 10006] row:{}, idx:{}".format(row, idx))
            elif is_KISLER_file == 1:
                #print("is_KISLER_file")
                # serach abs key word
                if 'abs' in row[0]:
                    KISLER_abs_idx = idx

                # found key word
                if KISLER_abs_idx != -1:
                    #print("found key word")
                    data_start_idx = KISLER_abs_idx + 2
                    if (
                        idx >=data_start_idx and 
                        len(row) == 1 and 
                        row[0] != ''                
                       ):
                        split_list = row[0].split()
                        #print("split_list:{}").format(split_list)

                        #assert False
                        try:
                            time_sec_tick += [float(split_list[0])]
                            force_N_1 += [-1]
                            force_N_2 += [-1]
                            force_N_join += [float(split_list[1])]
                        except:
                            error_code = 10005
                    elif (
                          idx >=data_start_idx and 
                          len(row) >= 2 and 
                          row[0] != '' and
                          row[1] != ''               
                        ):
                        #print("two column KISLER")
                        try:
                            time_sec_tick += [float(row[0])]
                            force_N_1 += [-1]
                            force_N_2 += [-1]
                            force_N_join += [float(row[1])]
                        except:
                            error_code = 10004


            idx += 1

    #print("idx:{}".format(idx))
    if len(time_sec_tick) > 0 and time_sec_tick[0] != 0:
        error_code = 10002

    return time_sec_tick, force_N_1, force_N_2, force_N_join, error_code




