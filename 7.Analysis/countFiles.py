from collections import OrderedDict
import os
import random
import json
import sys

if(len(sys.argv)<3):
    print "execution : $ python countFiles.py <root path of the directory containing all the mime types> <path for output json file>"
    exit()

#path = "/Users/charanshampur/newFIleAnalysis/Classified"
path=str(sys.argv[1])
jsonTrecFile = open(str(sys.argv[2]),"w")
fileCount = {};

#Traverse through all the files under different mime-types to calculate the count of files

for filePath,dirs,files in os.walk(path):
    if(len(files)>1):
        direcPath = filePath.split("/")
        dirStr = direcPath[len(direcPath)-2]+"/"
        dirStr+= direcPath[len(direcPath)-1]
        fileCount[dirStr]=len(files)

contentList=[]
content={}
jsonTrecData={}

# Writes the data to a json file for visualizing it as a pie chart
for key,value in fileCount.items():
    content=OrderedDict()
    content["label"]=key
    content["value"]=int(value)
    content["color"]="#%06x" % random.randint(0, 0xFFFFFF)
    contentList.append(content)

jsonTrecData["data"] = contentList
json.dump(jsonTrecData,jsonTrecFile,indent=4)
jsonTrecFile.close()