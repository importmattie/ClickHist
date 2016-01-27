
# coding: utf-8

# ## Clickable Histogram (ClickHist)
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

# Provide the path and filename of the data
# Obviously, the user is probably not 'niznik'
pathToData = '/Users/niznik/Desktop/GLORYS/'
filename = 'GLORYS2V3_20070101-20070105_gridS.nc4'

# Names needed to load the variables from the netCDF4 input
var1ValueName = 'vosaline'
lonValueName = 'nav_lon'
latValueName = 'nav_lat'
timeValueName = 'time_counter'
var2ValueName = latValueName

# Provide the startDatetime for ClickHistDo
import datetime
startDatetime = datetime.datetime(1991,12,4,0,0,0)

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

# Formatting for Output
# Basic Help: The number after the decimal point sets the number of
# decimal points shown in output
# For more on Python string formatting, see:
# (https://mkaz.github.io/2012/10/10/python-string-format/)
# These are OPTIONAL inputs to ClickHist: xFmtStr=?,yFmtStr=?)
var1FmtStr = "{:1.2f}"
var2FmtStr = "{:2.0f}"

# Variable Names and Units
# These are optional descriptive inputs to both ClickHist
# and (some) to ClickHistDo so that the ClickHist
# and the output bundle are labeled properly
var1Name = 'Delta Salinity'
var2Name = 'Latitude'
var1Units = 'PSU'
var2Units = 'Degrees'
metadata_UD = 'Sample Metadata'

# Unit correction options
# If the units in the input file are not what is desired,
# they can be corrected during the load with these multipliers.
var1ValueMult = 1.
var2ValueMult = 1.


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
import ClickHist_GLORYS as ClickHist
import ClickHistDo_GLORYS as ClickHistDo

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


# In[ ]:

# Load the Data
cdfIn = netCDF4.Dataset(pathToData+filename,'r')

# Data for ClickHistDo_IDV
lonValues = cdfIn.variables[lonValueName][:]
latValues = cdfIn.variables[latValueName][:]
timeValues = cdfIn.variables[timeValueName][:]

salinity = cdfIn.variables[var1ValueName][:,0,:,:]
var1Values = np.zeros(salinity.shape)
timeLen = len(timeValues)
var1Values[1:timeLen,:,:] = salinity[1:timeLen,:,:]-salinity[0:timeLen-1]

var2Values = np.zeros(var1Values.shape)
for tt in range(0,var1Values.shape[0]):
    var2Values[tt,:,:] = latValues[:,:]

cdfIn.close()
    
var1Edges = np.arange(-2.2,2.2+0.01,0.4)
var2Edges = np.arange(60.,90.+0.01,2.)


# In[ ]:

# Create ClickHist using a proper call
# If you only changed variable values in cells 1 and 4 above,
# ClickHist is ready to go!

# This call is necessary to create the output console for ClickHist
# (Note: for debugging, comment out '%' command)
get_ipython().magic(u'qtconsole')

# Create a ClickHistDo instance
ClickHistDo1 = ClickHistDo.ClickHistDo(lonValues,latValues,
                                       timeValues,startDatetime)

# Create a ClickHist instance
ClickHist1 = ClickHist.ClickHist(var1Edges,var2Edges,
                                 var1Values,var2Values,
                                 xVarName=var1Name,yVarName=var2Name,
                                 xUnits=var1Units,yUnits=var2Units,
                                 xFmtStr=var1FmtStr,
                                 yFmtStr=var2FmtStr,
                                 maxPlottedInBin=maxPlottedInBin_UD)

# Set ClickHistDo1 to be the official "action" for ClickHist
ClickHist1.setDo(ClickHistDo1)

# Show the ClickHist
ClickHist1.showPlot()


# In[ ]:



