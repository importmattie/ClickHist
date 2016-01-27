
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
var1FmtStr = "{:0.3f}"
var2FmtStr = "{:0.3f}"

# Variable Names and Units
# These are optional descriptive inputs to both ClickHist
# and (some) to ClickHistDo so that the ClickHist
# and the output bundle are labeled properly
var1Name = 'Sample X'
var2Name = 'Sample Y'
var1Units = 'units'
var2Units = 'units'
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
get_ipython().magic('matplotlib tk')
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
import ClickHist

# User-specified imports
# You can put your custom imports here


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

# Create the sample data
# If you would rather load data in and not manually specify
# variable values, this cell (or a new, empty cell above this
# one) is an appropriate location

# Manual Bin Definition
# Later call to create ClickHist uses the below variable names
# You should probably leave the names alone
var1Edges = np.arange(-1.1,1.1+0.01,0.2)
var2Edges = np.arange(-1.1,1.1+0.01,0.2)

# Manual Value Definition
# Later call to create ClickHist uses the below variable names
# You should probably leave the names alone
numOfValues = 10000
#var1Values = (0.5-np.random.rand(numOfValues))*2
#var2Values = (0.5-np.random.rand(numOfValues))*2
#var1Values = np.random.normal(loc=0.,scale=0.2,size=numOfValues)
#var2Values = np.random.normal(loc=0.,scale=0.2,size=numOfValues)
#randomValues = (0.5-np.random.rand(numOfValues))*2
randomValues = np.random.normal(loc=0.0,scale=0.25,size=numOfValues)
var1Values = randomValues+np.random.normal(loc=0.0,scale=0.1,
                                           size=numOfValues)
var2Values = np.zeros(numOfValues)
for i in range(0,numOfValues):
    if(np.random.random() < 0.5):
        var2Values[i] = randomValues[i]
    else:
        var2Values[i] = -1.*randomValues[i]
    var2Values[i] = var2Values[i] + np.random.normal(loc=0.0,scale=0.1)


# In[ ]:

# Create ClickHist using a proper call
# If you only changed variable values in cells 1 and 4 above,
# ClickHist is ready to go!

# This call is necessary to create the output console for ClickHist
# (Note: for debugging, comment out '%' command)
get_ipython().magic('qtconsole')

# Create a ClickHist instance
ClickHist1 = ClickHist.ClickHist(var1Edges,var2Edges,
                                 var1Values,var2Values,
                                xVarName=var1Name,yVarName=var2Name,
                                xUnits=var1Units,yUnits=var2Units,
                                xFmtStr=var1FmtStr,
                                 yFmtStr=var2FmtStr,
                                maxPlottedInBin=maxPlottedInBin_UD)
# Show the ClickHist
ClickHist1.showPlot()


# In[ ]:



