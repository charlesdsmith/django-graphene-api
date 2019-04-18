# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 12:38:06 2019

@author: Visitor
"""

from sqlalchemy import create_engine
import sqlalchemy as db
import pandas as pd
from adesa_run_list import main
import numpy as np
from mmr import get_mmr
import datetime
import json

def del_all_entries():
    engine = create_engine('postgres://dtgezubozbdpyd:fde75e2578c7e4b9fa527d3207abd8bb0b3cff5ae542ec3bc108edcb7fc3bcbc@ec2-54-204-14-96.compute-1.amazonaws.com:5432/d757trntif6574')
    connection = engine.connect()
    metadata = db.MetaData()
    metadata.reflect(engine)
    delete_entry = db.delete('api_getadesarunlist')
    results = connection.execute(delete_entry)
    connection.close()

data = main()

if (type(data) != int):
    engine = create_engine('postgres://dtgezubozbdpyd:fde75e2578c7e4b9fa527d3207abd8bb0b3cff5ae542ec3bc108edcb7fc3bcbc@ec2-54-204-14-96.compute-1.amazonaws.com:5432/d757trntif6574')
    
    connection = engine.connect()
    
    metadata = db.MetaData()
    #census = db.Table('census', metadata, autoload=True, autoload_with=engine)
    metadata.reflect(engine)
    #
    #for table in metadata.tables.values():
    #    print(table.name)
    
    try:
        run_list = db.Table('api_getadesarunlist', metadata, autoload=True, autoload_with=engine)
        
        print(run_list.columns.keys())
        print(run_list.columns.items())
        
        #print(metadata.tables['api_getadesarunlist'].columns.keys())
        
        query = db.select([run_list])
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        connection.close()
        df = pd.DataFrame(ResultSet, columns=['id', 'adesa_id', 'vin', 'year', 'make', 'model', 'trim', 'engine',
                                           'transmission', 'wheel_drive', 'interior_color', 'colour', 'mileage',
                                           'total_damages', 'img_url', 'run_no', 'lane', 'auction_location',
                                           'run_date', 'grade', 'extra', 'human_valuation', 'timestamp', 'check',
                                           'MMR'])
    
    except:
        df = pd.DataFrame(columns=['adesa_id', 'vin', 'year', 'make', 'model', 'trim', 'engine',
                                           'transmission', 'wheel_drive', 'interior_color', 'colour', 'mileage',
                                           'total_damages', 'img_url', 'run_no', 'lane', 'auction_location',
                                           'run_date', 'grade', 'extra', 'human_valuation', 'timestamp', 'check',
                                           'MMR']) #to reset the database
    
    
    already_mmr = df[['vin', 'MMR', 'check']][df['vin'].isin(data['vin'])]
    temp = {"values": []}
    data['MMR'] = json.dumps(temp)
    count = 0
    for idx, row in data.iterrows():
        
        check_mmr = already_mmr[already_mmr['vin'] == row['vin']]
        if((len(check_mmr) != 0)):
            if (check_mmr['MMR'].values[0] != json.dumps(temp)) and (check_mmr['MMR'].values[0] != ''):
                data.at[idx, 'MMR'] = check_mmr['MMR'].values[0]
                data.at[idx, 'check'] = check_mmr['check'].values[0]
                print('------------------------------------------------')
            else:
                if pd.isna(row['trim']) == True:
                    row['trim'] = 'NONE'
                if (pd.isna(row['grade'])) or (row['grade'] == 0):
                    row['grade'] = 4
                mileage = int(row['mileage']*0.621371)
                mmr_values = get_mmr(row['vin'], mileage, row['grade'], row['trim'])
                json_array = {}
                json_array["values"] = mmr_values
                data.at[idx, 'MMR'] = json.dumps(json_array)
                count = count+1
        else:
            if pd.isna(row['trim']) == True:
                row['trim'] = 'NONE'
            if (pd.isna(row['grade'])) or (row['grade'] == 0):
                row['grade'] = 4
            mileage = int(row['mileage']*0.621371)
            mmr_values = get_mmr(row['vin'], mileage, row['grade'], row['trim'])
            json_array = {}
            json_array["values"] = mmr_values
            data.at[idx, 'MMR'] = json.dumps(json_array)
            count = count+1
        if count == 10:
            break
        
    data['mileage'] = data['mileage'].map(str) +' '+data['odo unit'].map(str)
    data.drop(columns=['odo unit'], inplace=True)
    data = data.astype(str)

    #data['MMR'] = data['MMR'].str.replace('[', '{')
    #data['MMR'] = data['MMR'].str.replace(']', '}')
    #data['MMR'] = data['MMR'].str.replace('None', '0')    
    
    print('Start: ', datetime.datetime.now().time())
    data1 = data[0:30]
    data1.to_sql('api_getadesarunlist', engine, if_exists='replace', index=True, index_label='id', 
                dtype ={'MMR':db.types.JSON, 'extra': db.types.JSON, 'check': db.types.JSON})
    print('End: ', datetime.datetime.now().time())