from collections import OrderedDict

import json
import random
import sys

if(len(sys.argv)<3):
    print "Execution = $ python Generate_Trec_Mime.py <Path to new file> <path to trec json file>"
    exit()

jsonTrecFile = open(sys.argv[1],"rb+")
inputMimeFile = open(sys.argv[2],"r")
jsonTrecData=OrderedDict()
jsonTrecData = json.load(jsonTrecFile,object_pairs_hook=OrderedDict)
jsonInputData = json.load(inputMimeFile)

contentList = []

for key,value in jsonInputData.items():
    content=OrderedDict()
    content["label"] = key
    content["value"] = int(value)
    content["color"] = "#%06x" % random.randint(0, 0xFFFFFF)
    contentList.append(OrderedDict(content))

jsonTrecData["data"]["content"] = contentList
jsonTrecFile.seek(0,0)
json.dump(jsonTrecData,jsonTrecFile,indent=4)
jsonTrecFile.close()
inputMimeFile.close()


