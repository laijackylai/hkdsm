###################################################################################################
### This python file is used to change the xyz file to csv file                                 ###
###################################################################################################
# import the package needed
#import osgeo
import pandas as pd
import numpy as np
import os
import time

start_time = time.time()

# set paths


inpath = os.getcwd() + "/input_txt/"
outpath = os.getcwd() + "/csv/"

os.chdir(inpath)
files = [f for f in os.listdir(
    inpath) if os.path.isfile(os.path.join(inpath, f))]

# open .xyz file as csv file
for f in files:
    print(f)
    df = pd.read_csv(inpath + f, sep=",")
    df = df.dropna(axis=1)
    df = pd.DataFrame(np.vstack([df.columns, df]))
    for i in [0, 1, 2, 3]:
        df.iloc[0][i] = float(df.iloc[0][i])
    df.columns = ["Lon", "Lat", "Ele", "Na", "Na2"]
    name = f.split('.')[0]
    df = df.drop(columns={'Na', 'Na2'})
    df["Ele"] = df["Ele"] + 0.146
    print(df)
    df.to_csv(outpath + name + ".csv", index=False)

print("--- %s seconds ---" % (time.time() - start_time))
