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

def get_DJ_record_statistics(T, time_sec_tick, force_N_join, landing_start, landing_start_tick, landing_end, landing_end_tick, air_start, air_start_tick, air_end, air_end_tick):

    # statistics
    fly_time_sec = air_end - air_start
    contact_time_sec = landing_end - landing_start
    fly_contact_ratio = fly_time_sec / contact_time_sec
    if fly_time_sec == 0:
        RSI_mod = 0
    else:
        RSI_mod = contact_time_sec / fly_time_sec
    jump_height_m = 0.5 * 9.8 * (0.5 * fly_time_sec)**2

    print("fly_time_sec:{}".format(fly_time_sec))
    print("contact_time_sec:{}".format(contact_time_sec))
    print("fly_contact_ratio:{}".format(fly_contact_ratio))
    print("RSI_mod:{}".format(RSI_mod))
    print("jump_height_m:{}".format(jump_height_m))

    return fly_time_sec, contact_time_sec, fly_contact_ratio, RSI_mod, jump_height_m

def get_DJ_features_of_join_force(data_name, time_sec_tick, force_N_join):
    print("get_DJ_features_of_join_force")

    stages = ['before_jump', 'landing', 'on_air', 'landing_again']
    stg_num = 0

    before_jump_length = 0

    landing_start = -1
    landing_start_tick = -1

    landing_end = -1
    landing_end_tick = -1

    air_start = -1
    air_start_tick = -1

    air_end = -1
    air_end_tick = -1

    print("data_name:{}".format(data_name))
    print("[Stage:{}]".format(stages[stg_num]))
    for i in range(len(time_sec_tick)):

        if stg_num == 0:
            if force_N_join[i] < 100.0:
                before_jump_length += 1
            else:
                if before_jump_length > 500:
                    # landing
                    stg_num = 1
                    print("[Stage:{}]".format(stages[stg_num]))
                    landing_start = time_sec_tick[i]
                    landing_start_tick = i
                    print("landing_start:{}".format(landing_start))
                    print("landing_start_tick:{}".format(landing_start_tick))
                else:
                    before_jump_length = 0

        if stg_num == 1:
            if force_N_join[i] < 100.0 and (i-landing_start_tick) > 50:
                # on_air
                stg_num = 2
                print("[Stage:{}]".format(stages[stg_num]))
                landing_end = time_sec_tick[i]
                landing_end_tick = i
                air_start = landing_end
                air_start_tick = landing_end_tick
                print("landing_end:{}".format(landing_end))
                print("landing_end_tick:{}".format(landing_end_tick))

        if stg_num == 2:
            # on_air stage
            if force_N_join[i] > 100.0 and (i-air_start_tick)>=100:
                # landing again
                stg_num = 3
                print("[Stage:{}]".format(stages[stg_num]))
                air_end = time_sec_tick[i]
                air_end_tick = i
                print("air_end:{}".format(air_end))
                print("air_end_tick:{}".format(air_end_tick))


    return stg_num, landing_start, landing_start_tick, landing_end, landing_end_tick, air_start, air_start_tick, air_end, air_end_tick


















