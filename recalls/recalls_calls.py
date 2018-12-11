import requests
import json

#test = ['VHSRLAFKStest', 'No Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'some Recalls Reported', '12-01-2018']

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


def post_recall():
    test = ['GSMTEAM', 'SOME Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'some Recalls Reported', '12-01-2018']


    # example of test parameter
    # ['No Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'No Recalls Reported']


    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer qdKC0g6vn26GRXr2pmGVVeBXbWu8re',
    }

    data = {
        "vin": test[0],
        "make": "FORD",
        "recalls": "No recalls",
        "run_date": "11-28-2018"
    }

    data = json.dumps(data)

    try:
        response = requests.post('http://localhost:8000/api/v1/recalls/', data=data, headers=headers)
        #heroku_response = requests.post('https://gsm-django.herokuapp.com/api/v1/recalls/', data=data, headers=headers)
        # print(json.dumps(response.json))
        return response.text

    except Exception as e:
        print(e)

def get_one_recall():

    headers = {
        'Authorization': 'Bearer qdKC0g6vn26GRXr2pmGVVeBXbWu8re',
    }

    params = {
        'vin': "VHSRLAFKSF"
    }

    # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
    try:
        response = requests.get('http://localhost:8000/api/v1/recalls/GSMTEAM/', headers=headers)
        # print(json.dumps(response.json))

    except Exception as e:
        print(e)

    return response.text

def get_all_recalls():

    headers = {
        'Authorization': 'Bearer qdKC0g6vn26GRXr2pmGVVeBXbWu8re',
    }

    # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
    try:
        # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
        response = requests.get('http://127.0.0.1:8000/api/v1/recalls/', headers=headers)
        # print(json.dumps(response.json))

    except Exception as e:
        print(e)

    return response.text

def get_by_rundate():

    headers = {
        'Authorization': 'Bearer qdKC0g6vn26GRXr2pmGVVeBXbWu8re',
    }

    # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
    try:
        # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
        response = requests.get('http://127.0.0.1:8000/api/v1/recalls/retrieve_by_rundate/11-28-2018/', headers=headers)
        # print(json.dumps(response.json))

    except Exception as e:
        print(e)

    return response.text


if __name__ == "__main__":
    #print(post_recall())
    #print(authorize())
    #print(get_one_recall())
    #print(get_all_recalls())
    print(get_by_rundate())