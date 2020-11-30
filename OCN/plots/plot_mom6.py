#!/usr/bin/env python3
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import netCDF4 as nc
import numpy as np
import argparse
import glob
import os

def plot_world_map(lons, lats, data, metadata, plotpath):
    # plot generic world map
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree(central_longitude=0))
    ax.add_feature(cfeature.GSHHSFeature(scale='auto'))
    ax.set_extent([-180, 180, -90, 90])
    cmap='jet'
    cbarlabel = '%s' % (metadata['var'])
    plttitle = 'MOM6 Plot of variable %s' % (metadata['var'])
    if metadata['var'] == 'MLD_003': 
       bounds = np.array([10, 20, 30, 40, 50, 60, 80, 100, 150, 200, 250, 300, 400, 500, 1000])
       norm = mcolors.BoundaryNorm(boundaries=bounds, ncolors=256)
       cs = ax.pcolormesh(lons, lats, data,norm=norm,cmap=cmap)
    else: 
       vmin = np.nanmin(data)
       vmax = np.nanmax(data)
       cs = ax.pcolormesh(lons, lats, data,vmin=vmin,vmax=vmax,cmap=cmap)
    cb = plt.colorbar(cs, extend='both', orientation='horizontal', shrink=0.5, pad=.04)
    cb.set_label(cbarlabel, fontsize=12)
    plt.title(plttitle)
    plt.savefig(plotpath)
    plt.close('all')

def read_var(datapath, varname):
    datanc  = nc.Dataset(datapath)
    latout  = datanc.variables['geolat'][:]
    lonout  = datanc.variables['geolon'][:]
    dataout = datanc.variables[varname][0,...]
    datanc.close()
    return dataout, lonout, latout


def gen_figure(inpath, outpath, varname):
    # read the files to get the 2D array to plot
    data, lons, lats = read_var(inpath, varname)
    plotpath = outpath+'/%s.png' % (varname)
    metadata ={  'var': varname,
                }
    plot_world_map(lons, lats, data, metadata, plotpath)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--output', help="path to output directory", default="./")
    ap.add_argument('-i', '--input', help="path to input file", required=True)
    ap.add_argument('-v', '--variable', help="variable name to plot", required=True)
    MyArgs = ap.parse_args()
    gen_figure(MyArgs.input, MyArgs.output, MyArgs.variable)
