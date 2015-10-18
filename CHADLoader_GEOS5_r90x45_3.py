
# coding: utf-8

# Clickable Histogram (ClickHist) + Atmospheric Data Input =
# Clickable Histogram of Atmospheric Data (CHAD)
# 
# Author: Matthew Niznik (matthew.niznik9@gmail.com)<br>
# Post-Doctoral Associate, RSMAS, University of Miami
# 
# For more information, see:<br>
# https://sites.google.com/site/matthewjniznik/research/<br>
# https://sites.google.com/site/matthewjniznik/research/chad
# 
# (Note: iPython Notebook needs a few tweaks to work most seemlessly with ClickHist and ClickHistDo instances - those will be pointed out below as they come up.)

# In[1]:

#----- User Changeable Parameters (and appropriate libraries) -----

#----- Variable Names -----
#The appropriate other variables are set below based on this choice
#Options: Precip, W500, wPuP, TEEF, KEDot, HMV
var1Name = 'Precip'
var2Name = 'KEDot'

#----- Regions to be loaded from the file -----#
#----- All must be defined -----#
#----- lon in degE (0 to 360) -----#
#----- lat in degN (-90 to 90) -----#
#lonLow = 360.-170.
#lonHigh = 360.-120.
lonLow = 50.
lonHigh = 60.
latLow = -25.0
latHigh = 25.0

#----- Figure Size and Resolution -----
#Set the figure x by y resolution, DPI, and the max number of points to appear in a given bin
#(Plotting time as well as finding an individual event prohibitive for very large maxPlottedInBin values)
#(These are OPTIONAL inputs to ClickHist: figX=?, figY=?, figDPI=?, maxPlottedInBin=?)
figureXSize = 800
figureYSize = 800
figDPI = 150
maxPlottedInBin_UD = 1000

#----- Set the URL/Filepath for load files as well as the variable names to load -----
#Note: Loading bin edges is no longer necessary - they could also be manually specified as a numpy array
#and passed to ClickHist. This is a relic of when ClickHist needed a histogram passed to it.

#urlToLoadHist = '/path/to/your/directory'
#urlToLoad = 'https://weather.rsmas.miami.edu/repository/opendap/synth:4fd8f0b4-7cc2-411a-9b61-2ef0c24c1637:L0hWX3I5MHg0NV8zXzBFNU5fSE1WX0tFRE9ULm5jNA==/entry.das'
#urlToLoad = 'https://weather.rsmas.miami.edu/repository/opendap/synth:ce0cb211-ca06-42e5-997c-d9da5e791882:L2FsbFZhcnNfcjkweDQ1XzMubmM0/entry.das'
urlToLoad = 'https://weather.rsmas.miami.edu/repository/opendap/synth:eab82de2-d682-4dc0-ba8b-2fac7746d269:L2FsbFZhcnNfcjkweDQ1XzMubmM0/entry.das'

#----- Variable names in input file(s) for data needed for ClickHistDo_IDV -----
lonValueName = 'lon'
latValueName = 'lat'
timeValueName = 'time'

#----- Helpful fill-in variables that are set if only the name at top is selected -----
fmtStrOptions = {'Precip':"{:3.0f}", 'W500':"{:0.3f}", 'wPuP':"{:0.2f}",
                 'TEEF':"{:3.0f}", 'HMV':"{:2.0f}", 'KEDot':"{:3.0f}"}

valueNameOptions = {'Precip': 'PREC','W500': 'W500','wPuP': 'WPUP',
                    'TEEF': 'TEF','HMV': 'HMV','KEDot': 'KEDOT'}

import numpy as np
binOptions = {'Precip': np.array([0.,1.,11.,21.,31.,41.,51.,61.,71.,81.,91.,101.,250.]),
              'W500': np.array([-0.5,-0.135,-0.105,-0.075,-0.045,-0.015,
                                 0.015,0.045,0.075,0.105,0.135,0.165,0.5]),
              'wPuP': np.array([-0.5,-0.18,-0.14,-0.10,-0.06,-0.02,
                                 0.02,0.06,0.10,0.14,0.18,0.22,0.5]),
              'TEEF': np.array([-20.,20.,60.,100.,140.,180.,220.,
                                 260.,300.,340.,380.,420.,1000.]),
              'HMV': np.array([0.,4.,8.,12.,16.,20.,24.,28.,32.,36.,40.,44.,100.]),
              'KEDot': np.array([-1000.,-440.,-360.,-280.,-200.,-120.,-40.,
                                  40.,120.,200.,280.,360.,1000.])}

varUnitOptions = {'Precip': 'mm day-1','W500': 'm s-1','wPuP': 'm2 s-2',
                  'TEEF': 'J m kg-1 s-1','HMV': 'm2 s-2','KEDot': 'm3 s-3'}

varMultOptions = {'Precip': 86400.,'W500': 1.,'wPuP': 1.,'TEEF': 1.,'HMV': 1.,'KEDot': 1.}

#----- Set Bin Edges -----
var1Edges = binOptions[var1Name]
var2Edges = binOptions[var2Name]

#----- Formatting for Output -----
#Basic Help: The number after the decimal point sets the number of decimal points shown in output
#For more on Python string formatting, see:
#(https://mkaz.github.io/2012/10/10/python-string-format/)
#These are OPTIONAL inputs to ClickHist: xFmtStr=?,yFmtStr=?)
var1FmtStr = fmtStrOptions[var1Name]
var2FmtStr = fmtStrOptions[var2Name]

#----- Variable names in input file(s) for values -----
var1ValueName = valueNameOptions[var1Name]
var2ValueName = valueNameOptions[var2Name]

var1Units = varUnitOptions[var1Name]
var2Units = varUnitOptions[var2Name]
metadata_UD = var1Name+' vs '+var2Name+': '+str(lonLow)+' to '+str(lonHigh)+' E, '+str(latLow)+' to '+str(latHigh)+' N'

#----- Unit correction options -----
#If the units in the input file are not what is desired, they can be corrected during the load with
#these multipliers.
var1ValueMult = varMultOptions[var1Name]
var2ValueMult = varMultOptions[var2Name]


# In[2]:

#----- Setting the GUI -----
#ClickHist is currently optimized for tk
#For more options see section "%matplotlib" at
#https://ipython.org/ipython-doc/3/interactive/magics.html

#----- Matplotlib for graphics, set tk too -----
get_ipython().magic(u'matplotlib tk')
import matplotlib

#----- Modules for fixing the buffer in cell 3 -----
from IPython.display import clear_output
import sys

#----- numpy to create the sample input arrays -----
import numpy as np

#----- supress warnings from log10(0) -> handled in code -----
#----- Would rather not supress ALL warnings right now - fixed at a later date? -----
#import warnings
#warnings.filterwarnings('ignore')

#----- And obviously import ClickHist and ClickHistDo! -----
import ClickHist_IDV as ClickHist
import ClickHistDo_IDV as ClickHistDo

#----- User-specified imports -----
#Import netCDF4 to load the netCDF input file
import netCDF4


# In[3]:

#----- Fixing the output so it isn't buffered -----
#See: http://stackoverflow.com/questions/29772158/make-ipython-notebook-print-in-real-time
#Note: Nothing to edit in this cell!

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


# In[4]:

#----- Manual Bin Definition -----
#This is set above with the helpful fill-in
#But you can define your own different bounds if you'd like
#var1Edges = np.arange(0,1+0.01,0.1)
#var2Edges = np.arange(0,1+0.01,0.1)

#----- Load the Data -----
cdfIn = netCDF4.Dataset(urlToLoad,'r')

#----- Data for ClickHistDo_IDV -----
lonValues = cdfIn.variables[lonValueName][:]
latValues = cdfIn.variables[latValueName][:]
timeValues = cdfIn.variables[timeValueName][:]

lowLonInt,highLonInt = getIntEdges(lonValues,lonLow,lonHigh)
lowLatInt,highLatInt = getIntEdges(latValues,latLow,latHigh)

#----- Bin Edge and Value Data -----
#Later call to create ClickHist uses the below variable names
#You should probably leave the names alone
#var1Edges = cdfIn.variables[var1EdgeName][:]
#var2Edges = cdfIn.variables[var2EdgeName][:]
var1Values = cdfIn.variables[var1ValueName][:,lowLatInt:highLatInt+1,lowLonInt:highLonInt+1]*var1ValueMult
var2Values = cdfIn.variables[var2ValueName][:,lowLatInt:highLatInt+1,lowLonInt:highLonInt+1]*var2ValueMult

lonValues = lonValues[lowLonInt:highLonInt+1]
latValues = latValues[lowLatInt:highLatInt+1]

cdfIn.close()


# In[5]:

#----- Create ClickHist using a proper call -----
#If you only changed variable values in cells 1 and 4 above,
#ClickHist is ready to go!

#This call is necessary to create the output console for ClickHist
get_ipython().magic(u'qtconsole')

#----- Create a ClickHistDo instance -----
ClickHistDo1 = ClickHistDo.ClickHistDo(lonValues,latValues,timeValues,
                                      xVarName=var1ValueName,yVarName=var2ValueName)
#----- Create a ClickHist instance -----
ClickHist1 = ClickHist.ClickHist(var1Edges,var2Edges,var1Values,var2Values,
                                xVarName=var1Name,yVarName=var2Name,
                                xUnits=var1Units,yUnits=var2Units,
                                xFmtStr=var1FmtStr,yFmtStr=var2FmtStr,
                                maxPlottedInBin=maxPlottedInBin_UD,
                                metadata=metadata_UD)
#----- Set ClickHistDo1 to be the official "action" for ClickHist -----
ClickHist1.setDo(ClickHistDo1)

#----- Show the ClickHist -----
ClickHist1.showPlot()


# In[ ]:



