#mprof run ASC_mpl.py
#mprof plot

import time

import requests
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager
from matplotlib import collections as mc
import pandas
import numpy
import math
import ephem
from datetime import date, datetime, timedelta
import pathlib
from PIL import Image
import itertools
import sys
from sys import platform
import os
import gc
import feedparser
import re
import objgraph

##################
#memory leak
debug_mode = 0
##################

######################
# initial parameters #
######################

count=0
T0 = time.time()

#####################################
# location information
#HKO
Trig_0 = ephem.Observer()
Trig_0.lon = str(114+10/60+27.6/3600)
Trig_0.lat = str(22+18/60+7.3/3600)
#Hokoon
hokoon = ephem.Observer()
hokoon.lon = str(114+6/60+29/3600)
hokoon.lat = str(22+23/60+1/3600)

Obs = hokoon #<= set your observatory
#Obs.date = datetime.utcnow().replace(second=0,microsecond=0)
Obs.date = '2020/02/23 21:42:01' #UTC
#####################################
# plot parameters
fig = plt.figure(facecolor='#F0F0F0')
fig.subplots_adjust(0,0,1,1,0,0)

ax1 = plt.subplot()
ax1.set_facecolor('#F0F0F0')
ax1.set_aspect('equal', anchor='C')

#matplotlib.rcParams['savefig.facecolor'] = (0,0,0)

# log
def timelog(log):
    print(str(datetime.now().time().replace(microsecond=0))+'> '+log)
    
# LROC WAC basemap Shapefile
Mare    = numpy.zeros(shape=(267482,5)) 
Mare    = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','moon_mare.csv'))
Crater  = numpy.zeros(shape=(182111,5))
Crater  = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','moon_crater.csv'))
    
####################
# define functions #
####################

def moon_phase(): #ax1

    ax1.set_xlim((-180,180))
    ax1.set_ylim((-90,90))
    ax1.axis('off')
    
    timelog('drawing Moon')
    
    transform_moon_x = lambda x,y: x
    transform_moon_y = lambda x,y: y
    
    Mare_pt_lon = Mare.groupby('shapeid')['x'].apply(list)
    Mare_pt_lat = Mare.groupby('shapeid')['y'].apply(list)

    Mare_pt_list = Mare.groupby('shapeid')['x'].sum().reset_index()['shapeid']

    Mare_verts = []
    for i in Mare_pt_list:
        Mare_pt_x = list(map(transform_moon_x, Mare_pt_lon.loc[i], Mare_pt_lat.loc[i]))
        Mare_pt_y = list(map(transform_moon_y, Mare_pt_lon.loc[i], Mare_pt_lat.loc[i]))
        Mare_verts.append(list(zip(Mare_pt_x, Mare_pt_y)))

    Crater_pt_lon = Crater.groupby('shapeid')['x'].apply(list)
    Crater_pt_lat = Crater.groupby('shapeid')['y'].apply(list)

    Crater_pt_list = Crater.groupby('shapeid')['x'].sum().reset_index()['shapeid']

    Crater_verts = []
    for i in Crater_pt_list:
        Crater_pt_x = list(map(transform_moon_x, Crater_pt_lon.loc[i], Crater_pt_lat.loc[i]))
        Crater_pt_y = list(map(transform_moon_y, Crater_pt_lon.loc[i], Crater_pt_lat.loc[i]))
        Crater_verts.append(list(zip(Crater_pt_x, Crater_pt_y)))

    Mare_poly = mc.PolyCollection(Mare_verts,linewidths=0,facecolors='#696e65',zorder=3)
    Crater_poly = mc.PolyCollection(Crater_verts,linewidths=0,facecolors='#F0F0F0',alpha=0.25,zorder=4)
    ax1.add_collection(Mare_poly)
    ax1.add_collection(Crater_poly)

    plt.hlines([-90,-60,-30,0,30,60,90],-180,180,colors='c')
    plt.vlines([-180,-150,-120,-90,-60,-30,0,30,60,90,120,150,180],-90,90,colors='c')
    
moon_phase()

# plot
fig.canvas.draw() 
fig.canvas.flush_events()
#plt.savefig('moonmap.eps')

plt.show()

