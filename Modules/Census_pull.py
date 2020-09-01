# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:11:19 2020

@author: T-rex
"""
import pandas as pd
from census import Census
from us import states
from pyzipcode import ZipCodeDatabase


def get_censusdata(key, ziplist, demo, year=2010):
    zcdb = ZipCodeDatabase()    
    cendf = pd.DataFrame(columns = ['P007001', demo, 'state', 'zip code tabulation area (or part)'])
    miszip = []
    for i in ziplist:
        try:
            getstate = 'states.' + zcdb[i].state +'.fips'
            temp = key.sf1.state_zipcode(('P007001', demo), eval(getstate),
                                         i, year=year)
            cendf = cendf.append(temp[0], ignore_index = True)
        except IndexError:
            miszip.append(i)
    
    cendf.rename(columns = {'zip code tabulation area (or part)': 'zipcode',
                            'P007001': 'Total_pop'}, inplace=True)
    
    return (cendf, miszip) 