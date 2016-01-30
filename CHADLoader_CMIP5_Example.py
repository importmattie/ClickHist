
# coding: utf-8

# ## Clickable Histogram of Atmospheric Data (CHAD)
# ### *(Clickable Histogram (ClickHist) + Atmospheric Data Input)*
# 
# Author: [Matthew Niznik](http://matthewniznik.com) ([matt@matthewniznik.com](mailto:matt@matthewniznik.com))<br>
# Post-Doctoral Associate, RSMAS, University of Miami
# 
# For more information, see:<br>
# https://github.com/matthewniznik/ClickHist/wiki<br>
# http://matthewniznik.com/research-projects/clickhist<br>
# 
# (Note: iPython Notebook needs a few tweaks to work most seemlessly with ClickHist and ClickHistDo instances - those will be pointed out below as they come up.)

# In[ ]:

# User Changeable Parameters (and appropriate libraries)
import numpy as np

# Regions to be loaded from the file
# All must be defined
# lon in degE (-180 to 180)
# lat in degN (-90 to 90)
lonLow = 360.-139.
lonHigh = 360.-121.
latLow = -19.
latHigh = -11.

# Different values for plotting
lonLowPlot = 121.
lonHighPlot = 360.-61.
latLowPlot = -59.
latHighPlot = 19.

# Vertical level, if applicable
lev = 1

# Set the URL/Filepath for load files as well as the variable
# names to load
urlToLoad1 = 'http://data1.gfdl.noaa.gov:9192/opendap/CMIP5/output1/NOAA-GFDL/GFDL-CM3/historical/day/atmos/day/r1i1p1/v20110601/pr/pr_day_GFDL-CM3_historical_r1i1p1_20000101-20041231.nc'
urlToLoad2 = 'http://data1.gfdl.noaa.gov:9192/opendap/CMIP5/output1/NOAA-GFDL/GFDL-CM3/historical/day/atmos/day/r1i1p1/v20110601/hus/hus_day_GFDL-CM3_historical_r1i1p1_20000101-20041231.nc'
urlToLoad3 = 'http://data1.gfdl.noaa.gov:9192/opendap/CMIP5/output1/NOAA-GFDL/GFDL-CM3/historical/day/atmos/day/r1i1p1/v20120227/ua/ua_day_GFDL-CM3_historical_r1i1p1_20000101-20041231.nc'

# Variable names in input file(s) for bin edges and values
var1ValueName = 'ua'
var2ValueName = 'hus'
plotVarValueName = 'pr'

# Unit correction options
# If the units in the input file are not what is desired,
# they can be corrected during the load with these multipliers.
var1ValueMult = 1.
var2ValueMult = 1000.

# Manual Bin Definition
# Later call to create ClickHist uses the below variable names
# You should probably leave the names alone
var1Edges = np.arange(-21.,21.+0.01,2.)
var1Edges = np.append(var1Edges,250.)
var2Edges = np.arange(8.,16.+0.01,0.5)
var2Edges = np.append(0.,var2Edges)

# Variable Names and Units
# These are optional descriptive inputs to both ClickHist and
# (some) to ClickHistDo so that the ClickHist and the output
# bundle are labeled properly
var1Name = 'Zonal Wind at 850 hPa'
var2Name = 'Specific Humidity at 850 hPa'
var1Units = 'm s-1'
var2Units = 'g kg-1'
metadata_UD = (var1ValueName+' vs '+var2ValueName+': '+
               str(lonLow)+' to '+str(lonHigh)+' E, '+
               str(latLow)+' to '+str(latHigh)+' N')

# Formatting for Output
# Basic Help: The number after the decimal point sets the number
# of decimal points shown in output
# For more on Python string formatting, see:
# (https://mkaz.github.io/2012/10/10/python-string-format/)
# These are OPTIONAL inputs to ClickHist: xFmtStr=?,yFmtStr=?)
var1FmtStr = "{:2.1f}"
var2FmtStr = "{:2.1f}"

# Variable names in input file(s) for data needed for ClickHistDo_IDV
lonValueName = 'lon'
latValueName = 'lat'
timeValueName = 'time'

# Set appropriate multiplier if time variable is not in units
# Set appropriate offset if time math is inconsistent
# "seconds since [date]"
timeValueMult = 86400
timeValueOffset = 0

# datetime for setting the first data point's time
# More accurately, the starting point for counting
# for the time variable later on. This might be different
# from the time of the first data if timeValues[0] is not 0.
import datetime
startYear = 1860
startMonth = 1
startDay = 1
startHour = 0
startMinute = 0
startSecond = 0
startDatetime = datetime.datetime(startYear,startMonth,startDay,
                                  startHour,startMinute,startSecond)

# Figure Size and Resolution
# Set the figure x by y resolution, DPI, and the max number of points
# to appear in a given bin
# (Plotting time as well as finding an individual event prohibitive
# for very large maxPlottedInBin values)
# (These are OPTIONAL inputs to ClickHist: figX=?, figY=?,
# figDPI=?, maxPlottedInBin=?)
figureXSize = 800
figureYSize = 800
figDPI = 150
maxPlottedInBin_UD = 1000


# #### * There should be nothing to change in the following two cells. *<br>

# In[ ]:

# Setting the GUI 
# ClickHist is currently optimized for tk
# For more options see section "%matplotlib" at
# https://ipython.org/ipython-doc/3/interactive/magics.html

# matplotlib for graphics, set tk too
# %matplotlib osx is experimental
get_ipython().magic(u'matplotlib tk')
#%matplotlib osx
import matplotlib

# (Note: for debugging, replace '%' command with
# matplotlib.use)
#matplotlib.use('TkAgg')

# Modules for fixing the buffer in cell 3 
from IPython.display import clear_output
import sys

# numpy to create the sample input arrays
import numpy as np

# And obviously import ClickHist and ClickHistDo!
import ClickHist_CMIP5 as ClickHist
import ClickHistDo_CMIP5 as ClickHistDo

# User-specified imports
# netCDF4 to load the netCDF input file
import netCDF4


# In[ ]:

# Fixing the output so it isn't buffered
# See: http://stackoverflow.com/questions/29772158/make-ipython-notebook-print-in-real-time

oldsysstdout = sys.stdout
class flushfile():
    def __init__(self, f):
        self.f = f
    def __getattr__(self,name): 
        return object.__getattribute__(self.f, name)
    def write(self, x):
        self.f.write(x)
        self.f.flush()
    def flush(self):
        self.f.flush()
sys.stdout = flushfile(sys.stdout)

def getIntEdges(dim,low,high):
    lowInt = np.argmin(abs(dim-low))
    highInt = np.argmin(abs(dim-high))
    return lowInt,highInt


# #### *Changes here might be necessary to manually override the times to load *<br>

# In[ ]:

# Load the Data
cdfIn = netCDF4.Dataset(urlToLoad3,'r')

# Data for ClickHistDo_IDV
lons = cdfIn.variables[lonValueName][:]
lats = cdfIn.variables[latValueName][:]
timeValues = cdfIn.variables[timeValueName][:]*timeValueMult

lowLonInt,highLonInt = getIntEdges(lons,lonLow,lonHigh)
lowLatInt,highLatInt = getIntEdges(lats,latLow,latHigh)

# Bin Edge and Value Data
# Later call to create ClickHist uses the below variable names
# You should probably leave the names alone
#
# N.B. that CHAD expects the data to be in the Python format
# variable[times,latitudes,longitudes]. If this is not the default,
# you will have to permute the data here (or ideally process it to)
# match before loading - permutation could potentially take some
# time.
#
#var1Edges = cdfIn.variables[var1EdgeName][:]
#var2Edges = cdfIn.variables[var2EdgeName][:]
var1Values = cdfIn.variables[var1ValueName][:,lev,
                                            lowLatInt:highLatInt+1,
                                            lowLonInt:highLonInt+1]*\
                                            var1ValueMult
#var1Values = np.mean(np.mean(var1Values,2),1)
    
cdfIn.close()
cdfIn = netCDF4.Dataset(urlToLoad2,'r')

var2Values = cdfIn.variables[var2ValueName][:,lev,
                                            lowLatInt:highLatInt+1,
                                            lowLonInt:highLonInt+1]*\
                                            var2ValueMult
#var2Values = np.mean(np.mean(var2Values,2),1)

cdfIn.close()

# Use this subset for ClickHist
lonValues = lons[lowLonInt:highLonInt+1]
latValues = lats[lowLatInt:highLatInt+1]

#lonValues = [np.mean(lons[lowLonInt:highLonInt+1])]
#latValues = [np.mean(lats[lowLatInt:highLatInt+1])]


# In[ ]:

# Create ClickHist using a proper call
# If you only changed variable values in cells 1 and 4 above,
# ClickHist is ready to go!

lowLonIntPlot,highLonIntPlot = getIntEdges(lons,lonLowPlot,lonHighPlot)
lowLatIntPlot,highLatIntPlot = getIntEdges(lats,latLowPlot,latHighPlot)

# This call is necessary to create the output console for ClickHist
# (Note: for debugging, comment out '%' command)
get_ipython().magic(u'qtconsole')

# Create a ClickHistDo instance
ClickHistDo1 = ClickHistDo.ClickHistDo(lonValues,latValues,
                                       timeValues,startDatetime,
                                       urlToLoad1,plotVarValueName,
                                       lons,lats,
                                       (lowLonIntPlot,highLonIntPlot),
                                       (lowLatIntPlot,highLatIntPlot))

# Create a ClickHist instance
ClickHist1 = ClickHist.ClickHist(var1Edges,var2Edges,
                                 var1Values,var2Values,
                                 xVarName=var1Name,yVarName=var2Name,
                                 xUnits=var1Units,yUnits=var2Units,
                                 xFmtStr=var1FmtStr,
                                 yFmtStr=var2FmtStr,
                                 maxPlottedInBin=maxPlottedInBin_UD,
                                 metadata=metadata_UD)
# Set ClickHistDo1 to be the official "action" for ClickHist
ClickHist1.setDo(ClickHistDo1)

# Show the ClickHist
ClickHist1.showPlot()


# In[ ]:



