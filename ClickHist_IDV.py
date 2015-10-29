__author__ = 'niznik'

import ClickHistDo_Empty as ClickHistDo
from IPython.display import clear_output
import matplotlib
from matplotlib import pylab
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import sys

class ClickHist:
    def __init__(self,xBinEdges,yBinEdges,xData,yData,**kwargs):

        #Initialize ClickHist
        self.os = sys.platform
        matplotlib.rcParams['toolbar'] = 'None'

        #Set plot density and size parameters
        self.maxPlottedInBin = 1000
        self.figXPixelsReq = 800
        self.figYPixelsReq = 800
        self.figDPIReq = 150
        self.scatmarksize = int((self.figXPixelsReq+self.figYPixelsReq)/320)

        #Plot density and size parameters kwargs
        #(maxPlottedInBin, figX, figY, figDPI)
        if(kwargs.has_key('maxPlottedInBin')):
            self.maxPlottedInBin = kwargs.get('maxPlottedInBin')
        if(kwargs.has_key('figX')):
            self.figXPixelsReq = kwargs.get('figX')
        if(kwargs.has_key('figY')):
            self.figYPixelsReq = kwargs.get('figY')
        if(kwargs.has_key('figDPI')):
            self.figDPIReq = kwargs.get('figDPI')

        #Set the formatting of the axes for output
        self.xVarName = 'xVar'
        self.yVarName = 'yVar'
        self.xUnits = 'units'
        self.yUnits = 'units'
        self.xFmtStr = "{:.1f}"
        self.yFmtStr = "{:.1f}"

        #Formatting of the axes kwargs
        #(xVarName,yVarName,xUnits,yUnits,xFmtStr,yFmtStr)
        if(kwargs.has_key('xVarName')):
            self.xVarName = kwargs.get('xVarName')
        if(kwargs.has_key('yVarName')):
            self.yVarName = kwargs.get('yVarName')
        if(kwargs.has_key('xUnits')):
            self.xUnits = kwargs.get('xUnits')
        if(kwargs.has_key('yUnits')):
            self.yUnits = kwargs.get('yUnits')
        if(kwargs.has_key('xFmtStr')):
            self.xFmtStr = kwargs.get('xFmtStr')
        if(kwargs.has_key('yFmtStr')):
            self.yFmtStr = kwargs.get('yFmtStr')

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

        #Store the raw x and y data
        self.xData = xData.flatten()
        self.yData = yData.flatten()

        #Set the 2D histogram data needed for plotting
        self.xBinEdges = xBinEdges
        self.yBinEdges = yBinEdges
        self.xBinNum = len(self.xBinEdges)-1
        self.yBinNum = len(self.yBinEdges)-1
        self.xBinEdgesFrac = np.arange(0.,self.xBinNum+1.,1.)/self.xBinNum
        self.yBinEdgesFrac = np.arange(0.,self.yBinNum+1.,1.)/self.yBinNum

        #Calculate the histogram internally here, or at least if not passed as a kwarg?
        self.hist,A,B = np.histogram2d(self.xData,self.yData,[self.xBinEdges,self.yBinEdges])
        del A,B
        self.totalCounts = np.sum(self.hist)
        self.maxPower = 0
        self.minPower = int(np.log10(1./self.totalCounts))-1
        self.histTicks = np.arange(self.minPower,self.maxPower+1,1)
        self.histLog = np.log10((1.0*np.where(self.hist > 0,self.hist,0.1))/np.sum(self.hist))
        self.histLog = np.where(self.histLog < self.minPower,self.minPower,self.histLog)

        #Set similar parameters for the 1D histograms
        self.histX = np.sum(self.hist,1)
        self.histY = np.sum(self.hist,0)
        self.histXLog = np.log10((1.0*np.where(self.histX > 0,self.histX,0.1))/np.sum(self.histX))
        self.histXLog = np.where(self.histXLog < self.minPower,self.minPower,self.histXLog)
        self.histYLog = np.log10((1.0*np.where(self.histY > 0,self.histY,0.1))/np.sum(self.histY))
        self.histYLog = np.where(self.histYLog < self.minPower,self.minPower,self.histYLog)

        #Set up interactivity
        self.cid = self.figure.canvas.mpl_connect('button_press_event',self)
        self.clicksInHist2D = 0
        self.lastClickLoc = -1
        self.lastClickDot = []
        self.lastClickLine = []
        self.thinking = 0

        #Call generatePlotPositions() to ???
        self.plotPositions,self.plotPositionsFlat,\
        self.xDataFracFlat,self.yDataFracFlat,self.pointColors = self.generatePlotPositions()

        self.doObject = ClickHistDo.ClickHistDo()

        self.metadata = ''
        if(kwargs.has_key('metadata')):
            self.metadata = kwargs.get('metadata')

        #Inform the user that the plot was successfully initialized
        print 'ClickHist Initialized!'
        print 'Call showPlot() to see plot.'

    #__call__() function
    #Describes what to do when the user clicks on the plot
    def __call__(self,event):
        if(self.thinking == 0):
            self.thinking = 1
            self.clicksInHist2D += 1
            clear_output()
            print 'Thinking...'

            xClickFrac = ((event.x)*1.0)/self.figXPixels
            yClickFrac = ((event.y)*1.0)/self.figYPixels

            if((self.xPixFracStart < xClickFrac < self.xPixFracEnd) and
                   (self.yPixFracStart < yClickFrac < self.yPixFracEnd)):
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

                #Could be optimized? Reorder this so that drawing is after the point is found?
                locOfMinError = self.findNearestPointToClick(xClickFracInPlot,yClickFracInPlot)

                if(self.clicksInHist2D > 1):
                    self.lastClickDot.remove()
                    lineToRemove = self.lastClickLine.pop()
                    lineToRemove.remove()
                self.lastClickDot = self.axes_2D.scatter(xClickFracInPlot,yClickFracInPlot,s=self.scatmarksize,
                                                         c='#ff4080',edgecolors='#000000',lw=0)
                closestDataXFrac = self.xDataFracFlat[locOfMinError]
                closestDataYFrac = self.yDataFracFlat[locOfMinError]
                self.lastClickLine = self.axes_2D.plot([xClickFracInPlot,closestDataXFrac],
                                                           [yClickFracInPlot,closestDataYFrac],'-',color='#ff4080')
                plt.draw()

                closestDataX = self.convertFracToValue(self.xDataFracFlat[locOfMinError],
                                                       self.xBinEdges,self.xBinEdgesFrac)
                closestDataY = self.convertFracToValue(self.yDataFracFlat[locOfMinError],
                                                       self.yBinEdges,self.yBinEdgesFrac)

                if(self.lastClickLoc != locOfMinError):
                    #clear_output()
                    print('You clicked at X='+str(self.xFmtStr.format(xClickVal))+
                          ' Y='+str(self.yFmtStr.format(yClickVal)))
                    print('Nearest data point is X='+
                            str(self.xFmtStr.format(closestDataX))+' Y='+str(self.yFmtStr.format(closestDataY)))
                    print('(Click again to '+self.doObject.doObjectHint+')')
                    self.lastClickLoc = locOfMinError
                else:
                    #This can be edited to do just about anything!
                    clear_output()
                    xPercentile = self.findPercentile(self.xData,closestDataX)
                    yPercentile = self.findPercentile(self.yData,closestDataY)
                    self.doObject.do(self.plotPositionsFlat[locOfMinError],metadata=self.metadata,
                                     xPer=xPercentile,yPer=yPercentile,
                                     xyVals='X='+self.xFmtStr.format(closestDataX)+' '+self.xUnits+
                                            ' Y='+self.yFmtStr.format(closestDataY)+' '+self.yUnits)
                    #This should probably not be touched - it checks for whether or not to reset the closest point
                    self.lastClickLoc = locOfMinError
            elif((self.xPixFracStart < xClickFrac < self.xPixFracEnd) and
                     (self.yPixFracStart_1DX < yClickFrac < self.yPixFracEnd_1DX)):
                #currentBin ranges from 1 through self.xBinNum, so edges are currentBin-1 and currentBin
                currentBin = int(((xClickFrac-self.xPixFracStart)/self.xPixFracLen)*self.xBinNum)
                currentBinEdgeLow = self.xBinEdges[currentBin]
                currentBinEdgeHigh = self.xBinEdges[currentBin+1]
                currentBinPercent = "{:.4f}".format((10.**(self.histXLog[currentBin]))*100.)
                currentBinMem = self.histX[currentBin]
                clear_output()
                print 'X-Histogram Value:'
                print 'Bin '+str(currentBin+1)+':'
                print self.xFmtStr.format(currentBinEdgeLow)+' - '+self.xFmtStr.format(currentBinEdgeHigh)+\
                      ' '+self.xUnits
                print str(int(currentBinMem))+' counts ('+currentBinPercent+'% of all counts)'
            elif((self.xPixFracStart_1DY < xClickFrac < self.xPixFracEnd_1DY) and
                     (self.yPixFracStart < yClickFrac < self.yPixFracEnd)):
                currentBin = int(((yClickFrac-self.yPixFracStart)/self.yPixFracLen)*self.yBinNum)
                currentBinEdgeLow = self.yBinEdges[currentBin]
                currentBinEdgeHigh = self.yBinEdges[currentBin+1]
                currentBinPercent = "{:.4f}".format(((10.**(self.histYLog[currentBin]))*100.))
                currentBinMem = self.histY[currentBin]
                clear_output()
                print 'Y-Histogram Value:'
                print 'Bin '+str(currentBin+1)+':'
                print self.yFmtStr.format(currentBinEdgeLow)+' - '+self.yFmtStr.format(currentBinEdgeHigh)+\
                      ' '+self.yUnits
                print str(int(currentBinMem))+' counts ('+currentBinPercent+'% of all counts)'
            else:
                clear_output()
                print '(Non-clickable area...)'
            self.thinking = 0

    def showPlot(self):
        p = self.axes_2D.pcolor(self.xBinEdgesFrac,self.yBinEdgesFrac,np.transpose(self.histLog),
                                vmin=self.minPower,vmax=self.maxPower,cmap='Spectral_r')
        self.axes_2D.cla()

        self.axes_2D.scatter(self.xDataFracFlat,self.yDataFracFlat,s=self.scatmarksize,c=self.pointColors,lw=0)

        self.axes_2D.set_xlim(self.xBinEdgesFrac[0],self.xBinEdgesFrac[-1])
        self.axes_2D.set_xticks(self.xBinEdgesFrac)
        self.axes_2D.set_xticklabels(self.xBinEdges[0:self.xBinNum+1],rotation=270)
        self.axes_2D.tick_params(axis='x',labelsize=6)
        self.axes_2D.set_ylim(self.yBinEdgesFrac[0],self.yBinEdgesFrac[-1])
        self.axes_2D.set_yticks(self.yBinEdgesFrac)
        self.axes_2D.set_yticklabels(self.yBinEdges[0:self.yBinNum+1],rotation=360)
        self.axes_2D.tick_params(axis='y',labelsize=6)

        for yy in range(0,self.yBinNum):
            self.axes_2D.axhline(y=self.yBinEdgesFrac[yy],color='#000000')
        for xx in range(0,self.xBinNum):
            self.axes_2D.axvline(x=self.xBinEdgesFrac[xx],color='#000000')

        self.axes_2D.set_title(self.xVarName+' vs '+self.yVarName,fontsize=8)
        self.axes_2D.set_xlabel(self.xVarName+' (in '+self.xUnits+')',fontsize=6)
        self.axes_2D.set_ylabel(self.yVarName+' (in '+self.yUnits+')',fontsize=6)
        self.axes_2D.xaxis.set_label_coords(0.5,-0.43)
        self.axes_2D.yaxis.set_label_coords(-0.43,0.5)

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
            if(ii != 0):
                self.axes_1DX.axvline(x=self.xBinEdgesFrac[ii],ls='--',lw=1,color='#444444')
        self.axes_1DX.xaxis.set_visible(False)
        self.axes_1DX.yaxis.set_visible(False)

        self.axes_1DY.barh(self.yBinEdgesFrac[:-1],self.histYLog-self.minPower,height=1./self.yBinNum)
        for ii in range(0,self.yBinNum):
            cbPercent = (self.histYLog[ii]-self.minPower)*(1.0/abs(self.minPower))
            barColorsY = pylab.cm.Spectral_r(cbPercent)
            self.axes_1DY.barh(self.yBinEdgesFrac[ii],self.histYLog[ii]-self.minPower,
                               height=1./self.yBinNum,color=barColorsY)
            if(ii != 0):
                self.axes_1DY.axhline(y=self.yBinEdgesFrac[ii],ls='--',lw=1,color='#444444')
        self.axes_1DY.xaxis.set_visible(False)
        self.axes_1DY.yaxis.set_visible(False)

        self.figure.text(0.01,0.07,'ClickHist Version 0.18 (Experimental)',fontsize=4)
        self.figure.text(0.01,0.055,'Known bugs:',fontsize=4)
        self.figure.text(0.01,0.04,'Resizing window will break ClickHist',fontsize=4)
        self.figure.text(0.01,0.025,'"Thinking" message without any results',fontsize=4)
        self.figure.text(0.01,0.01,'To fix: Restart ClickHist',fontsize=4)

        plt.show()

        return

    def generatePlotPositions(self):
        print 'Calculating pos...'
        plotPositions = []
        plotPositionsFlat = []
        xDataFracFlat = []
        yDataFracFlat = []
        pointColors = []
        for v1bin in range(0,self.xBinNum):
            plotPositions.append([])
            for v2bin in range(0,self.yBinNum):
                plotPositions[v1bin].append([])
                plotPositions[v1bin][v2bin] = []
                xBinMid = (self.xBinEdges[v1bin]+self.xBinEdges[v1bin+1])/2.
                yBinMid = (self.yBinEdges[v2bin]+self.yBinEdges[v2bin+1])/2.
                xAcceptError = (self.xBinEdges[v1bin+1]-self.xBinEdges[v1bin])/2.
                yAcceptError = (self.yBinEdges[v2bin+1]-self.yBinEdges[v2bin])/2.
                localMatches = np.intersect1d(np.where(np.abs(self.xData - xBinMid) < xAcceptError),
                                              np.where(np.abs(self.yData - yBinMid) < yAcceptError))
                numOfLocalMatches = len(localMatches)
                if(numOfLocalMatches != 0):
                    if(numOfLocalMatches > self.maxPlottedInBin):
                        np.random.shuffle(localMatches)
                    for mm in range(0,min(numOfLocalMatches,self.maxPlottedInBin)):
                        plotPositions[v1bin][v2bin].append(localMatches[mm])
                        plotPositionsFlat.append(localMatches[mm])

                        xDataTemp = self.xData[localMatches[mm]]
                        yDataTemp = self.yData[localMatches[mm]]
                        xDataFracTemp = (1.0*v1bin/self.xBinNum)+(self.calcFracPastBinMin(xDataTemp,self.xBinEdges,
                                                                                       v1bin)/self.xBinNum)
                        yDataFracTemp = (1.0*v2bin/self.yBinNum)+(self.calcFracPastBinMin(yDataTemp,self.yBinEdges,
                                                                                       v2bin)/self.yBinNum)
                        xDataFracFlat.append(xDataFracTemp)
                        yDataFracFlat.append(yDataFracTemp)


                        locLogCount = self.histLog[v1bin,v2bin]
                        cbPercent = (locLogCount-self.minPower)*(1.0/abs(self.minPower))
                        pointColors.append(pylab.cm.Spectral_r(cbPercent))

        return plotPositions,plotPositionsFlat,np.array(xDataFracFlat),np.array(yDataFracFlat),np.array(pointColors)

    def findNearestPointToClick(self,xClickVal,yClickVal):
        error = ((self.xDataFracFlat-xClickVal)**2+(self.yDataFracFlat-yClickVal)**2)**0.5
        minError = np.amin(error)
        locOfMinError = np.where(error == minError)[0][0]
        return locOfMinError

    def calcFracPastBinMin(self,value,binEdges,bin):
        return ((value-binEdges[bin])/(binEdges[bin+1]-binEdges[bin]))

    def convertFracToValue(self,frac,binEdges,binEdgesFrac):
        bin = np.searchsorted(binEdgesFrac,frac)-1
        valPastBin = ((frac-binEdgesFrac[bin])/(binEdgesFrac[bin+1]-binEdgesFrac[bin]))*(binEdges[bin+1]-binEdges[bin])
        return binEdges[bin]+valPastBin

    def findPercentile(self,dataArray,point):
        return stats.percentileofscore(dataArray,point)

    def setDo(self,doObject):
        self.doObject = doObject
        return