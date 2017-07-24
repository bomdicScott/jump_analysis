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
from collections import defaultdict

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

def read_analysis_result_d(result_path, feature_list):

    feature_d = {}
    f = open(result_path, 'rU')
    for row in csv.DictReader(f): 
        for feature in feature_list:
            if (
                feature != 'date' and 
                feature != 'jump_type' and 
                feature != 'try_num'
               ):
                feature_d[feature] = row[feature]
    
    data_name_split = feature_d['data_name'].split('_')
    if len(data_name_split) == 4 and len(data_name_split[1]) == 8 and data_name_split[1][0:2] == '20' and 't' in data_name_split[3]:
        feature_d['date'] = data_name_split[1]
        feature_d['jump_type'] = data_name_split[2]
        feature_d['try_num'] = data_name_split[3]
    else:
        feature_d['date'] = ['NA']
        feature_d['jump_type'] = ['NA']
        feature_d['try_num'] = ['NA']

    return feature_d


def update_user_IMTP_statistics(data_dir):

    file_list = os.listdir(data_dir)
    result_list = get_IMTP_analysis_result_list(file_list)
    user_statistics_path = data_dir + '____user_IMTP_statistics.csv'

    feature_list = ['data_name', 'TtPF_sec', 'RFD', 'RFD_20ms', 'RFD_30ms', 'RFD_50ms', 'RFD_90ms', 'RFD_100ms', 'RFD_150ms', 'RFD_200ms', 'RFD_250ms', 'imp_20ms', 'imp_30ms', 'imp_50ms', 'imp_90ms', 'imp_100ms', 'imp_150ms', 'imp_200ms', 'imp_250ms', 'imp_total', 'PF', 'date', 'jump_type', 'try_num', 'pRFD', 'pRFD_sec']

    s_feature_d = defaultdict(list)
    for feature in feature_list:
        s_feature_d['s_'+feature] = []
    print("s_feature_d:{}".format(s_feature_d))

    for result_name in result_list:
        result_path = data_dir + result_name

        if os.path.exists(result_path):
            feature_d = read_analysis_result_d(result_path, feature_list)
            print("feature_d:{}".format(feature_d))

            for feature in feature_list:
                #print("s_feature_d['s_'+feature]:{}".format(s_feature_d['s_'+feature]))
                s_feature_d['s_'+feature] += [feature_d[feature]]

    print("s_feature_d:{}".format(s_feature_d))

    csv_header = []
    for feature in feature_list:
        csv_header += ['s_'+feature]

    with open(user_statistics_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(s_feature_d['s_data_name'])+1):
            data = []
            if row == 0:
                data = csv_header
            else:
                for col in range(len(csv_header)):
                    #print("csv_header[col]:{}".format((csv_header[col])))
                    #print("len:{}".format(len(eval(csv_header[col]))))
                    data += [s_feature_d[csv_header[col]][row-1]]
            writer.writerow(data)
        csvfile.close()

    















