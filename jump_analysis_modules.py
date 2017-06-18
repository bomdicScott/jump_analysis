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


def get_analysis_list(file_list):

    csv_list = []
    plot_list = []
    for f in file_list:
        if ('.csv' in f )and ('analysis_results' not in f) and ('_statistics' not in f) and ('dual_input' not in f):
            csv_list += [f.replace('.csv','')]

        if '.png' in f:
            plot_list += [f]

    #print("[Jump Analysis Modules] csv_list:{}".format(csv_list))
    #print("[Jump Analysis Modules] plot_list:{}".format(plot_list))

    analysis_list = []
    for c_name in csv_list:
        output_detected = 0
        for p_name in plot_list:
            if c_name in p_name:
                output_detected = 1
        if output_detected == 0:
            analysis_list += [c_name]
    print("[Jump Analysis Modules] analysis_list:{}".format(analysis_list))

    return analysis_list


