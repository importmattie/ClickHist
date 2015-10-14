__author__ = 'niznik'

import datetime
import os
import sys
from subprocess import call
from subprocess import Popen
import time

class ClickHistDo:
    def __init__(self,lons,lats,times,**kwargs):

        self.os = sys.platform

        self.lons = lons
        self.lats = lats
        self.times = times

        self.lonLen = len(self.lons)
        self.latLen = len(self.lats)
        self.timeLen = len(self.times)

        self.xVarName = 'xVar'
        self.yVarName = 'yVar'
        self.metadata = ''
        self.xPer = 99.9
        self.yPer = 99.9

        self.startDatetime = datetime.datetime(2005,05,16)
        #This is due to a as-of-yet poorly understood difference between Unix time and IDV time
        #It also doesn't seem to be consistent
        self.timeCorrection = 2*3600

        self.lonOffset = 5.0
        self.latOffset = 5.0
        self.timeOffsetBefore = -2*3600*1000
        self.timeOffsetAfter = 4*3600*1000-self.timeOffsetBefore

        self.doObjectHint = 'save IDV bundle...'

        #Handle kwargs for output
        if(kwargs.has_key('xVarName')):
            self.xVarName = kwargs.get('xVarName')
        if(kwargs.has_key('yVarName')):
            self.yVarName = kwargs.get('yVarName')

    def do(self,flatIndex,**kwargs):

        #Check if the metadata tag was included
        if(kwargs.has_key('metadata')):
            self.metadata = kwargs.get('metadata')
        if(kwargs.has_key('xPer')):
            self.xPer = kwargs.get('xPer')
        if(kwargs.has_key('yPer')):
            self.yPer = kwargs.get('yPer')

        print 'Saving IDV bundle...'

        currentUnixTime = str(int(time.time()))
        basisBundleFile = './Bundles/'+'ClickHist_testBundle.xidv'
        #Write a line in here to make a more normal, hidden temp directory?
        if(os.path.exists('./Bundles/TempBundles/') == False):
            call('mkdir ./Bundles/TempBundles/',shell=True)
        tempBundleFile = './Bundles/TempBundles/tempBundle_'+currentUnixTime+'.xidv'

        inputLonIndex,inputLatIndex,inputTimeIndex = self.find3DIndices(flatIndex)
        inputLon = self.lons[inputLonIndex]
        inputLat = self.lats[inputLatIndex]
        inputTime = int(time.mktime((self.startDatetime+datetime.timedelta(0,(self.times[inputTimeIndex]+30)*60
                                                                           )).timetuple()))

        print self.startDatetime+datetime.timedelta(0,(self.times[inputTimeIndex]+30)*60)

        westLon = str(inputLon-self.lonOffset)
        eastLon = str(inputLon+self.lonOffset)
        southLat = str(inputLat-self.latOffset)
        northLat = str(inputLat+self.latOffset)

        adjTime = (inputTime+self.timeCorrection)*1000

        startTime = str(adjTime+self.timeOffsetBefore)
        endTime = str(adjTime+self.timeOffsetAfter)
        startOffset = str(self.timeOffsetBefore/(60.*1000.))
        endOffset = str(self.timeOffsetAfter/(60.*1000.))

        #This needs to be fixed eventually
        timeTag = self.convertToYMDT(inputTime)
        commonFilename = self.xVarName+'_'+self.yVarName+'_'+\
                         "{:003.0f}".format(min(10*self.xPer,999))+'_'+\
                         "{:003.0f}".format(min(10*self.yPer,999))+'_'+\
                          str("%03i"%inputLon)+'_'+str("%02i"%inputLat)+'_'+timeTag
        finalBundleFile = './Bundles/'+commonFilename+'.xidv'

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
        elif(self.os.startswith('linux')):
            backupTag = '-i.bckp'

        call('sed \'s/'+minLonFiller+'/'+westLon+'/\' '+basisBundleFile+' > '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+maxLonFiller+'/'+eastLon+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+minLatFiller+'/'+southLat+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+maxLatFiller+'/'+northLat+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+centerLonFiller+'/'+str(inputLon)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+centerLatFiller+'/'+str(inputLat)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+lonLenFiller+'/'+str(self.lonOffset*2)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+latLenFiller+'/'+str(self.latOffset*2)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+startTimeFiller+'/'+startTime+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+endTimeFiller+'/'+endTime+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+startOffsetFiller+'/'+startOffset+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+endOffsetFiller+'/'+endOffset+'/\' '+tempBundleFile,shell=True)

        #Save the bundle with a recognizable filename
        call('mv '+tempBundleFile+' '+finalBundleFile,shell=True)
        call('rm '+tempBundleFile+'.bckp',shell=True)

        print 'Saved!'

        if(os.path.exists('./Bundles/Images/') == False):
            call('mkdir ./Bundles/Images/',shell=True)

        basisISL = './Bundles/idvMovieOutput_fillIn.isl'
        tempISL = './Bundles/Images/idvMovieOutput_'+currentUnixTime+'.isl'
        #Process via sed
        call('sed \'s/BUNDLENAME/'+commonFilename+'/\' '+basisISL+' > '+tempISL,shell=True)
        call('sed '+backupTag+' \'s/MOVIENAME/'+commonFilename+'/\' '+tempISL,shell=True)
        call('sed '+backupTag+' \'s/IMAGENAME/'+commonFilename+'/\' '+tempISL,shell=True)
        call('sed '+backupTag+' \'s/METADATA/'+self.metadata+'/\' '+tempISL,shell=True)
        #clean up backup files
        call('rm '+tempISL+'.bckp',shell=True)

    def convertToYMDT(self,unixTime):
        #Check for timezones in next version
        ymdt = datetime.datetime.fromtimestamp(unixTime)
        return str(ymdt.year)+"{:02.0f}".format(ymdt.month)+"{:02.0f}".format(ymdt.day)+'_'+\
               "{:02.0f}".format(ymdt.hour)+"{:02.0f}".format(ymdt.minute)

    def find3DIndices(self,flatIndex):
        lon = flatIndex%self.lonLen
        lat = (flatIndex/self.lonLen)%self.latLen
        time = flatIndex/(self.lonLen*self.latLen)
        return lon,lat,time

    def setNameAtHost(self,nameAtHost):
        self.nameAtHost = nameAtHost
        return

    def setPathAtHost(self,pathAtHost):
        self.pathAtHost = pathAtHost
        return