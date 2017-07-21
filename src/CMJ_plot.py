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

def get_fig_CMJ_compare(s_avg_ULCMJ_date, s_avg_ULCMJ_epoch_time_sec, s_avg_ULCMJ_jump_height_m, s_avg_LCMJ_date, s_avg_LCMJ_epoch_time_sec, s_avg_LCMJ_jump_height_m):

    s_avg_ULCMJ_jump_height_cm = np.array(s_avg_ULCMJ_jump_height_m)*100.0
    s_avg_LCMJ_jump_height_cm = np.array(s_avg_LCMJ_jump_height_m)*100.0

    fig = plt.figure(figsize=[15,10])

    ax = fig.add_subplot(111)
    ax.set_title('CMJ_Jump_Height_Compare')
    ax.plot(s_avg_ULCMJ_epoch_time_sec, s_avg_ULCMJ_jump_height_cm, 'b', label='ULCMJ')
    ax.plot(s_avg_LCMJ_epoch_time_sec, s_avg_LCMJ_jump_height_cm, 'r', label='LCMJ')
    ax.set_ylabel('cm')
    ax.grid(True)
    ax.set_xlim(min(s_avg_ULCMJ_epoch_time_sec) - 86400*3, max(s_avg_ULCMJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    
    for i in range(len(s_avg_ULCMJ_date)):
        s_avg_ULCMJ_date[i] = int(s_avg_ULCMJ_date[i])

    ax.set_xticks(s_avg_ULCMJ_epoch_time_sec)
    ax.set_xticklabels(s_avg_ULCMJ_date, rotation=45, ha='left')

    return fig

def get_fig_ULCMJ_analysis(s_ULCMJ_contact_time_sec,
                           s_ULCMJ_TtPF_sec,
                           s_ULCMJ_RFD,
                           s_ULCMJ_jump_height_m,
                           s_ULCMJ_jump_power,
                           s_ULCMJ_date,
                           s_ULCMJ_epoch_time_sec,
                           s_avg_ULCMJ_contact_time_sec,
                           s_avg_ULCMJ_TtPF_sec,
                           s_avg_ULCMJ_RFD,
                           s_avg_ULCMJ_jump_height_m,
                           s_avg_ULCMJ_jump_power,
                           s_avg_ULCMJ_date,
                           s_avg_ULCMJ_epoch_time_sec):

    fig = plt.figure(figsize=[10,15])

    ax = fig.add_subplot(511)
    ax.set_title('ULCMJ_analysis')
    ax.plot(s_ULCMJ_epoch_time_sec, s_ULCMJ_contact_time_sec, 'bo', label='CT')
    ax.plot(s_avg_ULCMJ_epoch_time_sec, s_avg_ULCMJ_contact_time_sec, 'r', label='avg_CT')
    ax.set_ylabel('sec')
    ax.grid(True)
    ax.set_xlim(min(s_avg_ULCMJ_epoch_time_sec) - 86400*3, max(s_avg_ULCMJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])

    ax = fig.add_subplot(512)
    ax.plot(s_ULCMJ_epoch_time_sec, s_ULCMJ_TtPF_sec, 'bo', label='TtPF')
    ax.plot(s_avg_ULCMJ_epoch_time_sec, s_avg_ULCMJ_TtPF_sec, 'r', label='avg_TtPF')
    ax.set_ylabel('sec')
    ax.grid(True)
    ax.set_xlim(min(s_avg_ULCMJ_epoch_time_sec) - 86400*3, max(s_avg_ULCMJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])

    ax = fig.add_subplot(513)
    ax.plot(s_ULCMJ_epoch_time_sec, s_ULCMJ_RFD, 'bo', label='RFD')
    ax.plot(s_avg_ULCMJ_epoch_time_sec, s_avg_ULCMJ_RFD, 'r', label='avg_RFD')
    ax.set_ylabel('N/s')
    ax.grid(True)
    ax.set_xlim(min(s_avg_ULCMJ_epoch_time_sec) - 86400*3, max(s_avg_ULCMJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])

    ax = fig.add_subplot(514)
    ax.plot(s_ULCMJ_epoch_time_sec, s_ULCMJ_jump_height_m, 'bo', label='J_Height')
    ax.plot(s_avg_ULCMJ_epoch_time_sec, s_avg_ULCMJ_jump_height_m, 'r', label='avg_J_Height')
    ax.set_ylabel('meter')
    ax.grid(True)
    ax.set_xlim(min(s_avg_ULCMJ_epoch_time_sec) - 86400*3, max(s_avg_ULCMJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])

    ax = fig.add_subplot(515)
    ax.plot(s_ULCMJ_epoch_time_sec, s_ULCMJ_jump_power, 'bo', label='J_Power')
    ax.plot(s_avg_ULCMJ_epoch_time_sec, s_avg_ULCMJ_jump_power, 'r', label='avg_J_Power')
    ax.set_ylabel('Watts')
    ax.grid(True)
    ax.set_xlim(min(s_avg_ULCMJ_epoch_time_sec) - 86400*3, max(s_avg_ULCMJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)


    for i in range(len(s_avg_ULCMJ_date)):
        s_avg_ULCMJ_date[i] = int(s_avg_ULCMJ_date[i])

    ax.set_xticks(s_avg_ULCMJ_epoch_time_sec)
    ax.set_xticklabels(s_avg_ULCMJ_date, rotation=45, ha='left')


    return fig

def get_fig_LCMJ_analysis(s_LCMJ_contact_time_sec,
                          s_LCMJ_TtPF_sec,
                          s_LCMJ_RFD,
                          s_LCMJ_jump_height_m,
                          s_LCMJ_jump_power,
                          s_LCMJ_date,
                          s_LCMJ_epoch_time_sec,
                          s_avg_LCMJ_contact_time_sec,
                          s_avg_LCMJ_TtPF_sec,
                          s_avg_LCMJ_RFD,
                          s_avg_LCMJ_jump_height_m,
                          s_avg_LCMJ_jump_power,
                          s_avg_LCMJ_date,
                          s_avg_LCMJ_epoch_time_sec):
    #print("s_LCMJ_epoch_time_sec:{}".format(s_LCMJ_epoch_time_sec))
    #print("s_avg_LCMJ_epoch_time_sec:{}".format(s_avg_LCMJ_epoch_time_sec))
    #print("s_LCMJ_contact_time_sec:{}".format(s_LCMJ_contact_time_sec))
    #print("s_avg_LCMJ_contact_time_sec:{}".format(s_avg_LCMJ_contact_time_sec))

    fig = plt.figure(figsize=[10,15])

    ax = fig.add_subplot(511)
    ax.set_title('LCMJ_analysis')
    ax.plot(s_LCMJ_epoch_time_sec, s_LCMJ_contact_time_sec, 'bo', label='CT')
    ax.plot(s_avg_LCMJ_epoch_time_sec, s_avg_LCMJ_contact_time_sec, 'r', label='avg_CT')
    ax.set_ylabel('sec')
    ax.grid(True)
    ax.set_xlim(min(s_avg_LCMJ_epoch_time_sec) - 86400*3, max(s_avg_LCMJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])

    ax = fig.add_subplot(512)
    ax.plot(s_LCMJ_epoch_time_sec, s_LCMJ_TtPF_sec, 'bo', label='TtPF')
    ax.plot(s_avg_LCMJ_epoch_time_sec, s_avg_LCMJ_TtPF_sec, 'r', label='avg_TtPF')
    ax.set_ylabel('sec')
    ax.grid(True)
    ax.set_xlim(min(s_avg_LCMJ_epoch_time_sec) - 86400*3, max(s_avg_LCMJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])

    ax = fig.add_subplot(513)
    ax.plot(s_LCMJ_epoch_time_sec, s_LCMJ_RFD, 'bo', label='RFD')
    ax.plot(s_avg_LCMJ_epoch_time_sec, s_avg_LCMJ_RFD, 'r', label='avg_RFD')
    ax.set_ylabel('N/s')
    ax.grid(True)
    ax.set_xlim(min(s_avg_LCMJ_epoch_time_sec) - 86400*3, max(s_avg_LCMJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])

    ax = fig.add_subplot(514)
    ax.plot(s_LCMJ_epoch_time_sec, s_LCMJ_jump_height_m, 'bo', label='J_Height')
    ax.plot(s_avg_LCMJ_epoch_time_sec, s_avg_LCMJ_jump_height_m, 'r', label='avg_J_Height')
    ax.set_ylabel('meter')
    ax.grid(True)
    ax.set_xlim(min(s_avg_LCMJ_epoch_time_sec) - 86400*3, max(s_avg_LCMJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)
    ax.set_xticks([])

    ax = fig.add_subplot(515)
    ax.plot(s_LCMJ_epoch_time_sec, s_LCMJ_jump_power, 'bo', label='J_Power')
    ax.plot(s_avg_LCMJ_epoch_time_sec, s_avg_LCMJ_jump_power, 'r', label='avg_J_Power')
    ax.set_ylabel('Watts')
    ax.grid(True)
    ax.set_xlim(min(s_avg_LCMJ_epoch_time_sec) - 86400*3, max(s_avg_LCMJ_epoch_time_sec)+86400)
    leg = ax.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)


    for i in range(len(s_avg_LCMJ_date)):
        s_avg_LCMJ_date[i] = int(s_avg_LCMJ_date[i])

    ax.set_xticks(s_avg_LCMJ_epoch_time_sec)
    ax.set_xticklabels(s_avg_LCMJ_date, rotation=45, ha='left')


    return fig

def get_fig_CMJ_time_force_notiation(data_name, time_sec_tick, force_N_join, stable_start_tick, stable_end_tick, ec_start_tick, ec_acc_end_tick, ec_deacc_start_tick, pf_tick, air_start_tick, air_end_tick, fly_time_sec, contact_time_sec, TtPF_sec, RFD, jump_height_m, jump_power, PF, ec_deacc_end, ec_deacc_end_tick, co_start, co_start_tick, co_end, co_end_tick, pRFD, pRFD_sec):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(time_sec_tick, force_N_join, 'k', label='force join')
    
    ax.plot(time_sec_tick[stable_start_tick], force_N_join[stable_start_tick], 'go', label='stable_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[stable_end_tick], force_N_join[stable_end_tick], 'go', label='stable_end', fillstyle = 'none', markeredgecolor = 'g', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[ec_start_tick], force_N_join[ec_start_tick], 'bo', label='ec_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[ec_acc_end_tick], force_N_join[ec_acc_end_tick], 'bo', label='ec_acc_end', fillstyle = 'none', markeredgecolor = 'b', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[ec_deacc_start_tick], force_N_join[ec_deacc_start_tick], 'mo', label='ec_deacc_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[ec_deacc_end_tick], force_N_join[ec_deacc_end_tick], 'mo', label='ec_deacc_end', fillstyle = 'none', markeredgecolor = 'm', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[co_start_tick], force_N_join[co_start_tick], 'ro', label='co_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[co_end_tick], force_N_join[co_end_tick], 'mo', label='co_end', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[pf_tick], force_N_join[pf_tick], 'r^', label='pf', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)
    ax.plot(pRFD_sec, force_N_join[int(pRFD_sec*1000)], 'rv', label='pRFD', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[air_start_tick], force_N_join[air_start_tick], 'yo', label='air_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[air_end_tick], force_N_join[air_end_tick], 'yo', label='air_end', fillstyle = 'none', markeredgecolor = 'y', markersize = 10, markeredgewidth = 2)

    ax.set_title(data_name)
    #ax.set_xlabel('distance (km)')
    ax.set_ylabel('Force (N)')
    ax.legend(loc='upper left')

    Xlim = max(time_sec_tick)
    Ylim = PF * 4.5

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim)
    ax.grid(True)
    ax.set_xlabel('time (sec)')

    # fly_time_sec, contact_time_sec, TtPF_sec, RFD, jump_height_m
    # round
    fly_time_sec = round(fly_time_sec,3)
    contact_time_sec = round(contact_time_sec,3)
    TtPF_sec = round(TtPF_sec,3)
    RFD = round(RFD,3)
    jump_height_cm = round(jump_height_m*100.0,3)
    jump_power = round(jump_power,3)
    PF = round(PF,3)
    pRFD = round(pRFD,3)
    pRFD_sec = round(pRFD_sec,3)

    ax.text(Xlim*0.4,Ylim * 0.9,'FT:{} sec'.format(fly_time_sec), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.4,Ylim * (0.9 - 0.05),'CT:{} sec'.format(contact_time_sec), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.4,Ylim * (0.9 - 0.10),'TtPF:{} sec'.format(TtPF_sec), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.4,Ylim * (0.9 - 0.15),'RFD:{} N/sec'.format(RFD), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.4,Ylim * (0.9 - 0.20),'jump_height:{} cm'.format(jump_height_cm), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.4,Ylim * (0.9 - 0.25),'jump_power:{} W'.format(jump_power), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.4,Ylim * (0.9 - 0.30),'PF:{} N'.format(PF), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.4,Ylim * (0.9 - 0.35),'pRFD:{} N/sec'.format(pRFD), bbox=dict(facecolor='white', edgecolor='none'))
    ax.text(Xlim*0.4,Ylim * (0.9 - 0.40),'pRFD_sec:{} sec'.format(pRFD_sec), bbox=dict(facecolor='white', edgecolor='none'))

    #fig.show()
    #plt.show()

    return fig

def get_fig_CMJ_time_f_a_v_p(data_name, time_sec_tick, force_N_join, a_mss, v_mps, p_watt, p_watt_max_tick, stable_start_tick, stable_end_tick, ec_start_tick, ec_acc_end_tick, ec_deacc_start_tick, pf_tick, air_start_tick, air_end_tick, ec_deacc_end_tick, co_start_tick, co_end_tick, time_ecc_sec, time_con_sec, total_time_sec, fly_contact_ratio, RSI_mod, mean_co_force, velocity_pf, force_pf, pVelocity, mean_power_con, time_to_pp_sec, min_velocity, force_at_zero_velocity, mean_ec_con_power, velocity_take_off, imp_ec_deacc_con, RNI, imp_ec_acc, area_force_velocity, ec_displacement_cm, vertical_stiffness, RFD_20ms, RFD_30ms, RFD_50ms, RFD_90ms, RFD_100ms, RFD_150ms, RFD_200ms, RFD_250ms):

    # round
    
    time_ecc_sec = round(time_ecc_sec,3)
    time_con_sec = round(time_con_sec,3)
    total_time_sec = round(total_time_sec,3)
    fly_contact_ratio = round(fly_contact_ratio,3)
    RSI_mod = round(RSI_mod,3)
    mean_co_force = round(mean_co_force,3)
    velocity_pf = round(velocity_pf,3)
    force_pf = round(force_pf,3)
    pVelocity = round(pVelocity,3)
    mean_power_con = round(mean_power_con,3)
    time_to_pp_sec = round(time_to_pp_sec,3)
    min_velocity = round(min_velocity,3)
    force_at_zero_velocity = round(force_at_zero_velocity,3)
    mean_ec_con_power = round(mean_ec_con_power,3)
    velocity_take_off = round(velocity_take_off,3)
    imp_ec_deacc_con = round(imp_ec_deacc_con,3)
    RNI = round(RNI,3)
    imp_ec_acc = round(imp_ec_acc,3)
    area_force_velocity = round(area_force_velocity,3)
    ec_displacement_cm = round(ec_displacement_cm,3)
    vertical_stiffness = round(vertical_stiffness,3)

    RFD_20ms = round(RFD_20ms,3)
    RFD_30ms = round(RFD_30ms,3)
    RFD_50ms = round(RFD_50ms,3)
    RFD_90ms = round(RFD_90ms,3)
    RFD_100ms = round(RFD_100ms,3)
    RFD_150ms = round(RFD_150ms,3)
    RFD_200ms = round(RFD_200ms,3)
    RFD_250ms = round(RFD_250ms,3)
    

    fig = plt.figure(figsize=(15,10))


    ax = fig.add_subplot(221)
    ax.plot(time_sec_tick, force_N_join, 'b', label='force join')
    ax.set_ylabel('Force (N)')
    ax.legend(loc='upper left')

    #ax.plot(time_sec_tick[pf_tick], force_N_join[pf_tick], 'ro')
    #ax.plot(time_sec_tick[p_watt_max_tick], force_N_join[p_watt_max_tick], 'yo')
    data_line = force_N_join
    ax.plot(time_sec_tick[stable_start_tick], data_line[stable_start_tick], 'go', label='stable_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[stable_end_tick], data_line[stable_end_tick], 'go', label='stable_end', fillstyle = 'none', markeredgecolor = 'g', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[ec_start_tick], data_line[ec_start_tick], 'bo', label='ec_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[ec_acc_end_tick], data_line[ec_acc_end_tick], 'bo', label='ec_acc_end', fillstyle = 'none', markeredgecolor = 'b', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[ec_deacc_start_tick], data_line[ec_deacc_start_tick], 'mo', label='ec_deacc_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[ec_deacc_end_tick], data_line[ec_deacc_end_tick], 'mo', label='ec_deacc_end', fillstyle = 'none', markeredgecolor = 'm', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[co_start_tick], data_line[co_start_tick], 'ro', label='co_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[co_end_tick], data_line[co_end_tick], 'mo', label='co_end', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[pf_tick], data_line[pf_tick], 'r^', label='pf', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[air_start_tick], data_line[air_start_tick], 'yo', label='air_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[air_end_tick], data_line[air_end_tick], 'yo', label='air_end', fillstyle = 'none', markeredgecolor = 'y', markersize = 10, markeredgewidth = 2)

    Xlim = max(time_sec_tick)
    Ylim = max(force_N_join) * 1.3

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim)
    ax.grid(True)

    ax.text(Xlim*0.6,Ylim * 0.9,'mean_co_force:{} N'.format(mean_co_force), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.05),'force_pf:{} N'.format(force_pf), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.10),'force_at_zero_velocity:{} N'.format(force_at_zero_velocity), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.15),'imp_ec_deacc_con:{} N.s'.format(imp_ec_deacc_con), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.20),'RNI:{} N.s/kg'.format(RNI), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.25),'imp_ec_acc:{} N.s'.format(imp_ec_acc), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)

    if RFD_20ms > 0:
        ax.text(Xlim*0.6,Ylim * (0.9 - 0.30),'RFD_20ms:{} N/s'.format(RFD_20ms), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    if RFD_30ms > 0:
        ax.text(Xlim*0.6,Ylim * (0.9 - 0.35),'RFD_30ms:{} N/s'.format(RFD_30ms), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    if RFD_50ms > 0:
        ax.text(Xlim*0.6,Ylim * (0.9 - 0.40),'RFD_50ms:{} N/s'.format(RFD_50ms), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    if RFD_90ms > 0:
        ax.text(Xlim*0.6,Ylim * (0.9 - 0.45),'RFD_90ms:{} N/s'.format(RFD_90ms), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    if RFD_100ms > 0:
        ax.text(Xlim*0.6,Ylim * (0.9 - 0.50),'RFD_100ms:{} N/s'.format(RFD_100ms), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    if RFD_150ms > 0:
        ax.text(Xlim*0.6,Ylim * (0.9 - 0.55),'RFD_150ms:{} N/s'.format(RFD_150ms), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    if RFD_200ms > 0:
        ax.text(Xlim*0.6,Ylim * (0.9 - 0.60),'RFD_200ms:{} N/s'.format(RFD_200ms), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    if RFD_250ms > 0:
        ax.text(Xlim*0.6,Ylim * (0.9 - 0.65),'RFD_250ms:{} N/s'.format(RFD_250ms), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)


    #ax.set_xlabel('time (sec)')

    ax = fig.add_subplot(222)
    ax.plot(time_sec_tick, a_mss, 'b', label='Acc')
    #ax.plot(time_sec_tick[pf_tick], a_mss[pf_tick], 'ro')
    #ax.plot(time_sec_tick[p_watt_max_tick], a_mss[p_watt_max_tick], 'yo')
    data_line = a_mss
    ax.plot(time_sec_tick[stable_start_tick], data_line[stable_start_tick], 'go', label='stable_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[stable_end_tick], data_line[stable_end_tick], 'go', label='stable_end', fillstyle = 'none', markeredgecolor = 'g', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[ec_start_tick], data_line[ec_start_tick], 'bo', label='ec_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[ec_acc_end_tick], data_line[ec_acc_end_tick], 'bo', label='ec_acc_end', fillstyle = 'none', markeredgecolor = 'b', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[ec_deacc_start_tick], data_line[ec_deacc_start_tick], 'mo', label='ec_deacc_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[ec_deacc_end_tick], data_line[ec_deacc_end_tick], 'mo', label='ec_deacc_end', fillstyle = 'none', markeredgecolor = 'm', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[co_start_tick], data_line[co_start_tick], 'ro', label='co_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[co_end_tick], data_line[co_end_tick], 'mo', label='co_end', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[pf_tick], data_line[pf_tick], 'r^', label='pf', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[air_start_tick], data_line[air_start_tick], 'yo', label='air_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[air_end_tick], data_line[air_end_tick], 'yo', label='air_end', fillstyle = 'none', markeredgecolor = 'y', markersize = 10, markeredgewidth = 2)
    ax.set_ylabel('Acc (m/s^2)')
    #ax.legend(loc='upper left')

    Xlim = max(time_sec_tick)
    Ylim = max(data_line) * 1.3

    ax.set_xlim(0, Xlim)
    ax.set_ylim(ymax=Ylim)
    ax.grid(True)
    #ax.set_xlabel('time (sec)')
    Ylim = Ylim - min(data_line)
    ax.text(Xlim*0.6,Ylim * 0.9 + min(data_line),'time_ecc_sec:{} sec'.format(time_ecc_sec), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.05) + min(data_line),'time_con_sec:{} sec'.format(time_con_sec), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.10) + min(data_line),'total_time_sec:{} sec'.format(total_time_sec), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.15) + min(data_line),'RSI(fly_contact_ratio):{}'.format(fly_contact_ratio), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.20) + min(data_line),'RSI_mod:{} m/s'.format(RSI_mod), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.25) + min(data_line),'ec_displacement_cm:{} cm'.format(ec_displacement_cm), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.30) + min(data_line),'vertical_stiffness:{} N/cm'.format(vertical_stiffness), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)

    ax = fig.add_subplot(223)
    ax.plot(time_sec_tick, v_mps, 'b', label='Speed')
    #ax.plot(time_sec_tick[pf_tick], v_mps[pf_tick], 'ro')
    #ax.plot(time_sec_tick[p_watt_max_tick], v_mps[p_watt_max_tick], 'yo')
    data_line = v_mps
    ax.plot(time_sec_tick[stable_start_tick], data_line[stable_start_tick], 'go', label='stable_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[stable_end_tick], data_line[stable_end_tick], 'go', label='stable_end', fillstyle = 'none', markeredgecolor = 'g', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[ec_start_tick], data_line[ec_start_tick], 'bo', label='ec_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[ec_acc_end_tick], data_line[ec_acc_end_tick], 'bo', label='ec_acc_end', fillstyle = 'none', markeredgecolor = 'b', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[ec_deacc_start_tick], data_line[ec_deacc_start_tick], 'mo', label='ec_deacc_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[ec_deacc_end_tick], data_line[ec_deacc_end_tick], 'mo', label='ec_deacc_end', fillstyle = 'none', markeredgecolor = 'm', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[co_start_tick], data_line[co_start_tick], 'ro', label='co_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[co_end_tick], data_line[co_end_tick], 'mo', label='co_end', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[pf_tick], data_line[pf_tick], 'r^', label='pf', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[air_start_tick], data_line[air_start_tick], 'yo', label='air_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[air_end_tick], data_line[air_end_tick], 'yo', label='air_end', fillstyle = 'none', markeredgecolor = 'y', markersize = 10, markeredgewidth = 2)
    ax.set_ylabel('V (m/s)')
    #ax.legend(loc='upper left')

    Xlim = max(time_sec_tick)
    Ylim = max(data_line) * 1.3

    ax.set_xlim(0, Xlim)
    ax.set_ylim(ymax=Ylim)
    ax.grid(True)

    Ylim = Ylim - min(data_line)
    ax.text(Xlim*0.6,Ylim * 0.9 + min(data_line),'velocity_pf:{} m/s'.format(velocity_pf), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.05) + min(data_line),'pVelocity:{} m/s'.format(pVelocity), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.10) + min(data_line),'min_velocity:{} m/s'.format(min_velocity), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.15) + min(data_line),'velocity_take_off:{} m/s'.format(velocity_take_off), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.20) + min(data_line),'area_force_velocity:{} N.m/s'.format(area_force_velocity), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    
    ax.set_xlabel('time (sec)')

    ax = fig.add_subplot(224)
    ax.plot(time_sec_tick, p_watt, 'b', label='Power')
    #ax.plot(time_sec_tick[pf_tick], p_watt[pf_tick], 'ro')
    #ax.plot(time_sec_tick[p_watt_max_tick], p_watt[p_watt_max_tick], 'yo')
    data_line = p_watt
    ax.plot(time_sec_tick[stable_start_tick], data_line[stable_start_tick], 'go', label='stable_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[stable_end_tick], data_line[stable_end_tick], 'go', label='stable_end', fillstyle = 'none', markeredgecolor = 'g', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[ec_start_tick], data_line[ec_start_tick], 'bo', label='ec_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[ec_acc_end_tick], data_line[ec_acc_end_tick], 'bo', label='ec_acc_end', fillstyle = 'none', markeredgecolor = 'b', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[ec_deacc_start_tick], data_line[ec_deacc_start_tick], 'mo', label='ec_deacc_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[ec_deacc_end_tick], data_line[ec_deacc_end_tick], 'mo', label='ec_deacc_end', fillstyle = 'none', markeredgecolor = 'm', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[co_start_tick], data_line[co_start_tick], 'ro', label='co_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[co_end_tick], data_line[co_end_tick], 'mo', label='co_end', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[pf_tick], data_line[pf_tick], 'r^', label='pf', fillstyle = 'none', markeredgecolor = 'r', markersize = 10, markeredgewidth = 2)

    ax.plot(time_sec_tick[air_start_tick], data_line[air_start_tick], 'yo', label='air_start', markersize= 8, markeredgewidth = 0)
    ax.plot(time_sec_tick[air_end_tick], data_line[air_end_tick], 'yo', label='air_end', fillstyle = 'none', markeredgecolor = 'y', markersize = 10, markeredgewidth = 2)
    ax.set_ylabel('watts')
    #ax.legend(loc='upper left')

    Xlim = max(time_sec_tick)
    Ylim = max(data_line) * 1.3

    ax.set_xlim(0, Xlim)
    ax.set_ylim(ymax=Ylim)
    ax.grid(True)
    Ylim = Ylim - min(data_line)
    ax.text(Xlim*0.6,Ylim * 0.9 + min(data_line),'mean_power_con:{} J/s'.format(mean_power_con), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.05) + min(data_line),'time_to_pp_sec:{} sec'.format(time_to_pp_sec), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    ax.text(Xlim*0.6,Ylim * (0.9 - 0.10) + min(data_line),'mean_ec_con_power:{} J/s'.format(mean_ec_con_power), bbox=dict(facecolor='white', edgecolor='none'), fontsize=9)
    
    ax.set_xlabel('time (sec)')

    return fig