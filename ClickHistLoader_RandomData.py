
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

# # Let's get started
# ## (0) Imports
# ### Import the necessary modules needed for CHAD to work
# 
# *Currently supported graphics backends are Qt4Agg ('qt4') and TK ('tk')*

# In[ ]:

#%matplotlib tk
get_ipython().magic(u'matplotlib qt4')
import matplotlib
#matplotlib.use('TkAgg')
#matplotlib.use('Qt4Agg')

from IPython.display import clear_output
import numpy as np
import sys

import ClickHist

# User-specified imports
# You can put your custom imports here


# ### Fixing the output so it isn't buffered
# (*See [this link](http://stackoverflow.com/questions/29772158/make-ipython-notebook-print-in-real-time) for more info*)

# In[ ]:

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


# ## (1) Setting the data
# ### Below are some options for sample ClickHist data
# **var1Values** and **var2Values** are used later to set up ClickHist - if you change the variable names here, be sure to change them in the cell that creates ClickHist<br><br>
# If you would rather load data in and not manually specify variable values, this cell (or a new, empty cell above this one) is an appropriate location

# In[ ]:

numOfValues = 10000


# ### Data randomly distributed between -1 and 1 on both axes

# In[ ]:

var1Values = (0.5-np.random.rand(numOfValues))*2
var2Values = (0.5-np.random.rand(numOfValues))*2


# ### Data normally distributed around 0 on both axes

# In[ ]:

var1Values = np.random.normal(loc=0., scale=0.2, size=numOfValues)
var2Values = np.random.normal(loc=0., scale=0.2, size=numOfValues)


# ### Data oriented in an 'X' shape

# In[ ]:

#randomValues = (0.5-np.random.rand(numOfValues))*2
randomValues = np.random.normal(loc=0.0, scale=0.25, size=numOfValues)
var1Values = randomValues+np.random.normal(loc=0.0, scale=0.1,
                                           size=numOfValues)
var2Values = np.zeros(numOfValues)
for i in range(0, numOfValues):
    if np.random.random() < 0.5:
        var2Values[i] = randomValues[i]
    else:
        var2Values[i] = -1.*randomValues[i]
    var2Values[i] = var2Values[i] + np.random.normal(loc=0.0, scale=0.1)


# ### Now define the bins for each axis

# In[ ]:

var1Edges = np.arange(-1.1, 1.1+0.01, 0.2)
var2Edges = np.arange(-1.1, 1.1+0.01, 0.2)


# ### The following (less often edited) items are set to default values here. Change them if desired.

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

# Quantiles to plot
# If you are interested in any threshold in both X and Y,
# set it here.
# (e.g. 90th percentile and 95th percentile, input [90, 95])
quantiles = [0.01,0.1,1,5,95,99,99.9,99.99]


# # (2) Create the ClickHist Instance
# (*Note that ClickHistDo can be created before ClickHist here as well, though for the basic test none is needed*)

# ### Create the ClickHist Instance!

# In[ ]:

#%qtconsole
ClickHist1 = ClickHist.ClickHist(var1Edges,var2Edges,
                                 var1Values,var2Values,
                                 xVarName=var1Name, yVarName=var2Name,
                                 xUnits=var1Units, yUnits=var2Units,
                                 xFmtStr=var1FmtStr,
                                 yFmtStr=var2FmtStr,
                                 maxPlottedInBin=maxPlottedInBin_UD,
                                 quantiles=quantiles)
ClickHist1.showPlot()


# In[ ]:



