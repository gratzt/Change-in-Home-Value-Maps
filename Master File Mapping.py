# -*- coding: utf-8 -*-
"""
Created on Mon May  4 09:26:29 2020

@author: T-rex

This file is intended to help people dig into how housing and census data are related. Currently,
it takes in 3 sources of data census data, zillow data, and Tiger/Lines shape file. These files are
merged at the zip code tabulation area(zcta). The user is allowed to pick the census varialbe 
(currently only supports race/ethnicity), the years of housing data to compare, and the geographic area
to investigate. The file produces one plot of two subplots.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from matplotlib.colors import Normalize
from matplotlib import cm
from matplotlib.cm import ScalarMappable
import math
from census import Census
from pyzipcode import ZipCodeDatabase

# Grab Modules
import sys
codepath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(codepath,'.\\Modules'))
import Census_pull as cp
import Shp_pull as sp
import Zillow_pull as zp
# Allow users to set up private key
try:
    import Private_key as pk
except Exception:
    pass

#############################################################################################
## Set up initial variables

###################
# Get Zip Codes
zcdb = ZipCodeDatabase()

ziptot = 0
while ziptot < 5:
    ziplist = input('Enter a city (e.g., Seattle) or list of zip codes separated by commas (e.g., 98101, 98102,...,98191): ')
    
    # Handle city entries different from zip code entries
    if any(i.isdigit() for i in ziplist):
        ziplist = ziplist.split(',')
        ziplist = list(map(str.strip, ziplist))
        maptitle = ''
        ziptot = len(ziplist)
        # Check entries are length 5
        if any([len(i) != 5 for i in ziplist]):
            ziptot = 0
            print('\nAt least one entry had more or less than 5 digits. Use leading zeros if need be. Please try again.')
            continue

    else:
        maptitle = ziplist
        state = input('Please enter the 2 letter state abbreviation (e.g., WA): ')
        citylist = zcdb.find_zip(city=ziplist, state = state)
        ziplist = [str(i.zip) for i in citylist]
        maptitle += ", " + state
        ziptot = len(ziplist)

    if ziptot < 5:
        print('\nFewer than 5 zip codes were selected. Please check the city name if entered, or enter more zip codes')

##########################
# Get Census Variables
c = ''
try:
    c = Census(pk.c)
except Exception:
    pass

if c == '':
    c = Census(input('Enter your census key, or set up a private key file and start over: '))

demodict = {'Total Housing Units' : 'P001001', 'Total Race' : 'P007001' , 'White' : 'P007003', 'Black' : 'P007004',
            'American Indian or Alaskan Native' : 'P007005', 'Asian' : 'P007006', 
            'Native Hawaiian and Other Pacific Islander': 'P007007', 'Other Race' : 'P007008',
            'Two or More Races' : 'P007009', 'Latino' : 'P007010'}

attempt = False
while attempt == False:
    demo = input("Enter a demogrphic variable:\n" + ', '.join(list(demodict.keys())[2:])+ ': ')
    if demo not in ', '.join(demodict.keys()):
        print('Please enter one of the provided demographic variables')
    else:
        attempt = True

################
# Get Years
syear = 0
eyear = 0

while (syear not in list(range(1996, 2020))) or (eyear not in list(range(1996, 2020))):
    
    syear = int(input('Enter the beginning year to track home prices (1996-2019): '))
    eyear = int(input('Enter the last year to track home prices(1996-2019): '))
    
    if (syear not in list(range(1996, 2020))) or (eyear not in list(range(1996, 2020))):
        print('\nPlease select years between 1996 and 2019, inclusive.')

#########################################################################################
## Get Data and Merge

# Get Shp file data
mapshp, misshpzip = sp.get_shpdata(ziplist)

# Get Census data
cendf, miscenzip = cp.get_censusdata(key = c, ziplist = ziplist, demo = demodict[demo], year = 2010)
cendf.rename(columns = {demodict[demo] : demo+ '_pop'}, inplace = True)
cendf['Per_' + demo] = cendf[demo+ '_pop'] / cendf['Total_pop']
cenvar = 'Per_' + demo

# Get Zillow data
zildf, miszilzip = zp.get_median(ziplist = ziplist, syear = syear, eyear = eyear)


# Merge Census and Zillow Data

scatterdf = pd.merge(zildf, cendf, how = 'inner', left_on = ['zipcode'], right_on = ['zipcode'])

# Merge Shape File and Merge Price Data Zillow Data
pricesshp = pd.merge(mapshp, zildf, how = 'left', left_on = 'ZCTA5CE10', right_on = 'zipcode')

print('\nThe following zip codes were missing from the housing data: ' +
      ", ".join( miszilzip))

    
############################################################################
# Plot

if (~zildf['per_change'].isnull()).sum() >= 5:
    
    fig, (axm, axt) = plt.subplots(1, 2)
    
    ################
    # Subplot 1 Map
    
    # Set colors min and max to nearest 25%
    lowbound = 25 * math.floor(pricesshp['per_change'].min()/25)
    uppbound = 25 * math.ceil(pricesshp['per_change'].max()/25)
    
    # Grab Colors for the Map 
    price_cmap = plt.cm.get_cmap('OrRd')
    sm = ScalarMappable(cmap=price_cmap, norm=plt.Normalize(lowbound, uppbound))
    # to_rgba doesn't handle missing values without encountering a RunTimeWarning
    maskcol = pricesshp['per_change'].isnull()
    pricesshp.loc[maskcol, 'per_change'] = 0
    colors =  sm.to_rgba(pricesshp['per_change'])
    pricesshp.loc[maskcol, 'per_change'] = np.nan
    
    # Plot Map
    greyplot = pricesshp[maskcol]
    p1 = pricesshp.plot( color = colors, ax = axm)
    p2 = greyplot.plot( color = '0.7', ax = axm)
    
    # Axes options
    axm.spines['top'].set_visible(False)
    axm.spines['right'].set_visible(False)
    axm.spines['bottom'].set_visible(False)
    axm.spines['left'].set_visible(False)
    axm.set_xlabel('\n' + maptitle, fontsize = 12)
    axm.tick_params(
        axis='both',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        left = False,
        labelleft=False,
        labelbottom=False) # labels along the bottom edge are off
    
    axm.set_title('Change in Home Prices From: \n {0} to {1} by Zip Code'.format(syear, eyear), fontsize = 12)
    
    # Plot Color Bar
    tickmarks = [i for i in range(lowbound, uppbound+25, 25)]
    cbar = plt.colorbar(sm, ticks = tickmarks, ax = axm, fraction = 0.04)
    cbar.ax.set_yticklabels(list(map(lambda i : ('+' if i > 0 else "") + str(i), tickmarks)))
    cbar.set_label('Percent Change', rotation=270, labelpad=25, fontsize = 12 )
    
    ###################
    # Subplot 2 Trend
    
    
    # Create trend line
    xs = scatterdf[str(syear)]
    ys = scatterdf[str(eyear)]
    minlim = pd.concat([xs, ys]).min() - 0.1*pd.concat([xs, ys]).min()
    maxlim = pd.concat([xs, ys]).max() + 0.1*pd.concat([xs, ys]).min()
    avgchange = (ys/xs).mean()
    xlineval = (np.linspace(minlim, maxlim, 10))
    ylineval = avgchange*xlineval
    
    if avgchange > 1:
        pltavchange =  '+' + str(round(avgchange*100) - 100)
    else:
        pltavchange = str(round(avgchange*100) - 100)
 
    # Plot trend line
    axt.plot(xlineval, ylineval, '--', color = 'black',
             label = '{0} Average Change:\n {1}%'.format(maptitle, pltavchange))
    
    # Add Pearsons Correlation Coef
    pr = np.corrcoef((ys/xs)[~(ys/xs).isnull()], scatterdf.loc[~(ys/xs).isnull(),cenvar])[0, 1].round(2)
    fake = axt.plot([0], [0], color = 'white', 
                    label = 'Correlation between percent {0} \n and change in price: {1}'.format(demo, pr))
    
    # Create Scatter
    # set color bar to be 1.5 times IQR
    smean =  scatterdf[cenvar].mean()
    sstd = scatterdf[cenvar].std()
    lb = round(0.05 * round( (smean - 2 * sstd)/0.05, 2), 2)
    ub = round(0.05 * round( (smean + 2 * sstd)/0.05, 2), 2)
    if lb < 0.1 : lb = 0
    if ub > 0.9 : ub = 1  
    scticks = list(np.linspace(lb, ub, 5).round(2))
    race_cmap = plt.cm.get_cmap('BuPu')
    sc = axt.scatter(xs, ys, c= scatterdf[cenvar], cmap = race_cmap, label = 'Zip Codes',
                vmin = lb, vmax = ub)
    
    # Axes options
    axt.spines['top'].set_visible(False)
    axt.spines['right'].set_visible(False)
    axt.set_aspect('equal', 'box')
    axt.set_xlabel('\n' + str(syear), fontsize=12)
    axt.set_ylabel(str(eyear), fontsize=12)
    axt.set_title('Home Prices by:\n Year, Zip Code, and Percent '+ demo)
    axt.set_ylim(minlim, maxlim)
    axt.set_xlim(minlim, maxlim)
    
    # Legend
    handles, labels = axt.get_legend_handles_labels()
    handles = [handles[0], handles[2], handles[1]]
    labels = [labels[0], labels[2], labels[1]]
    axt.legend(handles, labels,frameon = False, loc = 'lower right', fontsize = 8)
    midcolor = race_cmap(scatterdf[cenvar].median())
    axt.get_legend().legendHandles[1].set_color(midcolor)
    axt.get_legend().legendHandles[2].set_color('white')
    
    
    # Color bar
    rbar = plt.colorbar(sc, fraction = 0.04, ticks =scticks)
    labticks = list(map(lambda x: str(int(100*x)) + '%', scticks))
    if scticks[4] != 1 : labticks[4] = '> ' + labticks[4] 
    if scticks[0] != 0 : labticks[0] = '< ' + labticks[0]
        
    rbar.ax.set_yticklabels(labticks)
    rbar.set_label('Percent '+ demo, rotation=270, labelpad=25, fontsize = 12)
    
    
    ####################################
    # Overall Figure Options
    plt.subplots_adjust(wspace = 0.5)

else:
    print('Too few zip codes with housing data to plot.')