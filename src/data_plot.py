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


def get_fig_no_data_with_err_msg(error_code,err_msg):
    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.text(1,10,err_msg, color='red',bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(1,12,"error_code:{}".format(error_code), color='red',bbox=dict(facecolor='white', edgecolor='none'))

    return fig

def get_fig_time_force_with_err_msg(time_sec_tick, force_N_join, err_msg, data_name):
    fig = plt.figure()

    ax = fig.add_subplot(111)

    ax.plot(time_sec_tick, force_N_join, 'b', label='force join')
    ax.set_title(data_name)
    #ax.set_title('Heartrate')
    #ax.set_xlabel('distance (km)')
    ax.set_ylabel('Force (N)')
    ax.legend(loc='upper left')

    Xlim = max(time_sec_tick)
    Ylim = max(force_N_join) * 1.3

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim)
    ax.grid(True)
    ax.set_xlabel('time (sec)')

    ax.text(Xlim * 0.1,Ylim * 0.8,err_msg, color='red',bbox=dict(facecolor='white', edgecolor='none'))

    return fig


def get_fig_time_force(data_name, time_sec_tick, force_N_1, force_N_2, force_N_join):
    fig = plt.figure()

    ax = fig.add_subplot(311)

    ax.plot(time_sec_tick, force_N_1, 'b', label='force 1')

    ax.set_title(data_name)
    #ax.set_xlabel('distance (km)')
    ax.set_ylabel('Force (N)')
    ax.legend(loc='upper left')

    Xlim = max(time_sec_tick)
    Ylim = max(force_N_1) * 1.3

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim)
    ax.grid(True)

    ax = fig.add_subplot(312)

    ax.plot(time_sec_tick, force_N_2, 'b', label='force 2')

    #ax.set_title('Heartrate')
    #ax.set_xlabel('distance (km)')
    ax.set_ylabel('Force (N)')
    ax.legend(loc='upper left')

    Xlim = max(time_sec_tick)
    Ylim = max(force_N_2) * 1.3

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim)
    ax.grid(True)

    ax = fig.add_subplot(313)

    ax.plot(time_sec_tick, force_N_join, 'b', label='force join')

    #ax.set_title('Heartrate')
    #ax.set_xlabel('distance (km)')
    ax.set_ylabel('Force (N)')
    ax.legend(loc='upper left')

    Xlim = max(time_sec_tick)
    Ylim = max(force_N_join) * 1.3

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim)
    ax.grid(True)
    ax.set_xlabel('time (sec)')

    return fig

def get_fig_time_f_a_v_p(data_name, time_sec_tick, force_N_join, a_mss, v_mps, p_watt, pf_tick, p_watt_max_tick):

    fig = plt.figure(figsize=(15,10))


    ax = fig.add_subplot(221)
    ax.plot(time_sec_tick, force_N_join, 'b', label='force join')
    ax.set_ylabel('Force (N)')
    ax.legend(loc='upper left')

    ax.plot(time_sec_tick[pf_tick], force_N_join[pf_tick], 'ro')
    ax.plot(time_sec_tick[p_watt_max_tick], force_N_join[p_watt_max_tick], 'yo')

    Xlim = max(time_sec_tick)
    Ylim = max(force_N_join) * 1.3

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim)
    ax.grid(True)
    #ax.set_xlabel('time (sec)')

    ax = fig.add_subplot(222)
    ax.plot(time_sec_tick, a_mss, 'b', label='Acc')
    ax.plot(time_sec_tick[pf_tick], a_mss[pf_tick], 'ro')
    ax.plot(time_sec_tick[p_watt_max_tick], a_mss[p_watt_max_tick], 'yo')
    ax.set_ylabel('Acc (m/s^2)')
    ax.legend(loc='upper left')

    ax.grid(True)
    #ax.set_xlabel('time (sec)')

    ax = fig.add_subplot(223)
    ax.plot(time_sec_tick, v_mps, 'b', label='Speed')
    ax.plot(time_sec_tick[pf_tick], v_mps[pf_tick], 'ro')
    ax.plot(time_sec_tick[p_watt_max_tick], v_mps[p_watt_max_tick], 'yo')
    ax.set_ylabel('V (m/s)')
    ax.legend(loc='upper left')

    ax.grid(True)
    ax.set_xlabel('time (sec)')

    ax = fig.add_subplot(224)
    ax.plot(time_sec_tick, p_watt, 'b', label='Power')
    ax.plot(time_sec_tick[pf_tick], p_watt[pf_tick], 'ro')
    ax.plot(time_sec_tick[p_watt_max_tick], p_watt[p_watt_max_tick], 'yo')
    ax.set_ylabel('watts')
    ax.legend(loc='upper left')

    ax.grid(True)
    ax.set_xlabel('time (sec)')

    return fig





