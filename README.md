# Changing-Neighborhood-Maps
 
#Description
 Plots national housing prices using the Zillow Home Value Indwx by zip code tabulation area (zcta), and demographic data over selected years. 
 
 Running the 'Master File Mapping.py' script will prompt the user to select the following data:
 a geographic area (city or user entered zip codes), their census key (if not provided in script file, see below),
 a demographic variable, a base year, and an end year.

 Output is a Matplotlib plot. 

 Currently supports cutting the housing data only by racial/ethnic groups.

Installation

 1) Download the entire project.

 2) Go to https://api.census.gov/data/key_signup.html and get a Census Bureau API key.
    Requires a name and an email.

 3) Within the Modules subfolder create a python script titled 'Private_key.py'. It should have one line see below:
      c = 'MY CENSUS API KEY FROM STEP 2'

 4) Download the Zillow housing data from https://www.zillow.com/research/data/.
    Navigate to the 'Home Values' data, select the Data Type option of  'ZHVI All Homes (SFR, Condo/Co-op) Time Series($)',
    and select the Geography option of 'Zip Code'. Place the downloaded file 'Zip_Zhvi_AllHomes.csv' in the 'Data' directory.

 5) Download the 'Shapefile Zip File' from the Tiger/Lines data available at: 
    https://catalog.data.gov/dataset/tiger-line-shapefile-2015-2010-nation-u-s-2010-census-5-digit-zip-code-tabulation-area-zcta5-na.
    Extract the contents into the 'Data\\TigerLines ZCTA' directory.


Example - For the example prompts begin with '-' and user entered responses begin with '..'

 - Enter a city (e.g., Seattle) or list of zip codes separated by commas (e.g., 98101, 98102,...,98191): 
 ..Seattle

 - Please enter the 2 letter state abbreviation (e.g., WA): 
 ..WA

 - Enter your census key, or set up a private key file and start over: 
 ..XXXXXXXXXXXXXXXX

 - Enter a demogrphic variable:
 - White, Black, American Indian or Alaskan Native, Asian, Native Hawaiian and Other Pacific Islander, Other Race, Two or More Races, Latino: 
 ..White

 - Enter the beginning year to track median home prices (2009-2019): 
 ..2013

 - Enter the last year to track median home prices(2009-2019): 
 ..2018

See 'Seattle_example.png' for output.

Authors
 Trevor Gratz

License
 GNU V3

Project Status
 Development is ongoing, but has slowed due to other demands. Next steps: streamline censuse pull, add more
 variables to census pull options, build Flask web app, add event interactions, and create new functionality for the 2020 census.