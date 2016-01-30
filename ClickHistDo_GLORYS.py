__author__ = 'niznik'

import datetime

# ClickHistDo is very much specific to the implementation of ClickHist
# As an example, here is a blank ClickHistDo that tells the user that
# it will do nothing as the "hint" provided after an initial click
# (In the IDV implementation, this message is 'save IDV bundle'
#
# The do method is where all of the scripting should occur - see
# the IDV implementation for one such example

class ClickHistDo:
    def __init__(self,lons,lats,times,startDatetime):
        """
        Initialize the ClickHistDo
        :return:
        """
        # Initialize the three relevant dimensions based on input from
        # ClickHist as well as the reference start time
        self.lons = lons
        self.lats = lats
        self.times = times
        self.lonLen = len(self.lons[0,:])
        self.latLen = len(self.lats[:,0])
        self.timeLen = len(self.times)
        self.startDatetime = startDatetime

        self.doObjectHint = 'display time and location'
        return

    def do(self,flatIndex,**kwargs):
        """
        Performs the desired functionality based on the input from ClickHist
        :return:
        """

        inputLonIndex,inputLatIndex,inputTimeIndex = self.find3DIndices(flatIndex)
        inputLon = self.lons[inputLatIndex,inputLonIndex]
        inputLat = self.lats[inputLatIndex,inputLonIndex]
        inputDatetime = self.startDatetime+\
                        datetime.timedelta(0,int(self.times[inputTimeIndex]))
        #inputTime = int(calendar.timegm(inputDatetime.timetuple()))

        # Inform the user of the time and location of the point
        # And if passed, the values of X and Y as well
        print(inputDatetime)
        print("{:3.0f}".format(inputLon)+' E '+"{:2.0f}".format(inputLat)+' N')
        if('xyVals' in kwargs):
            print(kwargs['xyVals'])

        return

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
