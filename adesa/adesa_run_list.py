# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:16:52 2019

@author: Visitor
"""

import pandas as pd
from ftplib import FTP_TLS
import os
import re
import json
import datetime
import numpy as np

def get_latest_file():
    with open('filenames.json') as json_file:  
        files = json.load(json_file)
    flag = 0
    ftp = FTP_TLS(host='olftp.adesa.com', user='German_Star_Motors', passwd='aU)kj7Qn8')
    ftp.prot_p()
    #ftp.retrlines('LIST')
    ftp.cwd('outbound/')
    
    file_list = []
    ftp.retrlines('MLSD', file_list.append)
    #ftp.dir(file_list.append)
    max_value = 0
    full_max = 0
    filename = ''
    full_file = ''
    for i in file_list:
        col = i.split(';')
        col_max = int(re.search(r'\d+', col[0]).group())
        if (col_max>max_value) & ('.txt' in col[-1]):
            max_value = col_max
            filename = col[-1].replace(' ', '')
        if (col_max>full_max) & ('.txt' in col[-1]) & ('FULL' in col[-1]):
            full_max = col_max
            full_file = col[-1].replace(' ', '')

    if (filename != files['inc_file']):
        localfile = open(filename, 'wb')
        ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        localfile.close()
        print("Inc file data tranfer complete")
        flag = 1
    else:
        print("Inc already there")
        
    if (full_file != files['full_file']):
        localfile = open(full_file, 'wb')
        ftp.retrbinary('RETR ' + full_file, localfile.write, 1024)
        localfile.close()
        print("Full file data tranfer complete")
        flag = 1
    else:
        print("Full already there")
    
    if flag == 1:
        new_names = {
                    'full_file': full_file,
                    'inc_file': filename
                    }
        with open('filenames.json', 'w') as outfile:  
            json.dump(new_names, outfile)
            
    ftp.quit()
    return filename, full_file, flag

def get_dataframe(filename):
    data = pd.read_csv(filename, sep="|", header=None)
    
    data.columns = ['adesa_id', 'vin', 'status', 'seller', 'year', 'make', 'model', 'trim', 'body style',
                    'engine', 'engine displacement', 'engine cylinders', 'transmission', 'wheel_drive', 'ChromeStyleID',
                    'interior_color', 'colour', 'inventory type', 'mileage', 'registration province', 'postal code',
                    'CurrentHighBid', 'buy price', 'auction end date', 'total_damages', 'page url', 'image url',  'SellerAnnouncements',
                    'Reserved 1',  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,
                    40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,
                    53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,
                    66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,
                    79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,
                    92,  93,  94,  95,  96,  97,  98,  99, 100, 'img_url', 'Prior Paint', 'Seller Type', 'Lot number',
                   'run_no', 'lane', 'auction_location', 'Is Run list vehicle', 'ls Live Block vehicle', 'ls DealerBlock vehicle',
                   'vehicle type', 'odo unit', 'sale type', 'run_date', 'frame_damage_indicator', 'Is Reserved',
                   'Vehicle Listing Category', 'grade', 'Processing Auction Org ID', 'Is AutoGrade', 'rl_lb_listing_category',
                   'year_2', 'make_2', 'model_2', 'trim_2', 'province', 'tire', 'inspection date', 
                   'Inspection Company', 'damage_notes', 'inspection_comments', 'Iteration', 'n-Transit Indicator',
                   'Reserved 2', 'Reserved 3' ]
    
    cols = data.columns.tolist()
    end = cols[100:]
    start = cols[0:29]
    mid = cols[29:100]
    new_cols = start + end + mid
    data = data[new_cols]
    return data

def update_DB(inc_file, full_file):
    data = get_dataframe(full_file)
    inc_data = get_dataframe(inc_file)
    new_data = pd.concat([data, inc_data], ignore_index=True)
    new_data.drop_duplicates(subset=['vin'], keep='last', inplace=True)
    new_data.drop(index=new_data.index[new_data['status'] == 'Removed'], axis=0, inplace=True)
    
    high_value = ['BACK-UP CAMERA',
                'BLUETOOTH CONNECTIVITY',
                'HEATED SEATS - DRIVER AND PASSENGER',
                'MEMORY SEAT',
                'NAVIGATION SYSTEM',
                'NAVIGATION W/  HARD DRIVE',
                'PANORAMA ROOF',
                'POWER REAR HATCH',
                'SATELLITE RADIO SIRIUS',
                'VOICE COMMAND/ RECOGNITION',
                'COOLED SEATES',
                'POWER REAR HATCH',
                'NAVIGATION W/ MEDIA CARD',
                'DRIVE TRAIN - ALL WHEEL',
                'LEATHER',
                'DVD',
                'POWER MOONROOF',
                'SEATBACK MONITORS',
                'VOCAL ASSIST TELEMATICS',
                'REAR AIR CONDITIONING',
                'HD RADIO',
                'OVERHEAD MONITORS',
                'ONSTAR',
                '5TH WHEEL TOWING PACKAGE',
                '3RD ROW SEATING',
                'FOLD-AWAY SEATING',
                'ENTERTAINMENT SYSTEM REMOTE']
    
    options = new_data[[30,  31,  32,  33,  34,  35,  36,  37,  38,  39,
                        40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,
                        53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,
                        66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,
                        79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,
                        92,  93,  94,  95,  96,  97,  98,  99, 100]]
    
    more = new_data[['damage_notes', 'inspection_comments', 'frame_damage_indicator', 'rl_lb_listing_category', 'tire']]
    options = options.to_json(orient='index')
    options = json.loads(options)
    more = more.to_json(orient='index')
    more = json.loads(more)
#    new_data.drop(columns=['damage notes', 'Inspection Comments', 'Frame Damage Indicator', 'RL/LB Listing Category', 'tire',
#                        30,  31,  32,  33,  34,  35,  36,  37,  38,  39,
#                        40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,
#                        53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,
#                        66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,
#                        79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,
#                        92,  93,  94,  95,  96,  97,  98,  99, 100, 'Reserved 1', 'Reserved 2', 'Reserved 3'], inplace=True)
    
    new_data['run_no'] = new_data['run_no'].map(int)
    new_data['run_date'] = new_data['run_date'].map(str)
    #new_data['mileage'] = new_data['mileage'].map(str) +' '+new_data['odo unit'].map(str)
    new_data['run_no'] = new_data['Lot number'].map(str) +'-'+ new_data['run_no'].map(str)
    
    short_data = new_data[['adesa_id', 'vin', 'year', 'make', 'model', 'trim',
                           'engine', 'transmission', 'wheel_drive', 'interior_color', 'colour',
                           'mileage', 'odo unit', 'total_damages', 'img_url', 'run_no', 'lane',
                           'auction_location', 'run_date', 'grade']]
    short_data['extra'] = ''
    #short_data['MMR'] = ''
    #count = 0
    
    today = datetime.date.today()
    wednesday = today + datetime.timedelta( (2-today.weekday()) % 7 )
    wednesday = str(wednesday)
    thursday = today + datetime.timedelta( (3-today.weekday()) % 7 )
    thursday = str(thursday)
    short_data = short_data[((short_data['auction_location'] == 'ADESA Toronto') |
                            (short_data['auction_location'] == 'ADESA Ottawa') |
                            (short_data['auction_location'] == 'ADESA Montreal')) & 
                            ((short_data['run_date'] == wednesday) | (short_data['run_date'] == thursday))]
    
    
    for idx, row in short_data.iterrows():
        temp = {k: v for k, v in options[str(idx)].items() if v is not None}
        temp = list(temp.values())
        more[str(idx)]['options'] = temp
        short_data.at[idx, 'extra'] = more[str(idx)]
#        
#        if pd.isna(row['trim']) == True:
#            row['trim'] = 'NONE'
#        if (np.isnan(row['grade'])) or (row['grade'] == 0):
#            row['grade'] = 4
#        mileage = int(row['mileage']*0.621371)
#        mmr_values = get_mmr(row['vin'], mileage, row['grade'], row['trim'])
#        short_data.at[idx, 'MMR'] = mmr_values
#        
#        if count == 10:
#            break
#        count = count+1
#        
#    short_data['mileage'] = short_data['mileage'].map(str) +' '+short_data['odo unit'].map(str)
#    short_data.drop(columns=['odo unit'], inplace=True)
    
    return short_data


def main():
    inc_file, full_file, flag = get_latest_file()
    if (flag == 1):
        data = update_DB(inc_file, full_file)
        data['human_valuation'] = "0"
        data['timestamp'] = str(datetime.datetime.now().timestamp())
        temp = {"data": []}
        data['check'] = json.dumps(temp)
        #data = data.astype(str)
        return data
    return 0
    
