# -*- coding: utf-8 -*-
"""
Created on Fri May  1 12:29:43 2020

@author: T-rex

Pulls in Median Home Price data by zip code from Zillow and cleans it.
"""

import os
import pandas as pd
import numpy as np

def get_median(ziplist, syear,  eyear):
    '''
    Parameters
    ----------
    ziplist : List of Integers
        Zip codes to keep
    syear : Integer start year
    eyear: Integer end year


    Returns
    -------
    A tuple with the first item being a df of the annual median home price for selected zip codes and years,
    and the second item being a list of zipcodes not present in the zillow data.

    '''
    codepath = os.path.abspath(os.path.dirname(__file__))
    zillowpath = os.path.join(codepath, "..\\Data\\Zip_Zhvi_AllHomes.csv")
    zillowdf = pd.read_csv(zillowpath)
    zillowdf['RegionName'] = zillowdf['RegionName'].astype(str)
    zillowdf['RegionName'] =  zillowdf['RegionName'].str.zfill(5)
    zillowdf.drop(index = zillowdf.index[~zillowdf['RegionName'].isin(ziplist)],
                  inplace=True)
    miszip = list(np.setdiff1d(ziplist, zillowdf['RegionName']))
    
    # Get annual median home price 
    zillowdf[str(syear)] = zillowdf.loc[:,zillowdf.columns.str.contains(str(syear))].median(axis = 1)
    zillowdf[str(eyear)] = zillowdf.loc[:,zillowdf.columns.str.contains(str(eyear))].median(axis = 1)
  
    todrop = [name for name in zillowdf.columns if name not in ([str(syear), str(eyear)] + ['RegionName'])]
    zillowdf.drop(zillowdf[todrop], axis=1, inplace=True)
    zillowdf.rename({'RegionName' : 'zipcode'}, inplace=True, axis=1)
    zillowdf['per_change'] = (zillowdf[str(eyear)] / zillowdf[str(syear)]*100).round() - 100
    zillowdf['zipcode'] = zillowdf['zipcode'].astype(str)
    return zillowdf, miszip


   