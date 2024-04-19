# Importing the libraries
# Our data processing tools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.impute import SimpleImputer

import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

#Importing data settings
dataset = pd.read_csv(dir_path +'/Data.csv')
# main feature
# take all the column but not the last one  [ lower bound: up bound, -> rows   , lower bound: up bound ] -> columns
x = dataset.iloc[:, : -1].values 

# dependent var
# take all rows range but only the last column
y = dataset.iloc[:, -1].values 

#Taking care of missing data
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer.fit(x[:,1:3])
x[:,1:3] =imputer.transform(x[:,1:3])

print(x)