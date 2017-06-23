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

def get_IMTP_analysis_result_list(file_list):
    result_list = []
    for f_name in file_list:
        if 'analysis_results.csv' in f_name and 'IMTP' in f_name:
            result_list += [f_name]
    #print("result_list:{}".format(result_list))

    return result_list

def read_analysis_result(result_path):
    
    #print("result_path:{}".format(result_path))

    f = open(result_path, 'rU')
    for row in csv.DictReader(f): 
        data_name = row['data_name']
        TtPF_sec = row['TtPF_sec']
        RFD = row['RFD']
        RFD_20ms = row['RFD_20ms']
        RFD_30ms = row['RFD_30ms']
        RFD_50ms = row['RFD_50ms']
        RFD_90ms = row['RFD_90ms']
        RFD_100ms = row['RFD_100ms']
        RFD_150ms = row['RFD_150ms']
        RFD_200ms = row['RFD_200ms']
        RFD_250ms = row['RFD_250ms']
        imp_20ms = row['imp_20ms']
        imp_30ms = row['imp_30ms']
        imp_50ms = row['imp_50ms']
        imp_90ms = row['imp_90ms']
        imp_100ms = row['imp_100ms']
        imp_150ms = row['imp_150ms']
        imp_200ms = row['imp_200ms']
        imp_250ms = row['imp_250ms']
        imp_total = row['imp_total']
        PF = row['PF']
        
    return data_name,TtPF_sec, RFD, RFD_20ms, RFD_30ms, RFD_50ms, RFD_90ms, RFD_100ms, RFD_150ms, RFD_200ms, RFD_250ms, imp_20ms, imp_30ms, imp_50ms, imp_90ms, imp_100ms, imp_150ms, imp_200ms, imp_250ms, imp_total, PF


def update_user_IMTP_statistics(data_dir):

    file_list = os.listdir(data_dir)
    result_list = get_IMTP_analysis_result_list(file_list)
    user_statistics_path = data_dir + '____user_IMTP_statistics.csv'

    s_data_name = []
    s_TtPF_sec = []
    s_RFD = []
    s_RFD_20ms = []
    s_RFD_30ms = []
    s_RFD_50ms = []
    s_RFD_90ms = []
    s_RFD_100ms = []
    s_RFD_150ms = []
    s_RFD_200ms = []
    s_RFD_250ms = []
    s_imp_20ms = []
    s_imp_30ms = []
    s_imp_50ms = []
    s_imp_90ms = []
    s_imp_100ms = []
    s_imp_150ms = []
    s_imp_200ms = []
    s_imp_250ms = []
    s_imp_total = []
    s_PF = []
    s_date = []
    s_jump_type = []
    s_try_num = []

    for result_name in result_list:
        result_path = data_dir + result_name

        if os.path.exists(result_path):
            data_name,TtPF_sec, RFD, RFD_20ms, RFD_30ms, RFD_50ms, RFD_90ms, RFD_100ms, RFD_150ms, RFD_200ms, RFD_250ms, imp_20ms, imp_30ms, imp_50ms, imp_90ms, imp_100ms, imp_150ms, imp_200ms, imp_250ms, imp_total, PF = read_analysis_result(result_path)


            s_data_name += [data_name]
            s_TtPF_sec += [TtPF_sec]
            s_RFD += [RFD]
            s_RFD_20ms += [RFD_20ms]
            s_RFD_30ms += [RFD_30ms]
            s_RFD_50ms += [RFD_50ms]
            s_RFD_90ms += [RFD_90ms]
            s_RFD_100ms += [RFD_100ms]
            s_RFD_150ms += [RFD_150ms]
            s_RFD_200ms += [RFD_200ms]
            s_RFD_250ms += [RFD_250ms]
            s_imp_20ms += [imp_20ms]
            s_imp_30ms += [imp_30ms]
            s_imp_50ms += [imp_50ms]
            s_imp_90ms += [imp_90ms]
            s_imp_100ms += [imp_100ms]
            s_imp_150ms += [imp_150ms]
            s_imp_200ms += [imp_200ms]
            s_imp_250ms += [imp_250ms]
            s_imp_total += [imp_total]
            s_PF += [PF]

            # if data_name uses standard format
            data_name_split = data_name.split('_')
            #print("data_name_split:{}".format(data_name_split))

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
    csv_header += ["s_TtPF_sec"]
    csv_header += ["s_RFD"]
    csv_header += ["s_RFD_20ms"]
    csv_header += ["s_RFD_30ms"]
    csv_header += ["s_RFD_50ms"]
    csv_header += ["s_RFD_90ms"]
    csv_header += ["s_RFD_100ms"]
    csv_header += ["s_RFD_150ms"]
    csv_header += ["s_RFD_200ms"]
    csv_header += ["s_RFD_250ms"]
    csv_header += ["s_imp_20ms"]
    csv_header += ["s_imp_30ms"]
    csv_header += ["s_imp_50ms"]
    csv_header += ["s_imp_90ms"]
    csv_header += ["s_imp_100ms"]
    csv_header += ["s_imp_150ms"]
    csv_header += ["s_imp_200ms"]
    csv_header += ["s_imp_250ms"]
    csv_header += ["s_imp_total"]
    csv_header += ["s_PF"]
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
















