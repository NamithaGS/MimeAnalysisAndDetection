import math
import os
import sys

if(len(sys.argv)<2):
    print "execution : $ python FHT.py <path to directory containing files>"
    exit()
# path of the directory of files for generating header matrix
path = "/Users/charanshampur/newAwsDump/dumpedContents/application/rdf+xml";
#path="/Users/charanshampur/newAwsDump/dumpedContents/application/rdf+xml"
#path = "/Users/charanshampur/newAwsDump/dumpedContents/additional_test_files/gif/base_files "

# CSV file of file signature
fhtFile4 = open("head4application_rdfXml.csv", "w")
fhtFile8 = open("head8application_rdfXml.csv", "w")
fhtFile16 = open("head16application_rdfXml.csv", "w")

fttFile4 = open("tail4application_rdfXml.csv", "w")
fttFile8 = open("tail8application_rdfXml.csv", "w")
fttFile16 = open("tail16application_rdfXml.csv", "w")

fttTable={}
fhtTable={}
for i in range (0,16):
    fhtTable[i]=[0] * 256
    fttTable[i]=[0] * 256

numberOfFiles = 0

def bytes2int(str):
 return int(str.encode('hex'), 16)

# Traverse through each file in the repository and calculates the file header and trailer byte distribution
# matrix
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
            if(len(bytesRead)>16):
                headEnd = 16
                tailEndBlock = len(bytesRead) - 17
            else:
                headEnd = len(bytesRead)
                tailEndBlock = -1
            for i in range(0,headEnd):
                byteStr = bytesRead[i]
                byte = bytes2int(byteStr)
                fhtTable[i][byte]+=1


            for i in range(len(bytesRead)-1,tailEndBlock,-1):
                byteStr=bytesRead[i]
                byte = bytes2int(byteStr)
                fttTable[len(bytesRead)-i-1][byte]+=1
        numberOfFiles+=1

for key in fhtTable.keys():
    fhtTable[key] = [math.sqrt(float(x)/float(numberOfFiles)) for x in fhtTable[key]]
    fttTable[key] = [math.sqrt(float(x)/float(numberOfFiles)) for x in fttTable[key]]

header = ","+",".join(["Byte Value : "+ str(x) for x in range(0,256)])
fhtFile4.write(header+"\n")
fhtFile8.write(header+"\n")
fhtFile16.write(header+"\n")
fttFile4.write(header+"\n")
fttFile8.write(header+"\n")
fttFile16.write(header+"\n")

#Writes the header and trailer byte matrix to csv files.
for key in fhtTable.keys():
    row = str(key)+" Header Byte,"+",".join([str(x) for x in fhtTable[key]])
    if int(key) < 4 :
        fhtFile4.write(row+"\n")
    if int(key) < 8 :
        fhtFile8.write(row+"\n")
    fhtFile16.write(row+"\n")

for key in fttTable.keys():
    row = str(key)+" Trailer Byte,"+",".join([str(x) for x in fttTable[key]])
    if int(key) < 4 :
        fttFile4.write(row+"\n")
    if int(key) < 8 :
        fttFile8.write(row+"\n")
    fttFile16.write(row+"\n")

