# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.dates as md
import numpy as np


data_path = "./data.csv"

# read csv
f = open(data_path, 'rU')

readdata = csv.reader(f)
header = next(readdata)
columns = len(header) - 1 # exclude 1 for the time ticks

print("columns:{}".format(columns))
f.close()


fig = plt.figure(figsize=[15,10])
ax = fig.add_subplot(111)
ax.set_title('Normalized CMJ')
ax.set_ylabel('N')
ax.set_xlabel('Normalized time (%)')
ax.grid(True)

time_interp = np.linspace(0, 1, 1000)
data_avg_group_1 = np.zeros_like(time_interp)
data_avg_group_2 = np.zeros_like(time_interp)

# get data from each user and plot
for i in range(1,columns+1,1):
    time_list = []
    data_list = []

    # read time / force for each record
    f = open(data_path, 'rU')
    readdata = csv.reader(f)
    header = next(readdata)
    data = list(readdata)

    for row in data:
        if row[i] != '':
            time_list += [float(row[0])]
            data_list += [float(row[i])]
    f.close()

    # normalize the timing
    t_max = max(time_list)
    #print("t_max:{}".format(t_max))
    for t in range(len(time_list)):
        time_list[t] = time_list[t] / t_max

    print("time_list:{}".format(time_list))
    print("data_list:{}".format(data_list))

    data_interp = np.interp(time_interp, time_list, data_list)


    if i <13:
    #if i%2 == 1:
        color = 'red'
        data_avg_group_1 = ( data_avg_group_1 * (i-1) + data_interp ) / i
    else:
        color = 'blue'
        data_avg_group_2 = ( data_avg_group_2 * (i-13) + data_interp ) / (i-12)

    #ax.plot(time_list, data_list, color,label='user_{}'.format(i), linewidth=1.0)
    ax.plot(time_interp*100, data_interp, color, linewidth=1.0, alpha=0.2)

ax.plot(time_interp*100, data_avg_group_1, 'red',label='Group1_avg', linewidth=5.0)
ax.plot(time_interp*100, data_avg_group_2, 'blue',label='Group2_avg', linewidth=5.0)

leg = ax.legend(loc='upper left')
leg.get_frame().set_alpha(0.5)

plt.show()









