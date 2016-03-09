# Synopsis
MIME Diversity in the Text Retrieval Conference (TREC) Polar Dynamic Domain Dataset

## Motivation
As a team project, performing a MIME diversity analysis of the TREC-DDPolar dataset, helping to answer questions like why Tika’s MIME detection system did not have sufficient detection abilities to classify some of scientific data types into proper MIME types , 
and providing new and improved mechanisms for MIME detection in Tika for scientific Big Data. 
To understand these unknown types in a rich scientific domain better, MIME diversity analysis methods like Byte-based fingerprints of the data via Byte Frequency Analysis (BFA), Byte Frequency Distribution (BFD) Correlation, Byte Frequency Cross-Correlation (BFC), and File Header Trailer (FHT) are used.

Goal is to try improve Tika’s overall ability by suggesting new MIME magic for its database, and improve techniques for MIME detection in the Big Data present in the TREC-DD-Polar dataset.

#Installation
## organizeFiles.py 
This program classifies the files downloaded from the s3 bucket into their respective Mime-Types. The program does this classification by running Apache Tika on them. Files which are successfully parsed by tika are placed into an hierarchical directory structure according to their content- type. Files for which Tika gave exceptions are placed into an error directory.
Execution : 
$ python organizeFiles.py <path to S3 downloaded files directory> <path of destination directory>

## Generate_Trec_Mime.py
This program parses the Json file present in https://github.com/chrismattmann/trec-dd-polar/ and generates a Json data for visualizing it using d3 pie chart
Execution :
$ python Generate_Trec_Mime.py <Path to new file> <path to trec json file>

## BFA.py 
This program parses through all the files present in the directory of a particular mime type and outputs the signature as a json file.
Execution :
$ python BFA.py <Path to directory containing files> <output json file name>

## FHT.py :
This program parses through all the files present in the directory of a particular mime type  and outputs the File header and trailer byte positions as a csv file.
Execution :
$ python FHT.py <path to directory containing files>

## countFiles.py
This program counts the number of files present in each type and outputs the count as a json. This json file is further used to generate a d3 pie chart.
Execution :
$ python countFiles.py <root path of the directory containing all the mime types> <path for output json file>

# D3 Scripts -
## Byte Frequency Analysis
BFA.html - 
Generates Interactive visualization of Byte Frequencies which are represented as bar graphs. The D3 takes as input the signatures generated from BFA.py.

## File Header Trailer Analysis
fht.html -
Generates Interactive visualization of File header and trailers which are represented as a sparse matrix. The D3  takes as input the csv files generated by FHT.py. This script uses the library provided by Compass Inc for visualizing the data as matrix
Library: https://github.com/CompassInc/correlation-explorer.git

## Visualization of TREC dataset
Trec_Mime_Types.html -
Generates Interactive pie chart for visualizing the distribution of different mime types in the TREC dataset. The D3 takes as input a Json file which gives the frequency of occurences of each file under each mime type. The script uses the library provide by http://d3pie.org/ in generating the pie chart.
Library: https://github.com/benkeen/d3pie.git

## Contributors
Charan Shampur

Manisha Kampasi

## License
Apache Tika
https://tika.apache.org/license.html
