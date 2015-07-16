#! /usr/bin/env python
"""
Script to generate quicklooks for the ARM Archive for scanning radars

./generate_scanning_radar_quicklook /full/path/to/filename /out_path/
primary_measurement

if primary_measurement is absent code assumes reflectivity

"""

from matplotlib import use
use('agg')
import pyart
from matplotlib import pyplot as plt
import matplotlib
import sys
import numpy as np
from time import time
from netCDF4 import num2date, date2num
import datetime
import os

if __name__ == "__main__":
    #defaults
    sacr_range = [-40, 20]
    sapr_range = [-8, 64]

    #First parse the command line arguements
    filename = sys.argv[1]
    outdir = sys.argv[2]
    if len(sys.argv) == 4:
        primary_measurement = sys.argv[3]
    else:
        primary_measurement = 'reflectivity'

    #Read radar file
    radar = pyart.io.read(filename)
    #determine if SACR or SAPR
    if 'sacr' in filename.lower():
        radar_type = 'sacr'
    elif 'sapr' in filename.lower():
        radar_type = 'sapr'
    else:
        radar_type = 'sapr'

    if primary_measurement == 'reflectivity':
        if radar_type == 'sacr':
            pvim = sacr_range[0]
            pvmax = sacr_range[1]
        else:
            pvmin = sapr_range[0]
            pvmax = sapr_range[1]
    elif primary_measurement == 'velocity':

    #this will define the reflectivity ranges
    #Determine scanning strategy
    #Create radar display
    #Plot
    #generate file name
    #save




