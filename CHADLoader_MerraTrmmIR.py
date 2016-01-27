
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
lonLow = -160.
lonHigh = -140.
latLow = -20.
latHigh = 0.

# Set the URL/Filepath for load files as well as the variable
# names to load
# Note: Loading bin edges is no longer necessary - they could also
# be manually specified as a numpy array and passed to ClickHist.
# This is a relic of when ClickHist needed a histogram passed to it.

# urlToLoadHist = '/path/to/your/directory'
#urlToLoad = 'http://goldsmr2.sci.gsfc.nasa.gov/dods/MAT1NXFLX'
#urlToLoad = 'http://goldsmr2.sci.gsfc.nasa.gov/opendap/MERRA/MAT1NXFLX.5.2.0/1979/01/MERRA100.prod.assim.tavg1_2d_flx_Nx.19790101.hdf'
# Temporarily using CFSR data in lieu of MERRA
#urlToLoad = 'https://weather.rsmas.miami.edu/repository/opendap/synth:eab82de2-d682-4dc0-ba8b-2fac7746d269:L0NGU1JfcjE0NHg3Ml8yNC5uYzQ=/entry.das'
urlToLoad = 'http://weather.rsmas.miami.edu/repository/opendap/synth:28309f4c-d02c-43bc-8e67-d959a3a2ee49:L01FUlJBLnByb2QuYXNzaW0udGF2ZzFfMmRfbG5kX054LjE5OTdfMjAxNF9maXhlZC5uYw==/entry.das'
# Variable names in input file(s) for bin edges and values
var1ValueName = 'precip'
var2ValueName = 'olr'

# Unit correction options
# If the units in the input file are not what is desired,
# they can be corrected during the load with these multipliers.
var1ValueMult = 86400.
var2ValueMult = 1.

# Manual Bin Definition
# Later call to create ClickHist uses the below variable names
# You should probably leave the names alone
var1Edges = np.arange(0,100.+0.01,10.)
var2Edges = np.arange(120.,320.+0.01,20.)

# Variable Names and Units
# These are optional descriptive inputs to both ClickHist and
# (some) to ClickHistDo so that the ClickHist and the output
# bundle are labeled properly
var1Name = 'Total Precipitation'
var2Name = 'Outgoing Longwave Radiation'
var1Units = 'mm day-1'
var2Units = 'W m-2'
metadata_UD = (var1ValueName+' vs '+var2ValueName+': '+
               str(lonLow)+' to '+str(lonHigh)+' E, '+
               str(latLow)+' to '+str(latHigh)+' N')

# Formatting for Output
# Basic Help: The number after the decimal point sets the number
# of decimal points shown in output
# For more on Python string formatting, see:
# (https://mkaz.github.io/2012/10/10/python-string-format/)
# These are OPTIONAL inputs to ClickHist: xFmtStr=?,yFmtStr=?)
var1FmtStr = "{:3.0f}"
var2FmtStr = "{:3.0f}"

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
startYear = 1979
startMonth = 1
startDay = 1
startHour = 0
startMinute = 0
startSecond = 0
startDatetime = datetime.datetime(startYear,startMonth,startDay,
                                  startHour,startMinute,startSecond)

# Name of bundle template - no path needed
bundleInFilename = 'ClickHist_merraTrmmIR.xidv'

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

# datetime for setting the first data point's time
import datetime

# matplotlib for graphics, set tk too
# %matplotlib osx is experimental
get_ipython().magic('matplotlib tk')
#%matplotlib osx
import matplotlib

# (Note: for debugging, replace '%' command with
# matplotlib.use)
#matplotlib.use('TkAgg')

# Modules for fixing the buffer in cell 3
from IPython.display import clear_output
import sys

# And obviously import ClickHist and ClickHistDo!
import ClickHist_IDV as ClickHist
import ClickHistDo_IDV as ClickHistDo

# User-specified imports
# Import netCDF4 to load the netCDF input file
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
cdfIn = netCDF4.Dataset(urlToLoad,'r')

# Data for ClickHistDo_IDV
lonValues = cdfIn.variables[lonValueName][:]
latValues = cdfIn.variables[latValueName][:]
timeValues = cdfIn.variables[timeValueName][:]*timeValueMult

lowLonInt,highLonInt = getIntEdges(lonValues,lonLow,lonHigh)
lowLatInt,highLatInt = getIntEdges(latValues,latLow,latHigh)

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
#var1Values = cdfIn.variables[var1ValueName][:]
#var2Values = cdfIn.variables[var2ValueName][:]
var1Values = cdfIn.variables[var1ValueName][:,lowLatInt:highLatInt+1,lowLonInt:highLonInt+1]*var1ValueMult
var2Values = cdfIn.variables[var2ValueName][:,lowLatInt:highLatInt+1,lowLonInt:highLonInt+1]*var2ValueMult

lonValues = lonValues[lowLonInt:highLonInt+1]
latValues = latValues[lowLatInt:highLatInt+1]

cdfIn.close()


# In[ ]:

# Create ClickHist using a proper call
# If you only changed variable values in cells 1 and 4 above,
# ClickHist is ready to go!

# This call is necessary to create the output console for ClickHist
# (Note: for debugging, comment out '%' command)
get_ipython().magic('qtconsole')

# Create a ClickHistDo instance
ClickHistDo1 = ClickHistDo.ClickHistDo(lonValues,latValues,
                                       timeValues,startDatetime,
                                       bundleInFilename,
                                       xVarName=var1ValueName,
                                       yVarName=var2ValueName)
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



