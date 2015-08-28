__author__ = 'niznik'

import datetime
from IPython.display import clear_output
from matplotlib import pylab
from matplotlib import pyplot as plt
import numpy as np
from subprocess import call
import sys
import time

class CHAD:
    def __init__(self,
                 hist,xBinEdges,yBinEdges,xDataBinned,yDataBinned,
                 lons,lats,times,startDatetime,xData,yData,
                 maxPlottedInBin,figXPixelsReq,figYPixelsReq,figDPIReq,
                 xVarName,yVarName,xUnits,yUnits,xFmtStr,yFmtStr):

        #Initialize CHAD

        #self.os = 'darwin'
        self.os = sys.platform

        #Set plot density and size parameters
        self.maxPlottedInBin = maxPlottedInBin
        self.figXPixelsReq = figXPixelsReq
        self.figYPixelsReq = figYPixelsReq
        self.figDPIReq = figDPIReq

        #Set the formatting of the axes for output
        self.xVarName = xVarName
        self.yVarName = yVarName
        self.xUnits = xUnits
        self.yUnits = yUnits
        self.xFmtStr = xFmtStr
        self.yFmtStr = yFmtStr

        #Set parameters that help place the 2D histogram locations
        self.xPixFracStart = 0.3
        self.xPixFracLen = 0.6
        self.xPixFracEnd = self.xPixFracStart+self.xPixFracLen
        self.yPixFracStart = 0.3
        self.yPixFracLen = 0.6
        self.yPixFracEnd = self.yPixFracStart+self.yPixFracLen
        self.cbLen = 0.10
        self.cbPad = 0.02

        #Set parameters that help place the 1D histogram locations
        self.yPixFracStart_1DX = 0.05
        self.yPixFracEnd_1DX = self.yPixFracStart-0.1
        self.yPixFracLen_1DX = self.yPixFracEnd_1DX-self.yPixFracStart_1DX
        self.xPixFracStart_1DY = 0.05
        self.xPixFracEnd_1DY = self.xPixFracStart-0.1
        self.xPixFracLen_1DY =self.xPixFracEnd_1DY-self.xPixFracStart_1DY

        #Create the figure and retrieve the actual DPI/pixel sizes
        self.figure = plt.figure(figsize=((self.figXPixelsReq*1.0)/self.figDPIReq,(self.figYPixelsReq*1.0)/self.figDPIReq),
                                 dpi=self.figDPIReq)
        self.figDPI = self.figure.get_dpi()
        self.figXPixels = (self.figure.get_size_inches()*self.figDPI)[0]
        self.figYPixels = (self.figure.get_size_inches()*self.figDPI)[1]

        #Add the axes for the 2D and 1D histograms
        self.axes_1DX = self.figure.add_axes([self.xPixFracStart,self.yPixFracStart_1DX,
                                               self.xPixFracLen,self.yPixFracLen_1DX])
        self.axes_1DY = self.figure.add_axes([self.xPixFracStart_1DY,self.yPixFracStart,
                                              self.xPixFracLen_1DY,self.yPixFracLen])
        self.axes_2D = self.figure.add_axes([self.xPixFracStart,self.yPixFracStart,
                                             self.xPixFracLen+self.cbLen,self.yPixFracLen])

        #Set the 2D histogram data needed for plotting
        self.hist = hist
        self.totalCounts = np.sum(self.hist)
        self.maxPower = 0
        self.minPower = int(np.log10(1./self.totalCounts))-1
        self.histTicks = np.arange(self.minPower,self.maxPower+1,1)
        self.histLog = np.log10((1.0*self.hist)/np.sum(self.hist))
        self.histLog = np.where(self.histLog < self.minPower,self.minPower,self.histLog)
        self.xBinEdges = xBinEdges
        self.yBinEdges = yBinEdges
        self.xBinNum = len(self.xBinEdges)-1
        self.yBinNum = len(self.yBinEdges)-1
        self.xBinEdgesFrac = np.arange(0.,self.xBinNum+1.,1.)/self.xBinNum
        self.yBinEdgesFrac = np.arange(0.,self.yBinNum+1.,1.)/self.yBinNum

        #Set similar parameters for the 1D histograms
        self.histX = np.sum(hist,1)
        self.histY = np.sum(hist,0)
        self.histXLog = np.log10((1.0*self.histX)/np.sum(self.histX))
        self.histXLog = np.where(self.histXLog < self.minPower,self.minPower,self.histXLog)
        self.histYLog = np.log10((1.0*self.histY)/np.sum(self.histY))
        self.histYLog = np.where(self.histYLog < self.minPower,self.minPower,self.histYLog)

        #Store the raw x and y data
        self.xData = xData
        self.yData = yData
        self.xDataBinned = xDataBinned
        self.yDataBinned = yDataBinned

        #Store the raw data axis information
        self.lons = lons
        self.lats = lats
        self.times = times
        self.startDatetime = startDatetime
        self.lonNum = len(self.lons)
        self.latNum = len(self.lats)
        self.timeNum = len(self.times)
        self.tInterval = self.times[1]-self.times[0]

        #Set up interactivity
        self.cid = self.figure.canvas.mpl_connect('button_press_event',self)
        self.clicks = 0
        self.lastClickTYX = [-1,-1,-1]
        self.lastClickDot = []
        self.lastClickLine = []

        #Call generatePlotPositions() to ???
        self.plotPositions,self.xDataFracFlat,self.yDataFracFlat,\
        self.xPosFlat,self.yPosFlat,self.tPosFlat = self.generatePlotPositions()

        #Inform the user that the plot was successfully initialized
        print 'CHAD Initialized!'
        print 'Call showPlot() to see plot.'

    #__call__() function
    #Describes what to do when the user clicks on the plot
    def __call__(self,event):
        self.clicks += 1
        if(self.lastClickTYX[0] == -1):
            clear_output()
        #xyPixMargin = 7
        xClickFrac = ((event.x)*1.0)/self.figXPixels
        yClickFrac = ((event.y)*1.0)/self.figYPixels

        if(self.xPixFracStart < xClickFrac < self.xPixFracEnd):
            if(self.yPixFracStart < yClickFrac < self.yPixFracEnd):
                xClickFracInPlot = (xClickFrac-self.xPixFracStart)/(self.xPixFracLen)
                yClickFracInPlot = (yClickFrac-self.yPixFracStart)/(self.yPixFracLen)
                xClickBin = np.searchsorted(self.xBinEdgesFrac,xClickFracInPlot)-1
                yClickBin = np.searchsorted(self.yBinEdgesFrac,yClickFracInPlot)-1

                xClickValPastBin = (xClickFracInPlot-self.xBinEdgesFrac[xClickBin])*self.xBinNum*\
                                   (self.xBinEdges[xClickBin+1]-self.xBinEdges[xClickBin])
                yClickValPastBin = (yClickFracInPlot-self.yBinEdgesFrac[yClickBin])*self.yBinNum*\
                                   (self.yBinEdges[yClickBin+1]-self.yBinEdges[yClickBin])

                xClickVal = self.xBinEdges[xClickBin]+xClickValPastBin
                yClickVal = self.yBinEdges[yClickBin]+yClickValPastBin

                closestDataTYX,locOfMinError = self.findNearestPointToClick(xClickFracInPlot,yClickFracInPlot)
                closestDataTYX = closestDataTYX[0]

                if(self.clicks > 1):
                    self.lastClickDot.remove()
                    lineToRemove = self.lastClickLine.pop()
                    lineToRemove.remove()
                self.lastClickDot = self.axes_2D.scatter(xClickFracInPlot,yClickFracInPlot,c='#ff4080',edgecolors='#000000')
                closestDataXFrac = self.xDataFracFlat[locOfMinError]
                closestDataYFrac = self.yDataFracFlat[locOfMinError]
                self.lastClickLine = self.axes_2D.plot([xClickFracInPlot,closestDataXFrac],
                                                       [yClickFracInPlot,closestDataYFrac],'-',color='#ff4080')
                plt.draw()

                if(self.lastClickTYX != closestDataTYX):
                    print('You clicked at X='+str(self.xFmtStr%xClickVal)+' Y='+str(self.yFmtStr%yClickVal))
                    print('Nearest data point is X='+str(self.xFmtStr%self.xData[closestDataTYX[0],closestDataTYX[1],
                          closestDataTYX[2]])+' Y='+str(self.yFmtStr%self.yData[closestDataTYX[0],
                          closestDataTYX[1],closestDataTYX[2]]))
                    print('(Click again to open)')
                    self.lastClickTYX = closestDataTYX
                else:
                    print 'Saving case...'
                    inputLon = self.lons[self.lastClickTYX[2]]
                    inputLat = self.lats[self.lastClickTYX[1]]
                    inputTime = int(time.mktime((self.startDatetime+datetime.timedelta(0,(self.tInterval*60.)*
                                    self.lastClickTYX[0])).timetuple()))
                    self.saveLastLocBundle(inputLon,inputLat,inputTime)
                    #self.runIDV(inputLon,inputLat,inputTime)
                    self.lastClickTYX = [-1,-1,-1]

    def showPlot(self):
        p = self.axes_2D.pcolor(self.xBinEdgesFrac,self.yBinEdgesFrac,self.histLog,
                                vmin=self.minPower,vmax=self.maxPower,cmap='Spectral_r')
        self.axes_2D.cla()

        for xAxisBin in range(0,self.xBinNum):
            for yAxisBin in range(0,self.yBinNum):
                localPlotPositions = self.plotPositions[xAxisBin][yAxisBin]
                for ee in range(0,len(localPlotPositions)):
                    xI = localPlotPositions[ee][2]
                    yI = localPlotPositions[ee][1]
                    tI = localPlotPositions[ee][0]

                    locPointValueX = self.xData[tI,yI,xI]
                    locPointValueY = self.yData[tI,yI,xI]

                    #xFracPastBinMin = ((locPointValueX-self.xBinEdges[xAxisBin])/
                    #                   (self.xBinEdges[xAxisBin+1]-self.xBinEdges[xAxisBin]))
                    #yFracPastBinMin = ((locPointValueY-self.yBinEdges[yAxisBin])/
                    #                   (self.yBinEdges[yAxisBin+1]-self.yBinEdges[yAxisBin]))

                    xFracPastBinMin = self.calcFracPastBinMin(locPointValueX,self.xBinEdges,xAxisBin)
                    yFracPastBinMin = self.calcFracPastBinMin(locPointValueY,self.yBinEdges,yAxisBin)

                    fracPlotValueX = self.xBinEdgesFrac[xAxisBin]+(xFracPastBinMin/self.xBinNum)
                    fracPlotValueY = self.yBinEdgesFrac[yAxisBin]+(yFracPastBinMin/self.yBinNum)

                    locLogCount = self.histLog[xAxisBin,yAxisBin]
                    cbPercent = (locLogCount-self.minPower)*(1.0/abs(self.minPower))
                    pointColor = pylab.cm.Spectral_r(cbPercent)
                    self.axes_2D.scatter(fracPlotValueX,fracPlotValueY,c=pointColor)

        self.axes_2D.set_xlim(self.xBinEdgesFrac[0],self.xBinEdgesFrac[-1])
        self.axes_2D.set_xticks(self.xBinEdgesFrac)
        self.axes_2D.set_xticklabels(self.xBinEdges[0:self.xBinNum],rotation=270)
        self.axes_2D.tick_params(axis='x',labelsize=6)
        self.axes_2D.set_ylim(self.yBinEdgesFrac[0],self.yBinEdgesFrac[-1])
        self.axes_2D.set_yticks(self.yBinEdgesFrac)
        self.axes_2D.set_yticklabels(self.yBinEdges[0:self.yBinNum],rotation=360)
        self.axes_2D.tick_params(axis='y',labelsize=6)

        for yy in range(0,self.yBinNum):
            self.axes_2D.axhline(y=self.yBinEdgesFrac[yy],color='#000000')
        for xx in range(0,self.xBinNum):
            self.axes_2D.axvline(x=self.xBinEdgesFrac[xx],color='#000000')

        self.axes_2D.set_title(self.xVarName+' vs '+self.yVarName,fontsize=8)
        self.axes_2D.set_xlabel(self.xVarName+' (in '+self.xUnits+')',fontsize=6)
        self.axes_2D.set_ylabel(self.yVarName+' (in '+self.yUnits+')',fontsize=6)

        cbar = plt.colorbar(p,ticks=self.histTicks,
                            fraction=(self.cbLen/(self.xPixFracLen+self.cbLen))-self.cbPad,
                            pad=self.cbPad)
        cbar.ax.tick_params(labelsize=8)

        self.axes_1DX.bar(self.xBinEdgesFrac[:-1],self.histXLog-self.minPower,width=1./self.xBinNum)
        for ii in range(0,self.xBinNum):
            cbPercent = (self.histXLog[ii]-self.minPower)*(1.0/abs(self.minPower))
            barColorsX = pylab.cm.Spectral_r(cbPercent)
            self.axes_1DX.bar(self.xBinEdgesFrac[ii],self.histXLog[ii]-self.minPower,
                              width=1./self.xBinNum,color=barColorsX)
        self.axes_1DX.xaxis.set_visible(False)
        self.axes_1DX.yaxis.set_visible(False)

        self.axes_1DY.barh(self.yBinEdgesFrac[:-1],self.histYLog-self.minPower,height=1./self.yBinNum)
        for ii in range(0,self.yBinNum):
            cbPercent = (self.histYLog[ii]-self.minPower)*(1.0/abs(self.minPower))
            barColorsY = pylab.cm.Spectral_r(cbPercent)
            self.axes_1DY.barh(self.yBinEdgesFrac[ii],self.histYLog[ii]-self.minPower,
                               height=1./self.yBinNum,color=barColorsY)
        self.axes_1DY.xaxis.set_visible(False)
        self.axes_1DY.yaxis.set_visible(False)

        plt.show()

        return

    def generatePlotPositions(self):
        plotPositions = []
        xDataFracFlat = []
        yDataFracFlat = []
        xPosFlat = []
        yPosFlat = []
        tPosFlat = []
        for v1bin in range(0,self.xBinNum):
            plotPositions.append([])
            for v2bin in range(0,self.yBinNum):
                plotPositions[v1bin].append([])
                plotPositions[v1bin][v2bin] = []
                for yy in range(0,self.latNum):
                    for xx in range(0,self.lonNum):
                        localMatches = np.intersect1d(np.where(self.xDataBinned[:,yy,xx] == v1bin),
                                                      np.where(self.yDataBinned[:,yy,xx] == v2bin))
                        numOfLocalMatches = len(localMatches)
                        if(numOfLocalMatches != 0):
                            if(numOfLocalMatches > self.maxPlottedInBin):
                                np.random.shuffle(localMatches)
                            for mm in range(0,min(numOfLocalMatches,self.maxPlottedInBin)):
                                plotPositions[v1bin][v2bin].append([localMatches[mm],yy,xx])
                                xDataTemp = self.xData[localMatches[mm],yy,xx]
                                yDataTemp = self.yData[localMatches[mm],yy,xx]
                                xDataFracTemp = (1.0*v1bin/self.xBinNum)+(self.calcFracPastBinMin(xDataTemp,self.xBinEdges,
                                                                                               v1bin)/self.xBinNum)
                                yDataFracTemp = (1.0*v2bin/self.yBinNum)+(self.calcFracPastBinMin(yDataTemp,self.yBinEdges,
                                                                                               v2bin)/self.yBinNum)
                                xDataFracFlat.append(xDataFracTemp)
                                yDataFracFlat.append(yDataFracTemp)
                                xPosFlat.append(xx)
                                yPosFlat.append(yy)
                                tPosFlat.append(localMatches[mm])

        return plotPositions,np.array(xDataFracFlat),np.array(yDataFracFlat),\
               np.array(xPosFlat),np.array(yPosFlat),np.array(tPosFlat)

    def runIDV(self,inputLon,inputLat,inputTime):
        #IDV has an offset from my expected Unix times
        timeCorrection = 2*3600
        adjTime = (inputTime+timeCorrection)*1000

        lonOffset = 5.0
        latOffset = 5.0
        timeOffsetBefore = -2*3600*1000
        timeOffsetAfter = 4*3600*1000-timeOffsetBefore

        westLon = str(inputLon-lonOffset)
        eastLon = str(inputLon+lonOffset)
        southLat = str(inputLat-latOffset)
        northLat = str(inputLat+latOffset)

        startTime = str(adjTime+timeOffsetBefore)
        endTime = str(adjTime+timeOffsetAfter)
        startOffset = str(timeOffsetBefore/(60.*1000.))
        endOffset = str(timeOffsetAfter/(60.*1000.))

        currentUnixTime = str(int(time.time()))
        basisBundleFile = './Bundles/'+'CHAD_testBundle.xidv'
        tempBundleFile = './Bundles/TempBundles/tempBundle_'+currentUnixTime+'.xidv'

        centerLonFiller = '-154.123456789'
        lonLenFiller = '10.123456789'
        minLonFiller = '-159.1851851835'
        maxLonFiller = '-149.0617283945'
        centerLatFiller = '0.135792468'
        latLenFiller = '7.592592592'
        minLatFiller = '-3.660503828'
        maxLatFiller = '3.932088764'
        startTimeFiller = '1117594837000'
        endTimeFiller = '1117616461000'
        startOffsetFiller = '-119.87654321'
        endOffsetFiller = '361.23456789'

        call('sed \'s/'+minLonFiller+'/'+westLon+'/\' '+basisBundleFile+' > '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+maxLonFiller+'/'+eastLon+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+minLatFiller+'/'+southLat+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+maxLatFiller+'/'+northLat+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+centerLonFiller+'/'+str(inputLon)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+centerLatFiller+'/'+str(inputLat)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+lonLenFiller+'/'+str(lonOffset*2)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+latLenFiller+'/'+str(latOffset*2)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+startTimeFiller+'/'+startTime+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+endTimeFiller+'/'+endTime+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+startOffsetFiller+'/'+startOffset+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+endOffsetFiller+'/'+endOffset+'/\' '+tempBundleFile,shell=True)

        call('runIDV -bundle '+tempBundleFile,shell=True)
        call('rm -i '+tempBundleFile,shell=True)
        call('rm '+tempBundleFile+'.bckp',shell=True)

        return

    def saveLastLocBundle(self,inputLon,inputLat,inputTime):
        #IDV has an offset from my expected Unix times
        timeCorrection = 2*3600
        adjTime = (inputTime+timeCorrection)*1000

        lonOffset = 5.0
        latOffset = 5.0
        timeOffsetBefore = -2*3600*1000
        timeOffsetAfter = 4*3600*1000-timeOffsetBefore

        westLon = str(inputLon-lonOffset)
        eastLon = str(inputLon+lonOffset)
        southLat = str(inputLat-latOffset)
        northLat = str(inputLat+latOffset)

        startTime = str(adjTime+timeOffsetBefore)
        endTime = str(adjTime+timeOffsetAfter)
        startOffset = str(timeOffsetBefore/(60.*1000.))
        endOffset = str(timeOffsetAfter/(60.*1000.))

        currentUnixTime = str(int(time.time()))
        basisBundleFile = './Bundles/'+'CHAD_testBundle.xidv'
        tempBundleFile = './Bundles/TempBundles/tempBundle_'+currentUnixTime+'.xidv'
        #This needs to be fixed eventually
        finalBundleFile = './Bundles/'+self.xVarName+'_'+self.yVarName+'_999_999_'+\
                          str(inputLon)+'_'+str(inputLat)+'_'+str(inputTime)+'.xidv'

        centerLonFiller = '-154.123456789'
        lonLenFiller = '10.123456789'
        minLonFiller = '-159.1851851835'
        maxLonFiller = '-149.0617283945'
        centerLatFiller = '0.135792468'
        latLenFiller = '7.592592592'
        minLatFiller = '-3.660503828'
        maxLatFiller = '3.932088764'
        startTimeFiller = '1117594837000'
        endTimeFiller = '1117616461000'
        startOffsetFiller = '-119.87654321'
        endOffsetFiller = '361.23456789'

        backupTag = ''
        if(self.os.startswith('darwin')):
            backupTag = '-i \'.bckp\''
        elif(self.os == 'linux2'):
            backupTag = '-i.bckp'

        call('sed \'s/'+minLonFiller+'/'+westLon+'/\' '+basisBundleFile+' > '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+maxLonFiller+'/'+eastLon+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+minLatFiller+'/'+southLat+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+maxLatFiller+'/'+northLat+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+centerLonFiller+'/'+str(inputLon)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+centerLatFiller+'/'+str(inputLat)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+lonLenFiller+'/'+str(lonOffset*2)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+latLenFiller+'/'+str(latOffset*2)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+startTimeFiller+'/'+startTime+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+endTimeFiller+'/'+endTime+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+startOffsetFiller+'/'+startOffset+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+endOffsetFiller+'/'+endOffset+'/\' '+tempBundleFile,shell=True)

        #Save the bundle with a recognizable filename
        call('mv '+tempBundleFile+' '+finalBundleFile,shell=True)
        call('rm '+tempBundleFile+'.bckp',shell=True)
        #call('rm -i '+tempBundleFile,shell=True)

        return

    def findNearestPointToClick(self,xClickVal,yClickVal):
        error = ((self.xDataFracFlat-xClickVal)**2+(self.yDataFracFlat-yClickVal)**2)**0.5
        minError = np.amin(error)
        locOfMinError = np.where(error == minError)[0][0]
        return [[self.tPosFlat[locOfMinError],self.yPosFlat[locOfMinError],self.xPosFlat[locOfMinError]]],locOfMinError

    def calcFracPastBinMin(self,value,binEdges,bin):
        return ((value-binEdges[bin])/(binEdges[bin+1]-binEdges[bin]))
