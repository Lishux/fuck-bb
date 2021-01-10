#!/usr/bin/env python3

import os
import pandas as pd

curDir = os.getcwd()
for f in os.listdir(curDir):
    if f.endswith(".xlsx"):
        nameIDFile = f
        break

# change skiprows to ~$(row index of '姓名') - 1~
data = pd.read_excel(nameIDFile, engine="openpyxl", index_col=0, skiprows=5)[{'姓名','学号'}].dropna()
nameID = {}
for i in range(len(data)):
    nameID[data.iloc[i]['姓名'].strip('*')] = data.iloc[i]['学号']

HWDir = curDir + "/HW/"
for name in os.listdir(HWDir):
    if name in nameID:
        os.system("mv " + HWDir + name + " " + HWDir + nameID[name] + name)
        print(name, nameID[name], sep='\t')
    else:
        print(name, "not in table!!!", sep='\t')
