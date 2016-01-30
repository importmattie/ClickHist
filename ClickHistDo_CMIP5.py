__author__ = 'niznik'

from mpl_toolkits.basemap import Basemap
import datetime
from matplotlib import pyplot as pltOut
from matplotlib.patches import Rectangle
import netCDF4
import numpy as np

# ClickHistDo is very much specific to the implementation of ClickHist
# As an example, here is a blank ClickHistDo that tells the user that
# it will do nothing as the "hint" provided after an initial click
# (In the IDV implementation, this message is 'save IDV bundle'
#
# The do method is where all of the scripting should occur - see
# the IDV implementation for one such example

class ClickHistDo:
    def __init__(self,lons,lats,times,startDatetime,
                 xDataValueURL,xDataValueName,
                 lonsFull,latsFull,
                 lonMinMax,latMinMax):
        """
        Initialize the ClickHistDo
        :return:
        """
        # Initialize the three relevant dimensions based on input from
        # ClickHist as well as the reference start time
        self.lons = lons
        self.lats = lats
        self.times = times
        self.lonLen = len(self.lons)
        self.latLen = len(self.lats)
        self.timeLen = len(self.times)
        self.startDatetime = startDatetime

        #self.lonEverywhere = np.zeros((self.lonsPlotLen,self.latsPlotLen))
        #self.latEverywhere = np.zeros((self.lonsPlotLen,self.latsPlotLen))

        #for ii in range(0,self.lonLen):
        #    for jj in range(0,self.latLen):
        #        self.lonEverywhere[ii,jj] = self.lons[ii]
        #        self.latEverywhere[ii,jj] = self.lats[jj]

        self.xDataURL = xDataValueURL
        self.xDataValueName = xDataValueName

        self.lonsFull = lonsFull
        self.latsFull = latsFull
        self.lonsFullLen = len(lonsFull)
        self.latsFullLen = len(latsFull)

        self.lonMinMax = lonMinMax
        self.latMinMax = latMinMax

        # Initialize the figure
        #self.fig, self.axarr = pltOut.subplots(1, 1, figsize=(2, 1), dpi=300)
        self.fig = pltOut.figure(figsize=(2, 1), dpi=300)
        margin = 0.1
        self.axarr = self.fig.add_axes([margin, margin,
                                        1.-2.*margin-0.05, 1.-2.*margin])
        self.colorbarRange = np.arange(4., 48.+1., 4.)
        img = self.axarr.contourf(self.lonsFull[self.lonMinMax[0]:
                                  self.lonMinMax[1]+1],
                                  self.latsFull[self.latMinMax[0]:
                                  self.latMinMax[1]+1],
                                  np.zeros((latMinMax[1]-latMinMax[0]+1,
                                            lonMinMax[1]-lonMinMax[0]+1)),
                                  cmap=pltOut.cm.RdYlBu_r,
                                  levels=self.colorbarRange,
                                  extend='max')
        self.axarr.tick_params(labelsize=2)

        cax = self.fig.add_axes([0.89, 0.1, 0.02, .8])
        cb = self.fig.colorbar(img, cax=cax, ticks=self.colorbarRange)
        cb.ax.tick_params(labelsize=2)
        cb.set_label('test', size=2)

        self.doObjectHint = 'display time and location'
        return

    def do(self,flatIndex,**kwargs):
        """
        Performs the desired functionality based on the input from ClickHist
        :return:
        """
        self.axarr.cla()

        inputLonIndex,inputLatIndex,inputTimeIndex = self.find3DIndices(flatIndex)
        inputLon = self.lons[inputLonIndex]
        inputLat = self.lats[inputLatIndex]
        inputDatetime = self.startDatetime+\
                        datetime.timedelta(0,int(self.times[inputTimeIndex]))

        # Inform the user of the time and location of the point
        # And if passed, the values of X and Y as well
        print(inputDatetime)
        print("{:3.0f}".format(inputLon)+' E '+"{:2.0f}".format(inputLat)+' N')
        if('xyVals' in kwargs):
            print(kwargs['xyVals'])

        cdfIn = netCDF4.Dataset(self.xDataURL, 'r')
        plotSubset = cdfIn.variables[self.xDataValueName][inputTimeIndex,
                     self.latMinMax[0]:self.latMinMax[1]+1,
                     self.lonMinMax[0]:self.lonMinMax[1]+1]*86400

        #fig,axarr = pltOut.subplots(1, 1, figsize=(2, 1), dpi=300)
        #fig.tight_layout(h_pad=0.0, w_pad=0.0, rect=(0.02, 0.02, 0.9, 0.98))

        # Basemap was buggy - implement later?
        #mapAx = Basemap(projection='cyl',
        #                llcrnrlat=self.lats[self.latMinMax[0]],
        #                urcrnrlat=self.lats[self.latMinMax[1]],
        #                llcrnrlon=self.lons[self.lonMinMax[0]],
        #                urcrnrlon=self.lons[self.lonMinMax[1]],
        #                ax=axarr)
        #xMap,yMap = mapAx(self.lonEverywhere,self.latEverywhere)
        #mapAx.contourf(xMap,yMap,
        #               np.transpose(plotSubset),
        #               levels=np.arange(4.,20.+1.,2.),
        #               extend='max')
        #mapAx.drawcoastlines(linewidth=0.25)

        self.axarr.contourf(self.lonsFull[self.lonMinMax[0]:
                            self.lonMinMax[1]+1],
                            self.latsFull[self.latMinMax[0]:
                            self.latMinMax[1]+1],
                            plotSubset,
                            cmap=pltOut.cm.RdYlBu_r,
                            levels=self.colorbarRange,
                            extend='max')
        self.axarr.add_patch(Rectangle((self.lons[0], self.lats[0]),
                                       self.lons[-1]-self.lons[0],
                                       self.lats[-1]-self.lats[0],
                                       fill=False, lw=0.5,
                                       color=(0.0, 0.9, 0.0)))
        self.axarr.plot(inputLon, inputLat, marker='o', ms=2.0,
                        color=(0.9, 0.0, 0.9))

        self.fig.canvas.draw_idle()

        self.axarr.set_title(inputDatetime,size=2)

    def find3DIndices(self,flatIndex):
        """
        Finds the index of the appropriate latitude, longitude, and time
        based on the 1D index for the flattened data. This is accomplished
        by the input data following the assumed order (when flattened, loop
        through all longitudes, then all longitudes for the next latitude, etc.
        until both all latitudes and longitudes have been seen for a time, then
        next time, etc.)
        :param flatIndex: The 1D index of the x and y data in the flattened
        arrays
        :return: (1) the index of the longitude, (2) the index of the latitude,
        (3) the index of the time
        """
        lon = flatIndex%self.lonLen
        lat = (flatIndex/self.lonLen)%self.latLen
        time = flatIndex/(self.lonLen*self.latLen)
        return lon,lat,time





