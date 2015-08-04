import datetime
import os
from subprocess import call
import sys
import time

#weirdOffset = (4*3600)+(1-time.localtime().tm_isdst)*3600
weirdOffset = 2*3600

inTime = int(sys.argv[1])
adjTime = (inTime+weirdOffset)*1000 
lon = float(sys.argv[2])
lat = float(sys.argv[3])
fieldMovieFolder = ''
binMovieFolder = ''
if(len(sys.argv) >= 6):
    fieldMovieFolder = str(sys.argv[4])
    binMovieFolder = str(sys.argv[5])

if(len(sys.argv) == 5):
    print 'Need the field folder AND bin folder. Exiting...'
    sys.exit(1)

pathToMovieFolder = '/Users/niznik/Work/Plots/IDV_Movies/'
if not os.path.exists(pathToMovieFolder+fieldMovieFolder):
    os.mkdir(pathToMovieFolder+fieldMovieFolder)
if not os.path.exists(pathToMovieFolder+fieldMovieFolder+'/'+binMovieFolder):
    os.mkdir(pathToMovieFolder+fieldMovieFolder+'/'+binMovieFolder)

lonOffset = 5.0
latOffset = 5.0
timeOffsetBefore = -2*3600*1000
timeOffsetAfter = 4*3600*1000-timeOffsetBefore

westLon = str(lon-lonOffset)
eastLon = str(lon+lonOffset)
southLat = str(lat-latOffset)
northLat = str(lat+latOffset)

startTime = str(adjTime+timeOffsetBefore)
endTime = str(adjTime+timeOffsetAfter)
startOffset = str(timeOffsetBefore/(60.*1000.))
endOffset = str(timeOffsetAfter/(60.*1000.))

currentUnixTime = str(int(time.time()))
basisBundleFile = '/Users/niznik/Work/bin/GEOS5_IDVAutomation/NatureRun-uw-3DSections_timedriver_fillInNum_p1.xidv'
tempBundleFile = '/Users/niznik/Work/bin/GEOS5_IDVAutomation/TempBundles/tempBundle_'+currentUnixTime+'.xidv'
basisISLFile = '/Users/niznik/Work/bin/GEOS5_IDVAutomation/Scripts/idvMovieOutput_fillIn.isl'
tempISLFile = '/Users/niznik/Work/bin/GEOS5_IDVAutomation/Scripts/idvMovieOutput_'+currentUnixTime+'.isl'

#Somehow get things fed in here so that the movie description is meaningful
#Based on current isl file, don't need extension!
movieFilename = str(inTime)+'_'+str(lon)+'_'+str(lat)

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
call('sed -i \'.bckp\' \'s/'+maxLonFiller+'/'+eastLon+'/\' '+tempBundleFile,shell=True)
call('sed -i \'.bckp\' \'s/'+minLatFiller+'/'+southLat+'/\' '+tempBundleFile,shell=True)
call('sed -i \'.bckp\' \'s/'+maxLatFiller+'/'+northLat+'/\' '+tempBundleFile,shell=True)
call('sed -i \'.bckp\' \'s/'+centerLonFiller+'/'+str(lon)+'/\' '+tempBundleFile,shell=True)
call('sed -i \'.bckp\' \'s/'+centerLatFiller+'/'+str(lat)+'/\' '+tempBundleFile,shell=True)
call('sed -i \'.bckp\' \'s/'+lonLenFiller+'/'+str(lonOffset*2)+'/\' '+tempBundleFile,shell=True)
call('sed -i \'.bckp\' \'s/'+latLenFiller+'/'+str(latOffset*2)+'/\' '+tempBundleFile,shell=True)
call('sed -i \'.bckp\' \'s/'+startTimeFiller+'/'+startTime+'/\' '+tempBundleFile,shell=True)
call('sed -i \'.bckp\' \'s/'+endTimeFiller+'/'+endTime+'/\' '+tempBundleFile,shell=True)
call('sed -i \'.bckp\' \'s/'+startOffsetFiller+'/'+startOffset+'/\' '+tempBundleFile,shell=True)
call('sed -i \'.bckp\' \'s/'+endOffsetFiller+'/'+endOffset+'/\' '+tempBundleFile,shell=True)

if(fieldMovieFolder == ''):
    call('runIDV -bundle '+tempBundleFile,shell=True)
    call('rm -i '+tempBundleFile,shell=True)
else:
    call('cp '+basisISLFile+' '+tempISLFile,shell=True)
    call('sed -i \'.bckp\' \'s/UNIXTIME/'+currentUnixTime+'/\' '+tempISLFile,shell=True)
    call('sed -i \'.bckp\' \'s/FIELDMOVIEFOLDER/'+fieldMovieFolder+'/\' '+tempISLFile,shell=True)
    call('sed -i \'.bckp\' \'s/BINMOVIEFOLDER/'+binMovieFolder+'/\' '+tempISLFile,shell=True)
    call('sed -i \'.bckp\' \'s/MOVIENAME/'+movieFilename+'/\' '+tempISLFile,shell=True)
    
    call('runIDV -islfile '+tempISLFile,shell=True)

    call('rm '+tempBundleFile,shell=True)
    call('rm '+tempISLFile+'.bckp',shell=True)
    call('rm '+tempISLFile,shell=True)

call('rm '+tempBundleFile+'.bckp',shell=True)
