# -*- coding: utf-8 -*-
"""
Created on Sat May  2 16:01:55 2020

@author: T-rex

This file provides a function (get_shpdata) that takes one argument (ziplist) and 
pulls in Tiger Lines Zip Code Tabulation Area(zcta) shape data. It returns a tuple of the 
shape data from the zip list and any zcta not present in the Tiger Lines Data.
"""
import os
import geopandas as gpd
import numpy as np

def get_shpdata(ziplist):
    '''

    Parameters
    ----------
    ziplist : list of zip code integers
    
    Returns
    -------
    A tuple with the first item being a geopandas dataframe of the zip codes provided and
    any the second item is any zip codes not present in the Tiger Lines Data.

    '''
    codepath = os.path.abspath(os.path.dirname(__file__))
    shpath = os.path.join(codepath, '..\\Data\\TigerLines ZCTA\\tl_2015_us_zcta510.shp')
    zipshp = gpd.read_file(shpath)
    zipshp = zipshp[zipshp['ZCTA5CE10'].isin(ziplist)]
    miszip = list(np.setdiff1d(ziplist, zipshp['ZCTA5CE10']))
    return (zipshp, miszip)
