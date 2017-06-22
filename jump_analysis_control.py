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
import single_user_analysis_control as SUAC
from subprocess import check_output
import copy
#########################################
workspace_dir = "{}/".format(os.getcwd())

# for develop enviroment in mac 
#users_dir = workspace_dir + "test_data/"
#simualte formal user folder
users_dir = workspace_dir.replace('jump_analysis','jump_analysis_data')
print("users_dir:{}".format(users_dir))
dual_input_dir = users_dir + "_dual_input/"


# for app enviroment in windows
#users_dir = workspace_dir # for windows
#print("users_dir:{}".format(users_dir))
#dual_input_dir = workspace_dir + '_dual_input/'

print("users_dir:{}".format(users_dir))


enable_sys_fig_show = 1

#########################################

# dispatch files in dual input folder
list_new_error_fig_path = DPM.dispatch_daul_input(dual_input_dir, users_dir)

file_list = os.listdir(users_dir)
user_list = []
for f_name in file_list:
    dir_path = users_dir + "{}".format(f_name)
    if os.path.isdir(dir_path) and (not '_dual' in dir_path):
        user_list += [f_name]
print("user_list:{}".format(user_list))        
#print("this is a test version")


for user_name in user_list:
    data_dir = users_dir + "{}/".format(user_name)
    
    DPM.copy_txt_as_csv(data_dir)

    list_new_error_fig_path, list_new_fig_time_force_notiation_path, analysis_list = SUAC.single_user_analysis(data_dir)
    print("list_new_error_fig_path:{}".format(list_new_error_fig_path))
    print("list_new_fig_time_force_notiation_path:{}".format(list_new_fig_time_force_notiation_path))
    print("analysis_list:{}".format(analysis_list))
    
    #[TODO] add user statistics
    if analysis_list != []:
        SUAC.update_user_CMJ_statistics(data_dir)
        SUAC.update_user_SJ_statistics(data_dir)
        SUAC.update_user_DJ_statistics(data_dir)

if enable_sys_fig_show == 1:
    plt.show()









