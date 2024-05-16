# Importing the libraries
# Our data processing tools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.impute import SimpleImputer

import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

#Importing data settings
#dataset = pd.read_csv(dir_path +'/Data.csv')

# open inputFile.txt with the intention of reading it
inputFile = open(dir_path +"/inputFile.txt", "r")

# open passFile.txt with the intention of writing it
passFile = open(dir_path +"/passFile.txt", "w")

# open failFile.txt with the intention of writing it
failFile = open(dir_path +"/failFile.txt", "w")

# loop through each line in inputFile.txt
# uncomment the following lines of code and fill in
for line in inputFile:
    line_split = line.split()
    if line_split[2] == "P":
        passFile.write(line)
    else:
        failFile.write(line)

# close inputFile.txt
inputFile.close()

# close passFile.txt
passFile.close()

# close failFile.txt
failFile.close()