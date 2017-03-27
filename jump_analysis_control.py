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

#########################################
workspace_dir = "{}/".format(os.getcwd())

users_dir = workspace_dir + "test_data/"
dual_input_dir = workspace_dir + "dual_input/"

#users_dir = workspace_dir # for windows

print("users_dir:{}".format(users_dir))

# dispatch files in dual input folder
DPM.dispatch_daul_input(dual_input_dir, users_dir)


file_list = os.listdir(users_dir)
user_list = []
for f_name in file_list:
    dir_path = users_dir + "{}".format(f_name)
    if os.path.isdir(dir_path):
        user_list += [f_name]
print("user_list:{}".format(user_list))        
#print("this is a test version")

for user_name in user_list:
    data_dir = users_dir + "{}/".format(user_name)
    
    DPM.copy_txt_as_csv(data_dir)

    SUAC.single_user_analysis(data_dir)
    
    #[TODO] add user statistics
    SUAC.update_user_statistics(data_dir)












