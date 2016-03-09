import operator
import math
import os
import json
import sys
from collections import OrderedDict

# path of the directory of files for generating finger print
#path = "/Users/charanshampur/newAwsDump/dumpedContents/application/octet-stream";
# single file analysis
if(len(sys.argv)<3):
    print "Execution = $ python BFA.py <Path to directory containing files> <output json file name>"
    exit()

#path = "/Users/charanshampur/newFIleAnalysis"
path=str(sys.argv[1])

# json file of file signature
fingerPrintFile = open(str(sys.argv[2]),"w")

fingerPrintBytes={}

for i in range(0,256):
    fingerPrintBytes[i]=0

normalfactor = 0
numberOfFiles = 0

def bytes2int(str):
 return int(str.encode('hex'), 16)

#Traverse through each file in the repository and calculates the Byte Histogram.
for path, dirs, files in os.walk(path):
    for file in files:
        if file in ".DS_Store":
            continue
        else:
            bytesDict = {}
            path_to_file = path+"/"+str(file)
            print path_to_file
            filePointer = open(path_to_file,"rb")
            bytesRead = filePointer.read()
            if(len(bytesRead)==0):
                continue
            for i in range(0,len(bytesRead)):
                byteStr = bytesRead[i]
                byte = bytes2int(byteStr)
                if byte not in bytesDict:
                    bytesDict[byte]=1
                else:
                    bytesDict[byte]+=1
            # Normal factor
            normalfactor=max(bytesDict.iteritems(), key=operator.itemgetter(1))[1]
            # Normalizing The byte frequencies and apply mu-law companding function
            for key,value in bytesDict.items():
                newValue=float(value)/normalfactor
                newValue=math.sqrt(newValue)
                bytesDict[key]=newValue

            for key,value in bytesDict.items():
                newFpScore = (fingerPrintBytes[key] * numberOfFiles) + value
                newFpScore = (newFpScore)/(numberOfFiles + 1)
                fingerPrintBytes[key] = newFpScore
        numberOfFiles+=1
print fingerPrintBytes

# Converts the histogram into Byte frequency Signature for the file
freqList = []
fingerPrintJson={}
for i in range(0,len(fingerPrintBytes)):
    byteFreq = {}
    byteFreq["byte"]=str(i)
    byteFreq["frequency"]=fingerPrintBytes[i]
    freqList.append(dict(byteFreq))
fingerPrintJson["fingerPrint"]=freqList
json.dump(fingerPrintJson,fingerPrintFile,indent=4)










