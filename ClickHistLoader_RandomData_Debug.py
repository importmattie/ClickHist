__author__ = 'niznik'

#--- User Changeable Parameters (and appropriate libraries) ---

#--- Figure Size and Resolution ---
#--- Set the figure x by y resolution, DPI, and the max number of points to appear in a given bin ---
#--- (Plotting time as well as finding an individual event prohibitive for very large maxPlottedInBin values)
#--- (These are OPTIONAL inputs to ClickHist: figX=?, figY=?, figDPI=?, maxPlottedInBin=?)
figureXSize = 800
figureYSize = 800
figDPI = 150
maxPlottedInBin_UD = 2500

#--- Formatting for Output ---
#--- Basic Help: The number after the decimal point sets the number of decimal points shown in output ---
#--- For more on Python string formatting, see: () ---
#--- (These are OPTIONAL inputs to ClickHist: xFmtStr=?,yFmtStr=?)
var1FmtStr = "%0.3f"
var2FmtStr = "%0.3f"

#--- Variable Names and Units ---
#These are optional descriptive inputs to both ClickHist and (some) to ClickHistDo so that the ClickHist
#and the output bundle are labeled properly
var1ValueName = 'Sample X'
var2ValueName = 'Sample Y'
var1Units = 'units'
var2Units = 'units'

#--- Unit correction options ---
#If the units in the input file are not what is desired, they can be corrected during the load with
#these multipliers.
var1ValueMult = 1.
var2ValueMult = 1.

import matplotlib
matplotlib.use('tkagg')

import numpy as np

import sys

import ClickHist

#--- Fixing the output so it isn't buffered ---
#--- See: http://stackoverflow.com/questions/29772158/make-ipython-notebook-print-in-real-time ---

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

#--- Create the sample data ---

#--- Manual Bin Definition ---
var1Edges = np.arange(0,1+0.01,0.1)
var2Edges = np.arange(0,1+0.01,0.1)

#--- Manual Value Definition ---
var1Values = np.random.rand(10000)
var2Values = np.random.rand(10000)

#--- Create CHAD using a proper call ---

ClickHist1 = ClickHist.ClickHist(var1Edges,var2Edges,var1Values,var2Values,
                    xVarName=var1ValueName,yVarName=var2ValueName,
                    xUnits=var1Units,yUnits=var2Units,
                    xFmtStr=var1FmtStr,yFmtStr=var2FmtStr,
                    maxPlottedInBin=maxPlottedInBin_UD)
ClickHist1.showPlot()