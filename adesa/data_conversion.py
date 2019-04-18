# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 17:04:47 2019

@author: Visitor
"""

import pandas as pd
from collections import Counter
import os

date = 'OPENLANE_CA_Inventory_INC_03282019055639.txt'
path='C:\\Users\\Visitor\\Desktop\\python_code\\adesa\\outbound\\'

data = pd.DataFrame()

for file in os.listdir(path):
    if (file.endswith(".txt") & (date in file)):
        print(file)
        #data = data.append(pd.read_csv(path+file, sep="|", header=None), ignore_index=True)
        data = pd.concat([data, (pd.read_csv(path+file, sep="|", header=None))], ignore_index=True)
        


data.columns = ['vehicle ID', 'vin', 'auction status', 'seller', 'year', 'make', 'model', 'trim', 'body style',
                'engine', 'engine litres', 'engine cylinders', 'transmission', 'wheel drive', 14, 'interior color',
                'exterior color', 'inventory type', 'odo', 'registration province', 'postal code', 22, 23,
                '', 25, 'page url', 'image url',  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,
                40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,
                53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,
                66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,
                79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,
                92,  93,  94,  95,  96,  97,  98,  99, 100, 'front img url', 102, 'history type', 'run letter',
               'run number', 'lane', 'location', 108, 109, 110, 'vehicle type', 'odo unit', 'event type', 'auction date 2',
               115, 116, 117,
               'grade', 119, 120, 121, 'year_2', 'make_2', 'model_2', 'trim_2', 'province', 'tire', 'inspection date', 
               'location_2', 'damage notes',
               131, 132, 133, 134, 135 ]

#data = pd.read_fwf(path)