# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.dates as md
import csv
import json
import numpy as np
import os
import dateutil
import datetime
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from math import radians, cos, sin, asin, sqrt


def get_fig_ULDJ_analysis(s_ULDJ_contact_time_sec,
                           s_ULDJ_fly_contact_ratio,
                           s_ULDJ_RSI_mod,
                           s_ULDJ_date,
                           s_ULDJ_epoch_time_sec,
                           s_avg_ULDJ_contact_time_sec,
                           s_avg_ULDJ_fly_contact_ratio,
                           s_avg_ULDJ_RSI_mod,
                           s_avg_ULDJ_date,
                           s_avg_ULDJ_epoch_time_sec):

    fig = plt.figure(figsize=[10,15])

    ax = fig.add_subplot(311)
    ax.set_title('ULDJ_analysis')
    ax.plot(s_ULDJ_epoch_time_sec, s_ULDJ_contact_time_sec, 'bo', label='CT')
    ax.plot(s_avg_ULDJ_epoch_time_sec, s_avg_ULDJ_contact_time_sec, 'r', label='avg_CT')
    ax.set_ylabel('sec')
    ax.grid(True)
    ax.set_xlim(min(s_avg_ULDJ_epoch_time_sec) - 86400*3, max(s_avg_ULDJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])

    ax = fig.add_subplot(312)
    ax.plot(s_ULDJ_epoch_time_sec, s_ULDJ_fly_contact_ratio, 'bo', label='fly_contact_ratio')
    ax.plot(s_avg_ULDJ_epoch_time_sec, s_avg_ULDJ_fly_contact_ratio, 'r', label='avg_fly_contact_ratio')
    ax.set_ylabel('sec')
    ax.grid(True)
    ax.set_xlim(min(s_avg_ULDJ_epoch_time_sec) - 86400*3, max(s_avg_ULDJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])

    ax = fig.add_subplot(313)
    ax.plot(s_ULDJ_epoch_time_sec, s_ULDJ_RSI_mod, 'bo', label='RSI_mod')
    ax.plot(s_avg_ULDJ_epoch_time_sec, s_avg_ULDJ_RSI_mod, 'r', label='avg_RSI_mod')
    ax.set_ylabel('N/s')
    ax.grid(True)
    ax.set_xlim(min(s_avg_ULDJ_epoch_time_sec) - 86400*3, max(s_avg_ULDJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])



    for i in range(len(s_avg_ULDJ_date)):
        s_avg_ULDJ_date[i] = int(s_avg_ULDJ_date[i])

    ax.set_xticks(s_avg_ULDJ_epoch_time_sec)
    ax.set_xticklabels(s_avg_ULDJ_date, rotation=45, ha='left')


    return fig

def get_fig_LDJ_analysis(s_LDJ_contact_time_sec,
                          s_LDJ_fly_contact_ratio,
                          s_LDJ_RSI_mod,
                          s_LDJ_date,
                          s_LDJ_epoch_time_sec,
                          s_avg_LDJ_contact_time_sec,
                          s_avg_LDJ_fly_contact_ratio,
                          s_avg_LDJ_RSI_mod,
                          s_avg_LDJ_date,
                          s_avg_LDJ_epoch_time_sec):
    #print("s_LDJ_epoch_time_sec:{}".format(s_LDJ_epoch_time_sec))
    #print("s_avg_LDJ_epoch_time_sec:{}".format(s_avg_LDJ_epoch_time_sec))
    #print("s_LDJ_contact_time_sec:{}".format(s_LDJ_contact_time_sec))
    #print("s_avg_LDJ_contact_time_sec:{}".format(s_avg_LDJ_contact_time_sec))

    fig = plt.figure(figsize=[10,15])

    ax = fig.add_subplot(311)
    ax.set_title('LDJ_analysis')
    ax.plot(s_LDJ_epoch_time_sec, s_LDJ_contact_time_sec, 'bo', label='CT')
    ax.plot(s_avg_LDJ_epoch_time_sec, s_avg_LDJ_contact_time_sec, 'r', label='avg_CT')
    ax.set_ylabel('sec')
    ax.grid(True)
    ax.set_xlim(min(s_avg_LDJ_epoch_time_sec) - 86400*3, max(s_avg_LDJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])

    ax = fig.add_subplot(312)
    ax.plot(s_LDJ_epoch_time_sec, s_LDJ_fly_contact_ratio, 'bo', label='fly_contact_ratio')
    ax.plot(s_avg_LDJ_epoch_time_sec, s_avg_LDJ_fly_contact_ratio, 'r', label='avg_fly_contact_ratio')
    ax.set_ylabel('sec')
    ax.grid(True)
    ax.set_xlim(min(s_avg_LDJ_epoch_time_sec) - 86400*3, max(s_avg_LDJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])

    ax = fig.add_subplot(313)
    ax.plot(s_LDJ_epoch_time_sec, s_LDJ_RSI_mod, 'bo', label='RSI_mod')
    ax.plot(s_avg_LDJ_epoch_time_sec, s_avg_LDJ_RSI_mod, 'r', label='avg_RSI_mod')
    ax.set_ylabel('N/s')
    ax.grid(True)
    ax.set_xlim(min(s_avg_LDJ_epoch_time_sec) - 86400*3, max(s_avg_LDJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])



    for i in range(len(s_avg_LDJ_date)):
        s_avg_LDJ_date[i] = int(s_avg_LDJ_date[i])

    ax.set_xticks(s_avg_LDJ_epoch_time_sec)
    ax.set_xticklabels(s_avg_LDJ_date, rotation=45, ha='left')


    return fig

def get_fig_DJ_time_force_notiation(data_name, time_sec_tick, force_N_join, landing_start, landing_start_tick, landing_end, landing_end_tick, air_start, air_start_tick, air_end, air_end_tick, fly_time_sec, contact_time_sec, fly_contact_ratio, RSI_mod):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(time_sec_tick, force_N_join, 'k', label='force join')
    
    ax.plot(time_sec_tick[landing_start_tick], force_N_join[landing_start_tick], 'bo', label='landing_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[landing_end_tick], force_N_join[landing_end_tick], 'bo', label='landing_end', fillstyle = 'none', markeredgecolor = 'b', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[air_start_tick], force_N_join[air_start_tick], 'ro', label='air_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[air_end_tick], force_N_join[air_end_tick], 'ro', label='air_end', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)

    ax.set_title(data_name)
    #ax.set_xlabel('distance (km)')
    ax.set_ylabel('Force (N)')
    ax.legend(loc='upper left')

    Xlim = max(time_sec_tick)
    Ylim = max(force_N_join) * 3.0

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim)
    ax.grid(True)
    ax.set_xlabel('time (sec)')

    # fly_time_sec, contact_time_sec, fly_contact_ratio, RSI_mod, jump_height_m
    # round
    '''
    fly_time_sec, contact_time_sec, fly_contact_ratio, RSI_mod
    '''
    fly_time_sec = round(fly_time_sec,3)
    contact_time_sec = round(contact_time_sec,3)
    fly_contact_ratio = round(fly_contact_ratio,3)
    RSI_mod = round(RSI_mod,3)

    ax.text(Xlim*0.4,Ylim * 0.9,'FT:{} sec'.format(fly_time_sec), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.4,Ylim * (0.9 - 0.05),'CT:{} sec'.format(contact_time_sec), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.4,Ylim * (0.9 - 0.10),'fly_contact_ratio:{} '.format(fly_contact_ratio), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.4,Ylim * (0.9 - 0.15),'RSI_mod:{}'.format(RSI_mod), bbox=dict(facecolor='white', edgecolor='none'))
    

    return fig