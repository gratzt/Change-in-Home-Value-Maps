# Changing-Neighborhood-Maps
 
 This project plots national housing prices using the Zillow Home Value Index by zip code tabulation area (ZCTA), and demographic data over selected years.
 Two subplots are created. The first is a map of the selected geographic area, where the color fill depicts the change in home values from the base year
 to the end year. The second subplot is a scatter of the home prices in the base year relative to an end year, where the points are different ZCTAs. Points 
 are color coded according to the percent of the population in that ZCTA that is X% of some user specified demographic variable. 
 
 Running the 'Master File Mapping.py' script will prompt the user to select the following data:  
 a geographic area (city or user entered zip codes), their census key (if not provided in Private_key script file, see below),
 a demographic variable, a base year, and an end year.

 Output is a Matplotlib plot. 

 Currently supports cutting the housing data only by racial/ethnic groups.

Installation

 1) Download the entire project.

 2) Go to https://api.census.gov/data/key_signup.html and get a Census Bureau API key.
    Requires a name and an email.

 3) Within the Modules subfolder create a python script titled 'Private_key.py'. It should have one line see below:  
    c = 'MY CENSUS API KEY FROM STEP 2'

 4) Create the following folders within the main directory:  
    Data  
        TigerLines ZCTA

 5) Download the Zillow housing data from https://www.zillow.com/research/data/.
    Navigate to the 'Home Values' data, select the Data Type option of 'ZHVI All Homes (SFR, Condo/Co-op) Time Series($)',
    and select the Geography option of 'Zip Code'. Place the downloaded file 'Zip_Zhvi_AllHomes.csv' in the 'Data' directory.

 6) Download the 'Shapefile Zip File' from the Tiger/Lines data available at:   
    https://catalog.data.gov/dataset/tiger-line-shapefile-2015-2010-nation-u-s-2010-census-5-digit-zip-code-tabulation-area-zcta5-na.  
    Extract the contents into the 'Data/TigerLines ZCTA' directory.


Example 
 - Enter a city (e.g., Seattle) or list of zip codes separated by commas (e.g., 98101, 98102,...,98191):  
    Seattle

 - Please enter the 2 letter state abbreviation (e.g., WA):  
    WA

 - Enter your census key, or set up a private key file and start over:  
    XXXXXXXXXXXXXXXX

 - Enter a demogrphic variable:  
    White, Black, American Indian or Alaskan Native, Asian, Native Hawaiian and Other Pacific Islander, Other Race, Two or More Races, Latino:  
    White

 - Enter the beginning year to track median home prices (2009-2019):  
    2013

 - Enter the last year to track median home prices(2009-2019):   
    2018

See 'Seattle_example.png' for output.

Authors
 Trevor Gratz

License
 GNU V3

Project Status  
 Development is ongoing, but has slowed due to other demands. Next steps: streamline censuse pull, add more
 variables to census pull options, build Flask web app, add event interactions, and create new functionality for the 2020 census.