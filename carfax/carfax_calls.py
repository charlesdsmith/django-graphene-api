#  this file will POST carfax testrmation the our Django API

import requests
import json

test = ['VHSRLAFKStest', 'No Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'some Recalls Reported', '12-01-2018']
# MAKE SURE TO USE "application/json" IN "Content-Type"

def authorize():

    client_id = '8TqPw5f2WgdNiY8qFZ97oh7wDQhVNnuuKyJ30dUd'
    client_secret = 'F2MCmGC3EapJBWH7c446qpsQpj0fxYde9MKRXL8CsH514uN1CbMh654WrT8ZqqfrsZnsitsNnI4MeZEzmZu4t2at7ViEWDbELKzqUHeJWevyrpoeInSoJpEARxYvPs9R'


    data = {
        'grant_type': 'password',
        'username': 'charlessmith',
        'password': 'gsmcharles',
    }


    response = requests.post('http://localhost:8000/o/token/', data=data, auth=(client_id, client_secret))

    return response.text

def post_carfax(test):

    # example of test parameter
    # ['No Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'No Recalls Reported']


    '''cookies = {
        'PGADMIN_LANGUAGE': 'en',
        'PGADMIN_KEY': '5edc9e0d-8f36-4e63-8e9e-694ae3d9f9a9',
        'csrftoken': 'iHH5pujGsroVpiwBR4qpKuhVovCyWRauddwiCZaxnxxHzANt7rNTGhc4fKbjaqEV',
        'pga4_session': 'b395d851-2905-4dd9-aa83-7d27af6f0557!3ovpR7+Zw4XwrrRD0A9Qg5NYExs=',
        'tabstyle': 'raw-tab',
    }'''

    cookies = {
        'csrftoken': 'LQFPzk47nbZB0IbZMSolMZf6zLzl9KWeUHMBidLLBZiPDhloukrBxCnMBqN7eyYe',
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer TmI5EngNb8eUkR4IrifzdmkRvjcrIf',
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
    response = requests.post('http://127.0.0.1:8000/api/v1/post_carfax/', headers=headers, data=data)
    # print(json.dumps(response.json))
    return response.text


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
        'Authorization': 'Bearer TmI5EngNb8eUkR4IrifzdmkRvjcrIf',
    }

    params = {
        'vin': "VHSRLAFKSF"
    }

    # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
    response = requests.get('http://127.0.0.1:8000/api/v1/get_carfax/VHSRLAFKSF', headers=headers)
    # print(json.dumps(response.json))
    return response.text

def get_all_carfax():

    headers = {
        'Authorization': 'Bearer TmI5EngNb8eUkR4IrifzdmkRvjcrIf',
    }

    # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
    response = requests.get('http://127.0.0.1:8000/api/v1/get_carfax/', headers=headers)
    # print(json.dumps(response.json))
    return response.text

if __name__ == '__main__':
    print(post_carfax(test))
    #print(authorize())
    #print(get_api_root())
    #print(get_all_carfax())
    #print(get_one_carfax())
