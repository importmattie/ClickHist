# ClickHist IDV Preprocessor
# author: matthewniznik
# email: matthew.niznik9@gmail.com
#
# This script preprocesses .xidv files for compatability with
# ClickHist. Please E-mail the author at the provided email
# if this script breaks the bundle.
#
# To test, try to open the processed script in IDV.
#
# Arg1: File to be processed
# Arg2: Output File

from lxml import etree as ET
import sys

# Get the input and output filenames from user input
inFile = str(sys.argv[1])
outFile = str(sys.argv[2])

# Parse the xml from the .xidv input and get the root
tree = ET.parse(inFile)
root = tree.getroot()

# Current recommended 'dummy' values for longitude, latitude,
# and time in the bundles
lonCen_value = '-154.123456789'
lonLen_value = '2.123456789'
lonMin_value = '-155.1851851835'
lonMax_value = '-153.0617283945'
lonInc_value = '0.345678912'

latCen_value = '0.135792468'
latLen_value = '1.592592592'
latMin_value = '-0.660503828'
latMax_value = '0.932088764'
latInc_value = '0.234567891'

startTime_value = '1117594837000'
endTime_value = '1117616461000'
startOffset_value = '-119.87654321'
endOffset_value = '361.23456789'

def main():

    for item in root.iter('object'):

        # Set the bounding box for the data
        if(doesAttribMatch(item,'class','java.awt.geom.Rectangle2D$Float')):
            item[0][0].text = lonMin_value
            item[0][1].text = latMin_value
            item[0][2].text = lonLen_value
            item[0][3].text = latLen_value

        # Set the center of the bounding box
        elif(doesAttribMatch(item,'class',
                             'ucar.unidata.geoloc.LatLonPointImpl')):
            item[0][0].text = latCen_value
            item[1][0].text = lonCen_value

    for item in root.iter('property'):
        
        # Set the min/max lon/lat as well as the start/end times and offsets
        if(doesAttribMatch(item,'name','MinLon')):
            item[0].text = lonMin_value
        elif(doesAttribMatch(item,'name','MaxLon')):
            item[0].text = lonMax_value
        elif(doesAttribMatch(item,'name','MinLat')):
            item[0].text = latMin_value
        elif(doesAttribMatch(item,'name','MaxLat')):
            item[0].text = latMax_value
        elif(doesAttribMatch(item,'name','StartFixedTime')):
            item[0].text = startTime_value
        elif(doesAttribMatch(item,'name','EndFixedTime')):
            item[0].text = endTime_value
        elif(doesAttribMatch(item,'name','StartOffsetMinutes')):
            item[0].text = startOffset_value
        elif(doesAttribMatch(item,'name','EndOffsetMinutes')):
            item[0].text = endOffset_value

        # Set the bounding box information
        elif(doesAttribMatch(item,'name','BaseLabel')):
            if(doesAttribMatch(item.getparent(),
                               'class',
                               'ucar.unidata.view.geoloc.LatLonAxisScaleInfo')
               ):
                if(doesAttribMatch(item.getparent().getparent(),
                                   'name','LonAxisScaleInfo')):
                    item[0].text = lonMin_value
                elif(doesAttribMatch(item.getparent().getparent(),
                                     'name','LatAxisScaleInfo')):
                    item[0].text = latMin_value

        elif(doesAttribMatch(item,'name','Increment')):
            if(doesAttribMatch(item.getparent(),
                               'class',
                               'ucar.unidata.view.geoloc.LatLonAxisScaleInfo')
               ):
                if(doesAttribMatch(item.getparent().getparent(),
                                   'name','LonAxisScaleInfo')):
                    item[0].text = lonInc_value
                elif(doesAttribMatch(item.getparent().getparent(),
                                     'name','LatAxisScaleInfo')):
                    item[0].text = latInc_value

    # Output results
    tree.write(outFile,xml_declaration=True,encoding='ISO-8859-1')

# This method just simplifies some of the text when looking for
# matches in the XML
def doesAttribMatch(item,attrib,inquiry):
    if(item.attrib.has_key(attrib)):
        if(item.attrib[attrib] == inquiry):
            return 1
    else:
        return 0

if __name__ == "__main__":
    main()
