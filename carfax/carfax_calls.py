#  this file will POST carfax testrmation the our Django API

import requests
import json

test = ['VHSRLAFKStest', 'No Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'some Recalls Reported', '12-01-2018']
# MAKE SURE TO USE "application/json" IN "Content-Type"

# TODO: Figure out why carfax isn't returning 'html' field in GET request
def authorize():

    client_id = 'SF4ndlds1e6H5cAAi8vpxDzQB0zbkslfqiH1CgXb'
    client_secret = 'vznY2auvuqGnTKdaYOA6tqlpASRXU6dEe6V3ZdZblX2RVvQGdh2c1IF6byVpxOafdfqbysthAxeXkTyMI7R5SExvK6MbDEhXaaF4YXg9Wz9GyCXIZ97eCf6VaH8MlTEO'


    data = {
        'grant_type': 'password',
        'username': 'charles',
        'password': 'charles',
    }


    response = requests.post('http://localhost:8000/o/token/', data=data, auth=(client_id, client_secret))
    heroku_response = requests.post('https://gsm-django.herokuapp.com/o/token/', data=data, auth=(client_id, client_secret))

    return heroku_response.text

def post_carfax(test):

    # example of test parameter
    # ['No Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'No Recalls Reported']


    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer wfvkVUtFNDAGmSE5Kojb9pP6PhGMbx',
    }


    data = {
        "vin": test[0],
        "structural_damage": test[2],
        "total_loss": test[1],
        "accident": test[5],
        "airbags": 'charles',
        "odometer": test[4],
        "recalls": test[6],
        'run_date': test[7]
    }

    data = json.dumps(data)
    # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
    try:
        # heroku_response = requests.post('http://localhost:8000/api/v1/post_carfax', data=data, headers=headers)
        response = requests.post('https://gsm-django.herokuapp.com/api/v1/carfax/', data=data, headers=headers)
        # print(json.dumps(response.json))
        return response.text
    except Exception as e:
        print(e)




def get_api_root():

    cookies = {
        'csrftoken': 'LQFPzk47nbZB0IbZMSolMZf6zLzl9KWeUHMBidLLBZiPDhloukrBxCnMBqN7eyYe',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    response = requests.get('http://localhost:8000/api/v1/', headers=headers, cookies=cookies)
    return response.content

def get_one_carfax(vin=None):

    headers = {
        'Authorization': 'Bearer qdKC0g6vn26GRXr2pmGVVeBXbWu8re',
    }

    params = {
        'vin': "VHSRLAFKSF"
    }

    # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
    response = requests.get('http://127.0.0.1:8000/api/v1/carfax/5UXFG43549L225116', headers=headers)
    # print(json.dumps(response.json))
    return response.text

def get_all_carfax():

    headers = {
        'Authorization': 'Bearer qdKC0g6vn26GRXr2pmGVVeBXbWu8re',
    }

    # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
    response = requests.get('http://127.0.0.1:8000/api/v1/carfax/', headers=headers)
    # print(json.dumps(response.json))
    return response.text

def get_by_rundate():

    headers = {
        'Authorization': 'Bearer qdKC0g6vn26GRXr2pmGVVeBXbWu8re',
    }

    # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
    try:
        # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
        response = requests.get('http://127.0.0.1:8000/api/v1/carfax/retrieve_by_rundate/11-18-2018/', headers=headers)
        # print(json.dumps(response.json))

    except Exception as e:
        print(e)

    return response.text

if __name__ == '__main__':
    #print(post_carfax(test))
    #print(authorize())
    #print(get_api_root())
    #print(get_all_carfax())
    print(get_one_carfax())
    #print(get_by_rundate())
