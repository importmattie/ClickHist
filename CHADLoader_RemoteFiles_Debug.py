__author__ = 'niznik'

#--- User Changeable Parameters (and appropriate libraries) ---

#--- Figure Size and Resolution ---
#--- Set the figure x by y resolution, DPI, and the max number of points to appear in a given bin ---
#--- (Plotting time as well as finding an individual event prohibitive for very large maxPlottedInBin values)
figureXSize = 800
figureYSize = 800
figDPI = 150
maxPlottedInBin = 25

#--- Formatting for Output ---
#--- Basic Help: The number after the decimal point sets the number of decimal points shown in output ---
#--- For more on Python string formatting, see: () ---
xFmtStr = "%.2f"
yFmtStr = "%.2f"

#--- Start time is needed so that an appropriate time will be loaded upon calls to IDV ---
import datetime
startYear = 2005
startMonth = 06
startDay = 01
startDate = datetime.datetime(startYear,startMonth,startDay)

#--- Load Input from URL/Filepath ---
var1Name = 'Precipitation'
var2Name = 'W500'

urlToLoadHist = 'https://weather.rsmas.miami.edu/repository/opendap/synth:4fd8f0b4-7cc2-411a-9b61-2ef0c24c1637:L0hWX3I5MHg0NV8zXzBONVRfcHJfdGVmLm5jNA==/entry.das'

histName = 'HIST'
var1EdgeName = 'PRECBINEDGES'
var2EdgeName = 'TEEFBINEDGES'
var1BinnedName = 'PRECBINNED'
var2BinnedName = 'TEEFBINNED'

urlToLoadValues = urlToLoadHist

var1ValueName = 'PREC'
var2ValueName = 'TEEF'
var1ValueMult = 86400.
var2ValueMult = 1.

lonValueName = 'lon'
latValueName = 'lat'
timeValueName = 'time'

#--- Setting the GUI ---
#--- CHAD is currently optimized for tk ---
#--- For more options see section "%matplotlib" at ---
#--- https://ipython.org/ipython-doc/3/interactive/magics.html ---

from IPython.display import clear_output

import matplotlib
matplotlib.use('tkagg')

import netCDF4
import numpy as np

import sys

import CHAD

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

#--- Load the Data ---

#--- Histogram Data ---
cdfInHist = netCDF4.Dataset(urlToLoadHist,'r')
hist = cdfInHist.variables[histName][:]
var1Edges = cdfInHist.variables[var1EdgeName][:]
var2Edges = cdfInHist.variables[var2EdgeName][:]
var1Binned = cdfInHist.variables[var1BinnedName][:]
var2Binned = cdfInHist.variables[var2BinnedName][:]
cdfInHist.close()

#--- Value Data ---
cdfInValues = netCDF4.Dataset(urlToLoadValues,'r')
var1Values = cdfInValues.variables[var1ValueName][:]*var1ValueMult
var2Values = cdfInValues.variables[var2ValueName][:]*var2ValueMult
lonValues = cdfInValues.variables[lonValueName][:]
latValues = cdfInValues.variables[latValueName][:]
timeValues = cdfInValues.variables[timeValueName][:]
cdfInValues.close()

#--- Determine the start time ---
startHourInS = (timeValues[1]-timeValues[0])*(60./2.)
startDatetime = startDate+datetime.timedelta(0,startHourInS)

#--- Create CHAD using a proper call ---
CHAD1 = CHAD.CHAD(hist,var1Edges,var2Edges,lonValues,latValues,timeValues,
                  startDatetime,var1Values,var2Values,var1Binned,var2Binned,
                  maxPlottedInBin,figureXSize,figureYSize,figDPI,
                  xFmtStr,yFmtStr)
CHAD1.showPlot()