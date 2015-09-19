__author__ = 'niznik'

#--- User Changeable Parameters (and appropriate libraries) ---

#--- Figure Size and Resolution ---
#--- Set the figure x by y resolution, DPI, and the max number of points to appear in a given bin ---
#--- (Plotting time as well as finding an individual event prohibitive for very large maxPlottedInBin values)
#--- (These are OPTIONAL inputs to ClickHist: figX=?, figY=?, figDPI=?, maxPlottedInBin=?)
figureXSize = 800
figureYSize = 800
figDPI = 150
maxPlottedInBin_UD = 1000

#--- Formatting for Output ---
#--- Basic Help: The number after the decimal point sets the number of decimal points shown in output ---
#--- For more on Python string formatting, see: () ---
#--- (These are OPTIONAL inputs to ClickHist: xFmtStr=?,yFmtStr=?)
var1FmtStr = "%2i"
var2FmtStr = "%4i"

#--- Set the URL/Filepath for load files as well as the variable names to load ---

#Note: Loading bin edges is no longer necessary - they could also be manually specified as a numpy array
#and passed to ClickHist. This is a relic of when ClickHist needed a histogram passed to it.
#urlToLoadHist = '/path/to/your/directory'
urlToLoadHist = 'https://weather.rsmas.miami.edu/repository/opendap/synth:4fd8f0b4-7cc2-411a-9b61-2ef0c24c1637:L0hWX3I5MHg0NV8zXzBFNU5fSE1WX0tFRE9ULm5jNA==/entry.das'
var1EdgeName = 'HMVBINEDGES'
var2EdgeName = 'KEDOTBINEDGES'

urlToLoadValues = urlToLoadHist
var1ValueName = 'HMV'
var2ValueName = 'KEDOT'
lonValueName = 'lon'
latValueName = 'lat'
timeValueName = 'time'

#--- Variable Names and Units ---
#These are optional descriptive inputs to both ClickHist and (some) to ClickHistDo so that the ClickHist
#and the output bundle are labeled properly
var1Name = 'HMV'
var2Name = 'KEDot'
var1Units = 'm2 s-2'
var2Units = 'm3 s-3'

#--- Unit correction options ---
#If the units in the input file are not what is desired, they can be corrected during the load with
#these multipliers.
var1ValueMult = 1.
var2ValueMult = 1.

#--- Setting the GUI ---
#--- CHAD is currently optimized for tk ---
#--- For more options see section "%matplotlib" at ---
#--- https://ipython.org/ipython-doc/3/interactive/magics.html ---
from IPython.display import clear_output

import matplotlib
matplotlib.use('tkagg')

import netCDF4

import sys

import ClickHist_IDV as ClickHist
import ClickHistDo_IDV as ClickHistDo

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
var1Edges = cdfInHist.variables[var1EdgeName][:]
var2Edges = cdfInHist.variables[var2EdgeName][:]
cdfInHist.close()

#--- Manual Bin Definition ---
#var1Edges = numpy.arange(0,1+0.01,0.1)
#var2Edges = numpy.arange(0,1+0.01,0.1)

#--- Value Data ---
cdfInValues = netCDF4.Dataset(urlToLoadValues,'r')
var1Values = cdfInValues.variables[var1ValueName][:]*var1ValueMult
var2Values = cdfInValues.variables[var2ValueName][:]*var2ValueMult
lonValues = cdfInValues.variables[lonValueName][:]
latValues = cdfInValues.variables[latValueName][:]
timeValues = cdfInValues.variables[timeValueName][:]
cdfInValues.close()

#--- Create CHAD using a proper call ---
ClickHistDo1 = ClickHistDo.ClickHistDo(lonValues,latValues,timeValues,
                          xVarName=var1ValueName,yVarName=var2ValueName)
ClickHist1 = ClickHist.ClickHist(var1Edges,var2Edges,var1Values,var2Values,
                    xVarName=var1ValueName,yVarName=var2ValueName,
                    xUnits=var1Units,yUnits=var2Units,
                    xFmtStr=var1FmtStr,yFmtStr=var2FmtStr,
                    maxPlottedInBin=maxPlottedInBin_UD)
ClickHist1.setDo(ClickHistDo1)
ClickHist1.showPlot()