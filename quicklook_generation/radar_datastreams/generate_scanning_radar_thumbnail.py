#! /usr/bin/env python
"""
Script to generate quicklooks for the ARM Archive for scanning radars

./generate_scanning_radar_thumbnail /full/path/to/filename /out_path/
primary_measurement

if primary_measurement is absent code assumes reflectivity

"""

from matplotlib import use
use('agg')
import pyart
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import sys
import numpy as np
from netCDF4 import num2date
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

    #this will define the reflectivity ranges

    pvmin = None
    pvmax = None

    if primary_measurement == 'reflectivity':
        if radar_type == 'sacr':
            pvim = sacr_range[0]
            pvmax = sacr_range[1]
        else:
            pvmin = sapr_range[0]
            pvmax = sapr_range[1]
    elif primary_measurement == 'velocity':
        nyq = radar.instrument_parameters['nyquist_velocity']['data']
        pvmin = -1.0*nyq
        pvmax = nyq

    #Determine scanning strategy
    #add to this

    ppi_modes = ['ppi', 'sur', 'vol']
    rhi_modes = ['rhi', 'hsrhi']
    vpt_modes = ['vert', 'vpt']
    sweep_type = 'ppi'
    print  isinstance(radar.sweep_mode['data'][0], np.ndarray)
    print  isinstance(radar.sweep_mode['data'][0], list)

    try:
        if isinstance(radar.sweep_mode['data'][0], np.ndarray):
            #Array of chars
            if ("".join(radar.sweep_mode['data'][0][0:3])).lower()\
                    in ppi_modes:
                sweep_type = 'ppi'
            elif ("".join(radar.sweep_mode['data'][0][0:3])).lower()\
                    in rhi_modes:
                sweep_type = 'rhi'
            elif("".join( radar.sweep_mode['data'][0][0:3])).lower()\
                    in vpt_modes:
                sweep_type = 'vpt'
        else:
            #strings
            if radar.sweep_mode['data'][0].lower() in ppi_modes:
                sweep_type = 'ppi'
            elif radar.sweep_mode['data'][0].lower() in rhi_modes:
                sweep_type = 'rhi'
            elif radar.sweep_mode['data'][0].lower() in vpt_modes:
                sweep_type = 'vpt'


    except:
        sweep_type = 'ppi'
    fig = plt.figure(figsize = [1,0.73])
    ax = Axes(plt.gcf(),[0,0,1,1],yticks=[],xticks=[],frame_on=False)
    #Create radar display

    radar_display = pyart.graph.RadarDisplay(radar)
    #Plot
    if sweep_type == 'ppi':
        plt.gcf().delaxes(plt.gca())
        plt.gcf().add_axes(ax)
        radar_display.plot_ppi(primary_measurement, 0,
                vmin = pvmin, vmax = pvmax,
                mask_outside=False, title_flag=False,
                axislabels_flag=False,
                colorbar_flag= False, edges=False,
                filter_transitions=True,
                 ax=ax, fig=fig, cmap = pyart.graph.cm.NWSRef)
    elif sweep_type == 'rhi':
        plt.gcf().delaxes(plt.gca())
        plt.gcf().add_axes(ax)
        radar_display.plot_rhi(primary_measurement, 0,
                vmin = pvmin, vmax = pvmax,
                mask_outside=False, title_flag=False,
                axislabels_flag=False,
                colorbar_flag= False, edges=False,
                filter_transitions=True,
                 ax=ax, fig=fig, cmap = pyart.graph.cm.NWSRef)
        plt.ylim([0,17])

    #generate file name
    dt_obj = num2date(radar.time['data'][0], radar.time['units'])
    date_string = dt_obj.strftime("%Y%m%d_%H%M%S")
    radar_name = 'testing' #change
    level = 'a1'
    ofilename = radar_name + '.' + level + '.'+ \
            date_string + '.' + primary_measurement + '.png'
    #save

    plt.savefig(os.path.join(outdir, ofilename),
            dpi=100)
    plt.close(fig)
    print(sweep_type)
    print("".join(radar.sweep_mode['data'][0][0:3]))
    del radar







