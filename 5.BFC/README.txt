Description: This program calculates two different things:
a) The BFD correlation strengths between the byte frequencies of the same byte values in all input files belonging to the same mime type. Also, two min and max correlation strengths.
b) The BFC cross correlation matrix.

NOTE: This program needs to be run once per mime type.

To run this program, invoke the program with the following arguments in the command-line:

python BFC.py <Path to BFA fingerprint file> <Path to directory containing files> 

1. Path to BFA fingerprint file: 
Output from the BFA.py program 
2. Path to directory containing files: 
Path to directory containing the 25% files belonging to each mime type


Output will be genrated in the same directory where the BFC.py program resides. 
There will be two output files per mime type:
<mimetype>_correlation.json -----------This is required for Graph 1 (BFD correlation)
<mimetype>_correlationmatrix.csv -----------This is required for Graph 2 (BFC cross correlation)

_______________________________________________________________________________________________________________
_______________________________________________________________________________________________________________

The fingerptint files generated from the above programs have been placed into a folder "BFCOutput". 
The D3js code files (HTML,JS and CSS) also need to be placed at the same level as the fingerprints.