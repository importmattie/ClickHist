# ClickHist takes care of the interactive, 2D visualization of the input
# data and passes on data from click events to an instance of the
# ClickHistDo class based on the user's specification at runtime.

# List of imports
# ClickHistDo_Empty is used by default - can be overridden by user input.
# clear_output is needed to reset messages sent to the user.
# pylab is needed for colorbars, plt is needed for plot visualizations, and
# rcParams is needed to disable plot toolbars.
# np is used for math.
# stats is used to determine percentiles.
# sys used to detect user platform - needed for differences in os x and
# linux sed calls.
from IPython.display import clear_output
from matplotlib import pylab, pyplot as plt, rcParams
import numpy as np
import os
from scipy import stats
from subprocess import call
import sys

__author__ = 'niznik'
__clickHistName__ = 'ClickHist'
__version__ = '1.0.0'


class ClickHist:
    def __init__(self,xBinEdges,yBinEdges,xData,yData,**kwargs):

        """
        Creates an instance of ClickHist
        :param xBinEdges: edges of the histogram on the x-axis
        :param yBinEdges: edges of the histogram on the y-axis
        :param xData: array containing all of the data on the x-axis
        :param yData: array containing all of the data on the y-axis
        :param kwargs: many options - see wiki for now
        :return: a new instance of ClickHist
        """

        # Start by determining the OS and disabling figure toolbars
        self.os = sys.platform
        rcParams['toolbar'] = 'None'

        # Make sure the tmp directory exists for mostRecentCH.png
        if not os.path.exists('./Output/'):
            call('mkdir ./Output/Tmp/', shell=True)

        if not os.path.exists('./Output/Tmp/'):
            call('mkdir ./Output/Tmp/', shell=True)

        # Set default plot density (maxPlottedInBin) and size parameters
        # (fig[X,Y]PixelsReq, figDPIReq, scatmarksize) (Req is "Requested")
        # kwargs may replace these (maxPlottedInBin, figX, figY, figDPI)
        self.maxPlottedInBin = 1000
        self.figXPixelsReq = 800
        self.figYPixelsReq = 800
        self.figDPIReq = 150
        self.scatmarksize = int((self.figXPixelsReq+self.figYPixelsReq)/320)

        if('maxPlottedInBin' in kwargs):
            self.maxPlottedInBin = kwargs['maxPlottedInBin']
        if('figX' in kwargs):
            self.figXPixelsReq = kwargs['figX']
        if('figY' in kwargs):
            self.figYPixelsReq = kwargs['figY']
        if('figDPI' in kwargs):
            self.figDPIReq = kwargs['figDPI']

        # Set the default formatting of the axes for output
        # kwargs may replace these (xVarName, yVarName, xUnits, yUnits,
        # xFmtStr, yFmtStr)
        self.xVarName = 'xVar'
        self.yVarName = 'yVar'
        self.xUnits = 'units'
        self.yUnits = 'units'
        self.xFmtStr = "{:.1f}"
        self.yFmtStr = "{:.1f}"

        if('xVarName' in kwargs):
            self.xVarName = kwargs['xVarName']
        if('yVarName' in kwargs):
            self.yVarName = kwargs['yVarName']
        if('xUnits' in kwargs):
            self.xUnits = kwargs['xUnits']
        if('yUnits' in kwargs):
            self.yUnits = kwargs['yUnits']
        if('xFmtStr' in kwargs):
            self.xFmtStr = kwargs['xFmtStr']
        if('yFmtStr' in kwargs):
            self.yFmtStr = kwargs['yFmtStr']

        # Set parameters that help place the 2D histogram locations
        # These should not change unless you want to experiment with placements
        self.xPixFracStart = 0.3
        self.xPixFracLen = 0.6
        self.xPixFracEnd = self.xPixFracStart+self.xPixFracLen
        self.yPixFracStart = 0.3
        self.yPixFracLen = 0.6
        self.yPixFracEnd = self.yPixFracStart+self.yPixFracLen
        self.cbLen = 0.10
        self.cbPad = 0.02

        # Set parameters that help place the 1D histogram locations
        # These should not change unless you want to experiment with placements
        self.yPixFracStart_1DX = 0.05
        self.yPixFracEnd_1DX = self.yPixFracStart-0.1
        self.yPixFracLen_1DX = self.yPixFracEnd_1DX-self.yPixFracStart_1DX
        self.xPixFracStart_1DY = 0.05
        self.xPixFracEnd_1DY = self.xPixFracStart-0.1
        self.xPixFracLen_1DY =self.xPixFracEnd_1DY-self.xPixFracStart_1DY

        # Create the figure and retrieve the actual DPI/pixel sizes
        # Checking here for quirks of getting a slightly smaller or bigger
        # figure than the requested size
        self.figure = plt.figure(figsize=((self.figXPixelsReq*1.0)/
                                          self.figDPIReq,
                                          (self.figYPixelsReq*1.0)/
                                          self.figDPIReq),
                                 dpi=self.figDPIReq)
        self.figDPI = self.figure.get_dpi()
        self.figXPixels = (self.figure.get_size_inches()*self.figDPI)[0]
        self.figYPixels = (self.figure.get_size_inches()*self.figDPI)[1]

        # Create the axes for the 2D and 1D histograms
        self.axes_1DX = self.figure.add_axes([self.xPixFracStart,
                                              self.yPixFracStart_1DX,
                                               self.xPixFracLen,
                                              self.yPixFracLen_1DX])
        self.axes_1DY = self.figure.add_axes([self.xPixFracStart_1DY,
                                              self.yPixFracStart,
                                              self.xPixFracLen_1DY,
                                              self.yPixFracLen])
        self.axes_2D = self.figure.add_axes([self.xPixFracStart,
                                             self.yPixFracStart,
                                             self.xPixFracLen+self.cbLen,
                                             self.yPixFracLen])

        # Store the raw x and y data into a flattened, 1D array
        self.xData = xData.flatten()
        self.yData = yData.flatten()

        # Set the 2D histogram data needed for plotting
        self.xBinEdges = xBinEdges
        self.yBinEdges = yBinEdges
        self.xBinNum = len(self.xBinEdges)-1
        self.yBinNum = len(self.yBinEdges)-1
        self.xBinEdgesFrac = np.arange(0.,self.xBinNum+1.,1.)/self.xBinNum
        self.yBinEdgesFrac = np.arange(0.,self.yBinNum+1.,1.)/self.yBinNum

        # Calculate the histogram internally here
        # (In the future: allow to be passed as a kwarg instead?)
        self.hist,A,B = np.histogram2d(self.xData,self.yData,
                                       [self.xBinEdges,self.yBinEdges])
        del A,B
        self.totalCounts = np.sum(self.hist)

        # Set a maximum and minimum power
        # Default to minimum power for instances where a 0 count would become
        # minus infinity after conversion to fractional, logarithmic histogram
        self.maxPower = 0
        self.minPower = int(np.log10(1./self.totalCounts))-1
        self.histTicks = np.arange(self.minPower,self.maxPower+1,1)
        self.histLog = np.log10((1.0*np.where(self.hist > 0,self.hist,0.1))/
                                np.sum(self.hist))
        self.histLog = np.where(self.histLog < self.minPower,
                                self.minPower,self.histLog)

        # Set similar parameters for the 1D histograms
        self.histX = np.sum(self.hist,1)
        self.histY = np.sum(self.hist,0)
        self.histXLog = np.log10((1.0*np.where(self.histX > 0,self.histX,0.1))/
                                 np.sum(self.histX))
        self.histXLog = np.where(self.histXLog < self.minPower,
                                 self.minPower,self.histXLog)
        self.histYLog = np.log10((1.0*np.where(self.histY > 0,self.histY,0.1))/
                                 np.sum(self.histY))
        self.histYLog = np.where(self.histYLog < self.minPower,
                                 self.minPower,self.histYLog)

        # Set up interactivity
        # Button press event tracks if there are clicks
        # thinking makes sure that the previous click is processed before a new
        # click is considered
        # This also tracks the dot drawn at the click, the connecting line,
        # and the location of the previous click
        self.cid = self.figure.canvas.mpl_connect('button_press_event',self)
        self.thinking = 0
        self.clicksInHist2D = 0
        self.lastClickLoc = -1
        self.lastClickDot = []
        self.lastClickLine = []

        # Call generatePlotPositions() to calculate the fractional position
        # of the x and y data in the plot as well as determine the color of
        # each scatter point (NOTE: pointColors may be replaced in a future
        # version. Also keep track of the location in the original data arrays
        # of the x and y data. This is necessary due to the design decision
        # to not plot every point (which would be time consuming and
        # pointlessly plot many points over each other).
        self.xDataFrac,self.yDataFrac,\
        self.pointColors,self.plotPos = self.generatePlotPositions()

        # Set the doObject that is used when a point is selected twice
        self.doObject = None

        # Set metadata, if any, passed by the user (default to blank)
        self.metadata = ''
        if('metadata' in kwargs):
            self.metadata = kwargs['metadata']

        # Inform the user that the plot was successfully initialized
        print('ClickHist Initialized!')
        print('Call showPlot() to see plot.')

        # end of __init__

    #__call__() function
    #Describes what to do when the user clicks on the plot
    def __call__(self,event):
        """
        Processes a user click, either returning a message about the closest
        point or, in the event that the same point was retrieved as the
        previous click, calls ClickHistDo.
        :param event: a click event sensed by the histogram plot
        :return:
        """

        # As long as we're not already processing a point when a click happens
        if(self.thinking == 0):
            # Indicate that we're processing a click, clear messages
            self.thinking = 1
            clear_output()
            print('\nThinking...')

            # Convert the click to fractional values
            xClickFrac = ((event.x)*1.0)/self.figXPixels
            yClickFrac = ((event.y)*1.0)/self.figYPixels

            # If the click was within the 2D histogram
            if((self.xPixFracStart < xClickFrac < self.xPixFracEnd) and
                (self.yPixFracStart < yClickFrac < self.yPixFracEnd)):

                # Increase the counter for clicks
                # Needed to make sure nothing is removed in the event that
                # no clicks have occurred previous to this one
                self.clicksInHist2D += 1

                # Convert the click to a fractional location WITHIN
                # the 2D histogram and determine the bin of the click
                # This will be used to convert the click location to x and
                # y values to communicate to the user
                xClickFracInPlot = (xClickFrac-self.xPixFracStart)/\
                                   (self.xPixFracLen)
                yClickFracInPlot = (yClickFrac-self.yPixFracStart)/\
                                   (self.yPixFracLen)
                xClickBin = np.searchsorted(self.xBinEdgesFrac,
                                            xClickFracInPlot)-1
                yClickBin = np.searchsorted(self.yBinEdgesFrac,
                                            yClickFracInPlot)-1
                xClickValPastBin = (xClickFracInPlot-
                                    self.xBinEdgesFrac[xClickBin])*\
                                   self.xBinNum*\
                                       (self.xBinEdges[xClickBin+1]-
                                        self.xBinEdges[xClickBin])
                yClickValPastBin = (yClickFracInPlot-
                                    self.yBinEdgesFrac[yClickBin])*\
                                   self.yBinNum*\
                                       (self.yBinEdges[yClickBin+1]-
                                        self.yBinEdges[yClickBin])
                xClickVal = self.xBinEdges[xClickBin]+xClickValPastBin
                yClickVal = self.yBinEdges[yClickBin]+yClickValPastBin

                # Find the closest point to the click
                # (Old Note: Could be optimized? Reorder this so that drawing
                # is after the point is found?)
                locOfMinError = self.findNearestPointToClick(xClickFracInPlot,
                                                             yClickFracInPlot)

                # If this wasn't the first click, remove the point and line
                # drawn last time to the closest point
                if(self.clicksInHist2D > 1):
                    self.lastClickDot.remove()
                    lineToRemove = self.lastClickLine.pop()
                    lineToRemove.remove()

                # Generate this call's click point and the line from the
                # click to that point
                self.lastClickDot = self.axes_2D.scatter(xClickFracInPlot,
                                                         yClickFracInPlot,
                                                         s=self.scatmarksize,
                                                         c='#ff4080',
                                                         edgecolors='#000000',
                                                         lw=0)
                closestDataXFrac = self.xDataFrac[locOfMinError]
                closestDataYFrac = self.yDataFrac[locOfMinError]
                self.lastClickLine = self.axes_2D.plot([xClickFracInPlot,
                                                        closestDataXFrac],
                                                        [yClickFracInPlot,
                                                         closestDataYFrac],
                                                       '-',color='#ff4080')
                # Redraw the figure with the click point and line
                plt.draw()

                # Get the actual data values for the closest scatter point
                closestDataX = self.convertFracToValue(
                    self.xDataFrac[locOfMinError],self.xBinEdges,
                    self.xBinEdgesFrac)
                closestDataY = self.convertFracToValue(
                    self.yDataFrac[locOfMinError],self.yBinEdges,
                    self.yBinEdgesFrac)

                # If this wasn't the same point as last time, just inform
                # the user of the new closest point
                if(self.lastClickLoc != locOfMinError):
                    print('You clicked at X='+
                          str(self.xFmtStr.format(xClickVal))+
                          ' Y='+str(self.yFmtStr.format(yClickVal)))
                    print('Nearest data point is X='+
                            str(self.xFmtStr.format(closestDataX))+
                          ' Y='+str(self.yFmtStr.format(closestDataY)))
                    if self.doObject is None:
                        print('(Click again to do nothing - '+
                              'no doObject currently set...)')
                    else:
                        print('(Click again to ' +
                              self.doObject.doObjectHint+')')
                    self.lastClickLoc = locOfMinError
                # Otherwise, do anything necessary to generate the input
                # for ClickHistDo and then call it.
                else:
                    clear_output()
                    plt.savefig('./Output/Tmp/mostRecentCH.png')
                    if self.doObject is None:
                        print('(Doing nothing - no doObject set...)')
                    else:
                        xPercentile = self.findPercentile(self.xData,
                                                          closestDataX)
                        yPercentile = self.findPercentile(self.yData,
                                                          closestDataY)
                        # This can be edited to do just about anything!
                        # --- USER EDIT FOR CLICKHISTDO ---
                        self.doObject.do(self.plotPos[locOfMinError],
                                         yVals=('X='+
                                                self.xFmtStr.format(
                                                    closestDataX) +
                                                ' '+self.xUnits +
                                                ' Y=' +
                                                self.yFmtStr.format(
                                                    closestDataY) +
                                                ' '+self.yUnits))
                        # --- END USER EDIT FOR CLICKHISTDO ---

                    # This should probably not be touched - it checks for
                    # whether or not to reset the closest point
                    self.lastClickLoc = locOfMinError
            # Now for the case that the user clicked in the x-axis 1D hist
            elif((self.xPixFracStart < xClickFrac < self.xPixFracEnd) and
                     (self.yPixFracStart_1DX < yClickFrac <
                          self.yPixFracEnd_1DX)):
                # currentBin ranges from 1 through self.xBinNum,
                # so edges are currentBin-1 and currentBin
                currentBin = int(((xClickFrac-self.xPixFracStart)/
                                  self.xPixFracLen)*self.xBinNum)
                currentBinEdgeLow = self.xBinEdges[currentBin]
                currentBinEdgeHigh = self.xBinEdges[currentBin+1]
                currentBinPercent = "{:.4f}".format((10.**(self.histXLog[
                                                               currentBin]))
                                                    *100.)
                currentBinMem = self.histX[currentBin]
                clear_output()
                print('X-Histogram Value:')
                print('Bin '+str(currentBin+1)+':')
                print(self.xFmtStr.format(currentBinEdgeLow)+' - '+
                      self.xFmtStr.format(currentBinEdgeHigh)+' '+self.xUnits)
                print(str(int(currentBinMem))+' counts ('+
                      currentBinPercent+'% of all counts)')
            # Same as above, but for y-axis 1D hist
            # (NOTE: Worth changing in a future version to make this a simple
            # method perhaps)
            elif((self.xPixFracStart_1DY < xClickFrac < self.xPixFracEnd_1DY)
                 and (self.yPixFracStart < yClickFrac < self.yPixFracEnd)):
                # currentBin ranges from 1 through self.xBinNum,
                # so edges are currentBin-1 and currentBin
                currentBin = int(((yClickFrac-self.yPixFracStart)/
                                  self.yPixFracLen)*self.yBinNum)
                currentBinEdgeLow = self.yBinEdges[currentBin]
                currentBinEdgeHigh = self.yBinEdges[currentBin+1]
                currentBinPercent = "{:.4f}".format(((10.**(self.histYLog[
                                                                currentBin]))
                                                     *100.))
                currentBinMem = self.histY[currentBin]
                clear_output()
                print('Y-Histogram Value:')
                print('Bin '+str(currentBin+1)+':')
                print(self.yFmtStr.format(currentBinEdgeLow)+' - '
                      +self.yFmtStr.format(currentBinEdgeHigh)+' '+self.yUnits)
                print(str(int(currentBinMem))+' counts ('
                      +currentBinPercent+'% of all counts)')
            # Otherwise, the user didn't click anywhere that has functionality
            # currently implemented. Just inform them of this.
            else:
                clear_output()
                print('(Non-clickable area...)')
            # Allow for future clicks to be processed since we're done.
            self.thinking = 0

    def showPlot(self):
        """
        Displays the plot once all the prep work is finished.
        :return:
        """
        # Starting out with a 'dummy' call to pcolor just to set the colorbar
        # for later
        p = self.axes_2D.pcolor(self.xBinEdgesFrac, self.yBinEdgesFrac,
                                np.transpose(self.histLog),
                                vmin=self.minPower, vmax=self.maxPower,
                                cmap='Spectral_r')
        self.axes_2D.cla()

        # Scatter all of the points, previously filtered so that plot density
        # is as desired
        self.axes_2D.scatter(self.xDataFrac,self.yDataFrac,
                             s=self.scatmarksize,c=self.pointColors,lw=0)
        # Deal with x-axis labeling
        self.axes_2D.set_xlim(self.xBinEdgesFrac[0],self.xBinEdgesFrac[-1])
        self.axes_2D.set_xticks(self.xBinEdgesFrac)
        self.axes_2D.set_xticklabels(self.xBinEdges[0:self.xBinNum+1],
                                     rotation=270)
        self.axes_2D.tick_params(axis='x',labelsize=6)
        # Deal with y-axis labeling
        self.axes_2D.set_ylim(self.yBinEdgesFrac[0],self.yBinEdgesFrac[-1])
        self.axes_2D.set_yticks(self.yBinEdgesFrac)
        self.axes_2D.set_yticklabels(self.yBinEdges[0:self.yBinNum+1],
                                     rotation=360)
        self.axes_2D.tick_params(axis='y',labelsize=6)

        # Draw the bin separation lines for the 2D histogram
        for yy in range(0,self.yBinNum):
            self.axes_2D.axhline(y=self.yBinEdgesFrac[yy],color='#000000')
        for xx in range(0,self.xBinNum):
            self.axes_2D.axvline(x=self.xBinEdgesFrac[xx],color='#000000')

        # Set other aesthetics for the plot
        self.axes_2D.set_title(self.xVarName+' vs '+self.yVarName,
                               fontsize=8)
        self.axes_2D.set_xlabel(self.xVarName+' (in '+self.xUnits+')',
                                fontsize=6)
        self.axes_2D.set_ylabel(self.yVarName+' (in '+self.yUnits+')',
                                fontsize=6)
        self.axes_2D.xaxis.set_label_coords(0.5,-0.43)
        self.axes_2D.yaxis.set_label_coords(-0.43,0.5)

        # Create the colorbar
        cbar = plt.colorbar(p,ticks=self.histTicks,
                            fraction=((self.cbLen /
                                      (self.xPixFracLen+self.cbLen)) -
                                      self.cbPad),
                            pad=self.cbPad)
        cbar.ax.tick_params(labelsize=8)

        # Draw the x-axis 1D histogram, first to set the axes, and then again
        # to draw each bar with the proper color
        self.axes_1DX.bar(self.xBinEdgesFrac[:-1],self.histXLog-self.minPower,
                          width=1./self.xBinNum)
        for ii in range(0,self.xBinNum):
            cbPercent = (self.histXLog[ii]-self.minPower)*\
                        (1.0/abs(self.minPower))
            barColorsX = pylab.cm.Spectral_r(cbPercent)
            self.axes_1DX.bar(self.xBinEdgesFrac[ii],self.histXLog[ii]-
                              self.minPower,width=1./self.xBinNum,
                              color=barColorsX)
            if(ii != 0):
                self.axes_1DX.axvline(x=self.xBinEdgesFrac[ii],
                                      ls='--',lw=1,color='#444444')
        self.axes_1DX.xaxis.set_visible(False)
        self.axes_1DX.yaxis.set_visible(False)

        # Draw the y-axis 1D histogram, first to set the axes, and then again
        # to draw each bar with the proper color
        self.axes_1DY.barh(self.yBinEdgesFrac[:-1],self.histYLog-
                           self.minPower,height=1./self.yBinNum)
        for ii in range(0,self.yBinNum):
            cbPercent = (self.histYLog[ii]-self.minPower)*\
                        (1.0/abs(self.minPower))
            barColorsY = pylab.cm.Spectral_r(cbPercent)
            self.axes_1DY.barh(self.yBinEdgesFrac[ii],self.histYLog[ii]-
                               self.minPower,height=1./self.yBinNum,
                               color=barColorsY)
            if(ii != 0):
                self.axes_1DY.axhline(y=self.yBinEdgesFrac[ii],
                                      ls='--',lw=1,color='#444444')
        self.axes_1DY.xaxis.set_visible(False)
        self.axes_1DY.yaxis.set_visible(False)

        # Turn off window resizing so that the plot can't break
        # There is currently no implemented method to change all of the
        # fractional paramters if the window is resized, so clicking would
        # break
        plt.get_current_fig_manager().window.resizable(False,False)

        # Display text with the current version and any other messages
        self.figure.text(0.01,0.010,
                         __clickHistName__+' Version '+__version__,
                         fontsize=4)

        plt.show()

        return

    def generatePlotPositions(self):

        """
        This method calculates the x and y coordinates in the plot for each
        scatter point, xDataFrac and yDataFrac, using a fractional
        system with 0 and 1 as end points (e.g. 0.5 is "halfway"),
        the appropriate color to shade each point, pointColors, based on a
        colorbar generated using the maximum and minimum powers for the plot,
        and plotPos, which keeps track of the index of the x and y data
        in their original arrays.

        The color stored could be used in theory to determine the bin to which
        a particular point belongs. (NOTE: There is perhaps an argument to
        replace pointColors with "pointBin" or something similar in a future
        version, but sticking with legacy implementation for now.) This is
        needed to deal with the potential for uneven bin spacings.
        Additionally, this method thins out the data to meet the expectations
        of the point density per bin indicated by the user (maxPlottedInBin).

        :return: (1) Flattened x-axis histogram data containing the fractional
        position of each scatter point on the plot (e.g. 0.5 represents the
        middle of the plot, multiplied by a hypothetical width of 500 for the
        2D histogram yields 250 pixels from the left),
        (2) Same as (1), but for y-axis data, and
        (3) the associated color for each x-y scatter point based on the
        color bar generated by minPower and maxPower.
        (4) The indices of the selected x and y data in the original
        xData and yData arrays.
        """

        # Initialize the arrays that will be returned in the end
        print('Calculating pos...')
        xDataFrac = []
        yDataFrac = []
        pointColors = []
        plotPos = []
        for v1bin in range(0,self.xBinNum):
            for v2bin in range(0,self.yBinNum):

                # Calculate the middle point of each bin, determine its span
                # in either direction (i.e. 1/2 of its width), and then find
                # all points that belong to that particular bin
                xBinMid = (self.xBinEdges[v1bin]+self.xBinEdges[v1bin+1])/2.
                yBinMid = (self.yBinEdges[v2bin]+self.yBinEdges[v2bin+1])/2.
                xAcceptError = (self.xBinEdges[v1bin+1]-
                                self.xBinEdges[v1bin])/2.
                yAcceptError = (self.yBinEdges[v2bin+1]-
                                self.yBinEdges[v2bin])/2.
                localMatches = np.intersect1d(np.where(np.abs(self.xData-
                       xBinMid)<xAcceptError),np.where(np.abs(self.yData-
                       yBinMid)<yAcceptError))
                numOfLocalMatches = len(localMatches)

                # If there is at least one member to a bin...
                if(numOfLocalMatches != 0):
                    # If there are more points than the density allows,
                    # shuffle them before picking out the first
                    # maxPlottedInBin points for the plot.
                    if(numOfLocalMatches > self.maxPlottedInBin):
                        np.random.shuffle(localMatches)
                    for mm in range(0, min(numOfLocalMatches,
                                           self.maxPlottedInBin)):

                        # Keep track of the position of matches in the
                        # original xData and yData variables so that
                        # they can be found easily when ClickHistDo is called
                        plotPos.append(localMatches[mm])

                        # Get the x and y data, calculate the fractional
                        # position, and then store it
                        xDataTemp = self.xData[localMatches[mm]]
                        yDataTemp = self.yData[localMatches[mm]]
                        xDataFracTemp = ((1.0*v1bin/self.xBinNum)+
                            (self.calcFracPastBinMin(xDataTemp,self.xBinEdges,
                                                     v1bin)/self.xBinNum))
                        yDataFracTemp = ((1.0*v2bin/self.yBinNum)+
                            (self.calcFracPastBinMin(yDataTemp,self.yBinEdges,
                                                     v2bin)/self.yBinNum))
                        xDataFrac.append(xDataFracTemp)
                        yDataFrac.append(yDataFracTemp)

                        # Calculate the color of the scatterpoint based on its
                        # bin
                        locLogCount = self.histLog[v1bin,v2bin]
                        cbPercent = ((locLogCount-self.minPower) *
                                     (1.0/abs(self.minPower)))
                        pointColors.append(pylab.cm.Spectral_r(cbPercent))

        return np.array(xDataFrac),np.array(yDataFrac),\
               np.array(pointColors),np.array(plotPos)

    def findNearestPointToClick(self,xClickVal,yClickVal):
        """
        Returns the closest point to the click in terms of physical plot
        location (pixels), not necessarily by absolute value
        :param xClickVal: The fractional x location of the click within the
        2D histogram
        :param yClickVal: The fractional y location of the click within the
        2D histogram
        :return: The 1D array index of the closest point
        """
        error = ((self.xDataFrac-xClickVal)**2+
                 (self.yDataFrac-yClickVal)**2)**0.5
        minError = np.amin(error)
        locOfMinError = np.where(error == minError)[0][0]
        return locOfMinError

    def calcFracPastBinMin(self,value,binEdges,bin):
        """
        Calculates how far past the minimum of a bin a value is in the range 0
        to 1, with 1 being at the maximum of a bin (e.g. 15 with bin min 10 and
        bin max 20 would return 0.5)
        :param value: the value to convert
        :param binEdges: all bin edges
        :param bin: the position in bin edges of the bin minimum
        :return: a value between 0 and 1 indicating how far near the bin
        minimum (0) or maximum (1) the value lies
        """
        return ((value-binEdges[bin])/(binEdges[bin+1]-binEdges[bin]))

    def convertFracToValue(self,frac,binEdges,binEdgesFrac):
        """
        Converts a fractional location in a histogram to an actual value with
        units (e.g. from 0.5 to 50 mm/day)
        :param frac: the fractional location along the axis
        :param binEdges: the bin edge values (with units) along the axis
        :param binEdgesFrac: the fractional bin edge values
        :return: the converted value, now with units
        """
        bin = np.searchsorted(binEdgesFrac,frac)-1
        valPastBin = (((frac-binEdgesFrac[bin]) /
                      (binEdgesFrac[bin+1]-binEdgesFrac[bin])) *
                      (binEdges[bin+1]-binEdges[bin]))
        return binEdges[bin]+valPastBin

    def findPercentile(self,dataArray,point):
        """
        Determines the percentile that a particular data value belongs to
        among the data
        :param dataArray: An array with all data points, even those not plotted
        :param point: The value of a particular point
        :return: The percentile (0.0-99.9) of point relative to dataArray
        """
        return stats.percentileofscore(dataArray,point)

    def setDo(self,doObject):
        """
        Sets the ClickHistDo object
        :param doObject: A ClickHistDo object
        :return:
        """
        self.doObject = doObject
        return