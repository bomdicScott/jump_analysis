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

def get_fig_IMTP_time_force_notiation(data_name, time_sec_tick, force_N_join, stable_start, stable_start_tick, stable_end, stable_end_tick, pull_start, pull_start_tick, pf, pf_tick, pull_end, pull_end_tick, TtPF_sec, RFD, RFD_20ms, RFD_30ms, RFD_50ms, RFD_90ms, RFD_100ms, RFD_150ms, RFD_200ms, RFD_250ms, imp_20ms, imp_30ms, imp_50ms, imp_90ms, imp_100ms, imp_150ms, imp_200ms, imp_250ms, imp_total, PF, pRFD, pRFD_sec):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(time_sec_tick, force_N_join, 'k', label='force join')
    
    ax.plot(time_sec_tick[stable_start_tick], force_N_join[stable_start_tick], 'go', label='stable_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[stable_end_tick], force_N_join[stable_end_tick], 'go', label='stable_end', fillstyle = 'none', markeredgecolor = 'g', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[pull_start_tick], force_N_join[pull_start_tick], 'ro', label='pull_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[pf_tick], force_N_join[pf_tick], 'r^', label='pf', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)
    ax.plot(pRFD_sec, force_N_join[int(pRFD_sec*1000)], 'rv', label='pRFD', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)
    
    ax.plot(time_sec_tick[pull_end_tick], force_N_join[pull_end_tick], 'ro', label='pull_end', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)

    ax.set_title(data_name)
    #ax.set_xlabel('distance (km)')
    ax.set_ylabel('Force (N)')
    ax.legend(loc='upper left')

    Xlim = max(time_sec_tick)
    Ylim = max(force_N_join) * 3.5

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim)
    ax.grid(True)
    ax.set_xlabel('time (sec)')

    # fly_time_sec, contact_time_sec, TtPF_sec, RFD, jump_height_m
    # round
    TtPF_sec = round(TtPF_sec, 3)
    RFD = round(RFD, 3)
    RFD_20ms = round(RFD_20ms, 3)
    RFD_30ms = round(RFD_30ms, 3)
    RFD_50ms = round(RFD_50ms, 3)
    RFD_90ms = round(RFD_90ms, 3)
    RFD_100ms = round(RFD_100ms, 3)
    RFD_150ms = round(RFD_150ms, 3)
    RFD_200ms = round(RFD_200ms, 3)
    RFD_250ms = round(RFD_250ms, 3)
    imp_20ms = round(imp_20ms, 3)
    imp_30ms = round(imp_30ms, 3)
    imp_50ms = round(imp_50ms, 3)
    imp_90ms = round(imp_90ms, 3)
    imp_100ms = round(imp_100ms, 3)
    imp_150ms = round(imp_150ms, 3)
    imp_200ms = round(imp_200ms, 3)
    imp_250ms = round(imp_250ms, 3)
    imp_total = round(imp_total, 3)
    pRFD = round(pRFD,3)
    pRFD_sec = round(pRFD_sec,3)

    ax.text(Xlim*0.35,Ylim * 0.9,'TtPF_sec:{} sec'.format(TtPF_sec), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.35,Ylim * (0.9 - 0.05),'RFD:{} N/sec'.format(RFD), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.35,Ylim * (0.9 - 0.10),'RFD_20ms:{} N/sec'.format(RFD_20ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.35,Ylim * (0.9 - 0.15),'RFD_30ms:{} N/sec'.format(RFD_30ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.35,Ylim * (0.9 - 0.20),'RFD_50ms:{} N/sec'.format(RFD_50ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.35,Ylim * (0.9 - 0.25),'RFD_90ms:{} N/sec'.format(RFD_90ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.35,Ylim * (0.9 - 0.30),'RFD_100ms:{} N/sec'.format(RFD_100ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.35,Ylim * (0.9 - 0.35),'RFD_150ms:{} N/sec'.format(RFD_150ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.35,Ylim * (0.9 - 0.40),'RFD_200ms:{} N/sec'.format(RFD_200ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.35,Ylim * (0.9 - 0.45),'RFD_250ms:{} N/sec'.format(RFD_250ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.35,Ylim * (0.9 - 0.50),'pRFD:{} N/sec'.format(pRFD), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.35,Ylim * (0.9 - 0.55),'pRFD_sec:{} sec'.format(pRFD_sec), bbox=dict(facecolor='white', edgecolor='none'))

    ax.text(Xlim*0.75,Ylim * 0.9,'PF:{} N'.format(PF), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.75,Ylim * (0.9 - 0.05),'imp_total:{} N.sec'.format(imp_total), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.75,Ylim * (0.9 - 0.10),'imp_20ms:{} N.sec'.format(imp_20ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.75,Ylim * (0.9 - 0.15),'imp_30ms:{} N.sec'.format(imp_30ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.75,Ylim * (0.9 - 0.20),'imp_50ms:{} N.sec'.format(imp_50ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.75,Ylim * (0.9 - 0.25),'imp_90ms:{} N.sec'.format(imp_90ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.75,Ylim * (0.9 - 0.30),'imp_100ms:{} N.sec'.format(imp_100ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.75,Ylim * (0.9 - 0.35),'imp_150ms:{} N.sec'.format(imp_150ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.75,Ylim * (0.9 - 0.40),'imp_200ms:{} N.sec'.format(imp_200ms), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.75,Ylim * (0.9 - 0.45),'imp_250ms:{} N.sec'.format(imp_250ms), bbox=dict(facecolor='white', edgecolor='none'))

    #fig.show()
    #plt.show()

    return fig