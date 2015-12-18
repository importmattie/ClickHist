__author__ = 'niznik'

import calendar
import datetime
import os
import sys
from subprocess import call
import time

class ClickHistDo:
    def __init__(self,lons,lats,times,startDatetime,bundle,**kwargs):

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

        self.startDatetime = startDatetime

        self.lonOffset = 5.0
        self.latOffset = 5.0
        self.dtFromCenter = (2*3600)*1000

        self.bundleInFilename = bundle

        self.doObjectHint = 'save IDV bundle...'

        #Handle kwargs for output
        if(kwargs.has_key('xVarName')):
            self.xVarName = kwargs.get('xVarName')
        if(kwargs.has_key('yVarName')):
            self.yVarName = kwargs.get('yVarName')
        if(kwargs.has_key('lonOffset')):
            self.lonOffset = kwargs.get('lonOffset')
        if(kwargs.has_key('latOffset')):
            self.latOffset = kwargs.get('latOffset')
        if(kwargs.has_key('dtFromCenter')):
            self.dtFromCenter = kwargs.get('dtFromCenter')*1000

    def do(self,flatIndex,**kwargs):

        #Check if the metadata tag was included
        if(kwargs.has_key('metadata')):
            self.metadata = kwargs.get('metadata')
        if(kwargs.has_key('xPer')):
            self.xPer = kwargs.get('xPer')
        if(kwargs.has_key('yPer')):
            self.yPer = kwargs.get('yPer')

        #Make sure output folders exist
        if(os.path.exists('./Output/Tmp/') == False):
            call('mkdir ./Output/Tmp/',shell=True)
        if(os.path.exists('./Output/GeneratedBundles/') == False):
            call('mkdir ./Output/GeneratedBundles/',shell=True)
        if(os.path.exists('./Output/GeneratedBundlesZ/') == False):
            call('mkdir ./Output/GeneratedBundlesZ/',shell=True)
        if(os.path.exists('./Output/ImageScripts/') == False):
            call('mkdir ./Output/ImageScripts/',shell=True)
        if(os.path.exists('./Output/Images/') == False):
            call('mkdir ./Output/Images/',shell=True)

        print('Saving IDV bundle...')

        currentUnixTime = str(int(time.time()))
        basisBundleFile = './Output/Templates/'+self.bundleInFilename

        tempBundleFile = './Output/Tmp/tempBundle_'+currentUnixTime+'.xidv'

        inputLonIndex,inputLatIndex,inputTimeIndex = self.find3DIndices(flatIndex)
        inputLon = self.lons[inputLonIndex]
        inputLat = self.lats[inputLatIndex]
        inputDatetime = self.startDatetime+datetime.timedelta(0,(self.times[inputTimeIndex]))
        inputTime = int(calendar.timegm(inputDatetime.timetuple()))

        print(inputDatetime)
        print("{:3.0f}".format(inputLon)+' E '+"{:2.0f}".format(inputLat)+' N')
        if(kwargs.has_key('xyVals')):
            print(kwargs.get('xyVals'))

        westLon = str(inputLon-self.lonOffset)
        eastLon = str(inputLon+self.lonOffset)
        southLat = str(inputLat-self.latOffset)
        northLat = str(inputLat+self.latOffset)

        adjTime = int(inputTime)*1000

        startTime = str(adjTime-self.dtFromCenter)
        endTime = str(adjTime+self.dtFromCenter)
        #IDV wants these in minutes
        startOffset = str(0)
        endOffset = str((self.dtFromCenter*2)/(60*1000))

        timeTag = self.convertToYMDT(inputTime)
        commonFilename = self.xVarName+'_'+self.yVarName+'_'+\
                         "{:005.0f}".format(min(1000*self.xPer,99999))+'_'+\
                         "{:005.0f}".format(min(1000*self.yPer,99999))+'_'+\
                          str("%03i"%inputLon)+'_'+str("%02i"%inputLat)+'_'+timeTag
        finalBundleFile = './Output/GeneratedBundles/'+commonFilename+'.xidv'

        centerLonFiller = '-154.123456789'
        #lonLenFiller = '10.123456789'
        #minLonFiller = '-159.1851851835'
        #maxLonFiller = '-149.0617283945'
        lonLenFiller = '2.123456789'
        minLonFiller = '-155.1851851835'
        maxLonFiller = '-153.0617283945'
        incLonFiller = '0.345678912'

        centerLatFiller = '0.135792468'
        #latLenFiller = '7.592592592'
        #minLatFiller = '-3.660503828'
        #maxLatFiller = '3.932088764'
        latLenFiller = '1.592592592'
        minLatFiller = '-0.660503828'
        maxLatFiller = '0.932088764'
        incLatFiller = '0.234567891'

        startTimeFiller = '1117594837000'
        endTimeFiller = '1117616461000'
        startOffsetFiller = '-119.87654321'
        endOffsetFiller = '361.23456789'
        metadataFiller = 'replaceme_METADATASTRING_replaceme'

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
        call('sed '+backupTag+' \'s/'+incLonFiller+'/'+str(self.lonOffset/2.)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+incLatFiller+'/'+str(self.latOffset/2.)+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+startTimeFiller+'/'+startTime+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+endTimeFiller+'/'+endTime+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+startOffsetFiller+'/'+startOffset+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+endOffsetFiller+'/'+endOffset+'/\' '+tempBundleFile,shell=True)
        call('sed '+backupTag+' \'s/'+metadataFiller+'/'+self.metadata+'/\' '+tempBundleFile,shell=True)

        #Save the bundle with a recognizable filename
        call('mv '+tempBundleFile+' '+finalBundleFile,shell=True)
        call('rm '+tempBundleFile+'.bckp',shell=True)

        print('Saved!')

        basisISL = './Output/Templates/idvMovieOutput_fillIn.isl'
        tempISL = './Output/ImageScripts/idvImZIDVOutput_'+commonFilename+'.isl'
        #Process via sed
        call('sed \'s/BUNDLENAME/'+commonFilename+'/\' '+basisISL+' > '+tempISL,shell=True)
        call('sed '+backupTag+' \'s/MOVIENAME/'+commonFilename+'/\' '+tempISL,shell=True)
        call('sed '+backupTag+' \'s/IMAGENAME/'+commonFilename+'/\' '+tempISL,shell=True)
        call('sed '+backupTag+' \'s/\"METADATA\"/\"'+self.metadata+'\"/\' '+tempISL,shell=True)
        #clean up backup files
        call('rm '+tempISL+'.bckp',shell=True)

    def convertToYMDT(self,unixTime):
        #Check for timezones in next version
        #ymdt = datetime.datetime.fromtimestamp(unixTime)
        ymdt = datetime.datetime.utcfromtimestamp(unixTime)
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