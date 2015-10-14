
# coding: utf-8

# Clickable Histogram (ClickHist)
# 
# Author: Matthew Niznik (matthew.niznik9@gmail.com)<br>
# Post-Doctoral Associate, RSMAS, University of Miami
# 
# For more information, see:<br>
# https://sites.google.com/site/matthewjniznik/research/<br>
# https://sites.google.com/site/matthewjniznik/research/clickhist
# 
# (Note: iPython Notebook needs a few tweaks to work most seemlessly with ClickHist instances - those will be pointed out below as they come up.)

# In[ ]:

#----- User Changeable Parameters (and appropriate libraries) -----

#----- Figure Size and Resolution -----
#Set the figure x by y resolution, DPI, and the max number of points to appear in a given bin
#(Plotting time as well as finding an individual event prohibitive for very large maxPlottedInBin values)
#(These are OPTIONAL inputs to ClickHist: figX=?, figY=?, figDPI=?, maxPlottedInBin=?)
figureXSize = 800
figureYSize = 800
figDPI = 150
maxPlottedInBin_UD = 1000

#----- Formatting for Output -----
#Basic Help: The number after the decimal point sets the number of decimal points shown in output
#For more on Python string formatting, see:
#(https://mkaz.github.io/2012/10/10/python-string-format/)
#These are OPTIONAL inputs to ClickHist: xFmtStr=?,yFmtStr=?)
var1FmtStr = "{:0.3f}"
var2FmtStr = "{:0.3f}"

#----- Variable Names and Units -----
#These are optional descriptive inputs to both ClickHist and (some) to ClickHistDo so that the ClickHist
#and the output bundle are labeled properly
var1Name = 'Sample X'
var2Name = 'Sample Y'
var1Units = 'units'
var2Units = 'units'
metadata_UD = 'Sample Metadata'

#----- Unit correction options -----
#If the units in the input file are not what is desired, they can be corrected during the load with
#these multipliers.
var1ValueMult = 1.
var2ValueMult = 1.


# In[ ]:

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

#----- And obviously import ClickHist! -----
import ClickHist

#----- User-specified imports -----
#You can put your custom imports here


# In[ ]:

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


# In[ ]:

#----- Create the sample data -----
#If you would rather load data in and not manually specify
#variable values, this cell (or a new, empty cell above this
#one) is an appropriate location

#----- Manual Bin Definition -----
#Later call to create ClickHist uses the below variable names
#You should probably leave the names alone
var1Edges = np.arange(0,1+0.01,0.1)
var2Edges = np.arange(0,1+0.01,0.1)

#----- Manual Value Definition -----
#Later call to create ClickHist uses the below variable names
#You should probably leave the names alone
var1Values = np.random.rand(10000)
var2Values = np.random.rand(10000)


# In[ ]:

#----- Create ClickHist using a proper call -----
#If you only changed variable values in cells 1 and 4 above,
#ClickHist is ready to go!

#This call is necessary to create the output console for ClickHist
get_ipython().magic(u'qtconsole')

#----- Create a ClickHist instance -----
ClickHist1 = ClickHist.ClickHist(var1Edges,var2Edges,var1Values,var2Values,
                                xVarName=var1Name,yVarName=var2Name,
                                xUnits=var1Units,yUnits=var2Units,
                                xFmtStr=var1FmtStr,yFmtStr=var2FmtStr,
                                maxPlottedInBin=maxPlottedInBin_UD,
                                )
#----- Show the ClickHist -----
ClickHist1.showPlot()

