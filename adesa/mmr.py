# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 11:27:47 2018

@author: Visitor
"""

import pandas as pd
import requests
import numpy as np
import math
import json
from currency_conversion import get_conversion

url = "https://api.manheim.com/oauth2/token.oauth2"

payload = "grant_type=client_credentials"
headers = {
    'authorization': "Basic eTZqdDh2Nnc1MmJrZzQyMm40a3A5Mzd0OnVRRXBEZmJEanI=",
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'Postman-Token': "026cd8be-a3ba-4517-ba82-633f2c7f1fdd"
}

response = requests.request("POST", url, data=payload, headers=headers)

token = ''

for val in response.json().values():
    token = token+' '+val
token = token[1:]


def get_mmr(vin, odo, grade, trim, is_array=0):
    
    if (len(trim) == 0):
        trim = 'NONE'
    odo = int(odo)
    if (odo == 0):
        odo = 1
    flag = 0
    if (len(str(grade)) == 0):
        grade = 4.0
        flag = 1
    else: 
        grade = float(grade)


    grade = int(grade * 10)

    # print('mmrVehicle', vin,odo,grade,trim)
    # print('newGrade', grade)
    url = "https://api.manheim.com/valuations/vin/"+vin+"?country=US&odometer=" + \
        str(odo)+"&region=ne&grade=" + str(grade) + \
        "&include=retail,historical,forecast"
    payload = ""
    headers = {
        'cache-control': "no-cache",
        'authorization': token
    }

    response = requests.request("GET", url, data=payload, headers=headers)
    if (response.status_code == 404):
        print('404 error', response.text)
        vehicleObject = {
                    "MMR":"0", 
                    "MID":"0", 
                    "transactions":"0", 
                    "suggestedPrice":"0", 
                    "suggestedPriceCAD":"0", 
                    "trim":"0"
                }
        json_data = json.dumps(vehicleObject)
        single_list = {}
        if is_array == 0:
            single_list[0] = vehicleObject
            return single_list
        else:
        # print(type(json_data))
            return vehicleObject

    # print(response.status_code)
    carList = response.json()
    # print('response',response.text)
    # print('carlist',carList)
    # print(carList['message'])

    try:

        all_cars = carList['items']

        if (carList['count'] > 1) & (trim == 'NONE'):
            temp_data = {}
            count = 0
            for i in all_cars:
                #print(i['adjustedPricing']['wholesale']['average'])
                mmr_by_trim = get_mmr(vin, odo, grade/10.0, i['description']['trim'], 1)
                #temp_data.append(mmr_by_trim)
                temp_data[count] = mmr_by_trim
                count = count+1
            return temp_data
            # return ','.join(str(s) for s in temp_data)
        elif carList['count'] > 1:
            count_flag = 0
            for i in all_cars:
                temp = i['description']['trim']
                if temp.lower().endswith(trim.lower()):
                    carList = i
                    count_flag = 1
                elif trim.lower() in temp.lower():
                    carList = i
                    count_flag = 1
            if count_flag == 0:
                temp_data = {}
                count = 0
                for i in all_cars:
                    mmr_by_trim = get_mmr(vin, odo, grade/10.0, i['description']['trim'], 1)
                    #temp_data.append(mmr_by_trim)
                    temp_data[count] = mmr_by_trim
                    count = count+1
                return temp_data
        else:
            carList = carList['items'][0]

        car_id = carList['href']
        start = car_id.find('id/') + 3
        end = car_id.find('?')
        car_id = car_id[start:end]
        # print(carList['adjustedPricing']['wholesale']['average'])

        url2 = "https://api.manheim.com/valuation-samples/id/"+car_id+"?country=US&region=NE&limit=100"
        response2 = requests.request(
            "GET", url2, data=payload, headers=headers)

        car_samples = response2.json()
        car_samples = car_samples['items']
        car_count = len(car_samples)
        total_miles = []
        total_price = []
        total_grade = []
        for i in car_samples:
            try:
                total_price.append(i['purchasePrice'])
                total_miles.append(i['vehicleDetails']['odometer'])
            except:
                total_miles.append(odo)
            try:
                total_grade.append(int(i['vehicleDetails']['grade']))
            except:
                total_grade.append(grade)

        avg_price = np.median(total_price)
        avg_miles = np.mean(total_miles)
        avg_grade = np.mean(total_grade)
        
        if np.isnan(avg_price):
            avg_price = carList['adjustedPricing']['wholesale']['average']
            avg_grade = grade
            avg_miles = odo
            

        cost_miles = avg_price / avg_miles
        cost_grade = avg_price/avg_grade

        car_price = avg_price

        if (odo - avg_miles > 0):
            car_price = car_price - \
                ((math.log(odo, avg_miles))*(odo-avg_miles)*0.1)
        else:
            car_price = car_price - \
                ((math.log(avg_miles, odo))*(odo-avg_miles)*0.1)

        if(grade - avg_grade > 0):
            car_price = car_price + \
                ((math.log((grade), avg_grade))*(grade-avg_grade))
        else:
            car_price = car_price + \
                ((math.log(avg_grade, grade))*(grade-avg_grade))

        if car_price < 0:
            car_price = 0

        current_rate = get_conversion()
        car_price_cad = int(round(car_price*current_rate, -2))
        car_price = int(round(car_price, -2))
        expenses = 2850
        car_price_cad = car_price_cad - expenses
        if vin[0].isalpha():
           car_price_cad = car_price_cad- (car_price_cad*0.10)
        # print("Avg Price in USD: ", avg_price, "Our MMR in USD: ",
        #   car_price, "Our MMR in CAD: ", car_price*current_rate)
        if car_price <= 0:
            car_price = 0
            car_price_cad = 0
            
        vehicleObject = {
            "MMR":str(carList['adjustedPricing']['wholesale']['average']), 
            "MID":str(car_id), 
            "transactions":str(car_count), 
            "suggestedPrice":str(car_price), 
            "suggestedPriceCAD":str(car_price_cad), 
            "trim":str(trim)
        }
        json_data = json.dumps(vehicleObject)
        
        single_list = {}
        if is_array == 0:
            #single_list.append(json_data)
            single_list[0] = vehicleObject
            return single_list
        else:
        # print(type(json_data))
            return vehicleObject
        # return(','.join(str(s) for s in [carList['adjustedPricing']['wholesale']['average'], car_id, car_count, car_price, car_price_cad, trim]))
    except Exception as e:
        print('mmr exception:', e, vin, odo, grade, trim, flag)
        print('*******************************************************************************************')
        vehicleObject = {
            "MMR":"0", 
            "MID":"0", 
            "transactions":"0", 
            "suggestedPrice":"0", 
            "suggestedPriceCAD":"0", 
            "trim":"0"
        }
        json_data = json.dumps(vehicleObject)
        single_list = {}
        if is_array == 0:
            single_list[0] = vehicleObject
            return single_list
        else:
        # print(type(json_data))
            return vehicleObject

# u = mmr('1FTEX1C88AFD13465', 73039.69816, 4.5, '')
# print(type(u),u)

#vin = "3VWG17AU8JM285662" #2LMTJ8KR2GBL40991"
#odo = 44119
#odo = int(odo*0.621371)
#grade = 45
#### #color = 'BLACK'
#trim = ""
###
#print(get_mmr(vin, odo, grade, trim))