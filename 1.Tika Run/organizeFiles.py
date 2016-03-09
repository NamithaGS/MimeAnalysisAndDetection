import os
import shutil
from tika import parser
import json
import subprocess
import sys

if(len(sys.argv)<3):
    print "execution = $ python organizeFiles.py <path to S3 downloaded files directory> <path of destination directory>"
    exit()
# Root Directory of the files dumped from amazon
#path = "/Users/charanshampur/newFIleAnalysis/Octet-stream"
path = str(sys.argv[1])

# Root Directory where the organized files will be written
#destPath = "/Users/charanshampur/newFIleAnalysis/Classified"
destPath = str(sys.argv[2])

# Tika Snapshot Jar location
tikaSnapshotPath = "/Users/charanshampur/nutch/tika/tika/tika-app/target/tika-app-1.11-SNAPSHOT.jar"

contentTypeDict={}
errorFileCount = 1

# Error file : contains a list of files which tika failed to parse
errorFile = open("errorFile.txt","w")

# This function is used to write to error directory the files which tika was unable to parse
def writeError(path_to_file,destPath,file):
    errorFile.write(path_to_file+"\n")
    if not os.path.exists(destPath+"/error"):
        os.makedirs(destPath+"/error")
    shutil.move(path_to_file,destPath+"/error/"+str(file))

# This function is used to validate the content-type.
def validateContent(contentType):
    if ';' in contentType and type(contentType) != list:
        contentType = contentType.split(";")[0]
        return contentType
    if type(contentType) is list:
        contentType = contentType[0]
        return contentType
    return contentType

# Traverse through each file in the repository and runs tika on them
for path, dirs, files in os.walk(path):
    print path
    for file in files:
        if file not in ".DS_Store":
            path_to_file = path+"/"+str(file)
            print path_to_file
            parsed = parser.from_file(path_to_file)
            if parsed == {}:
                try:
                    outputDict=subprocess.check_output(['java', '-jar', tikaSnapshotPath, '-j', path_to_file])
                    outputDict = json.loads(outputDict)
                    contentType = validateContent(outputDict["Content-Type"])
                except:
                    writeError(path_to_file,destPath,file)
                    print "Tika Command line failed"
                    continue
            else:
                try:
                    contentType = validateContent(parsed["metadata"]["Content-Type"])
                except KeyError:
                    print "KeyError"
                    writeError(path_to_file,destPath,file)
                    errorFileCount+=1
                    continue
            directory = destPath+"/"+contentType
            if contentType not in contentTypeDict:
                contentTypeDict[contentType]=1
                if not os.path.exists(directory):
                    os.makedirs(directory)
                destFileName = directory+"/"+str(file)
            else:
                contentTypeDict[contentType]+=1
                destFileName = directory+"/"+str(file)
            shutil.move(path_to_file,destFileName)
errorFile.close()