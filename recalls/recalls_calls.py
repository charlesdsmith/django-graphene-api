import requests
import json

#test = ['VHSRLAFKStest', 'No Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'some Recalls Reported', '12-01-2018']

def authorize():

    client_id = '8TqPw5f2WgdNiY8qFZ97oh7wDQhVNnuuKyJ30dUd'
    client_secret = 'F2MCmGC3EapJBWH7c446qpsQpj0fxYde9MKRXL8CsH514uN1CbMh654WrT8ZqqfrsZnsitsNnI4MeZEzmZu4t2at7ViEWDbELKzqUHeJWevyrpoeInSoJpEARxYvPs9R'

    local_client_id = '8TqPw5f2WgdNiY8qFZ97oh7wDQhVNnuuKyJ30dUd'
    local_client_secret = 'F2MCmGC3EapJBWH7c446qpsQpj0fxYde9MKRXL8CsH514uN1CbMh654WrT8ZqqfrsZnsitsNnI4MeZEzmZu4t2at7ViEWDbELKzqUHeJWevyrpoeInSoJpEARxYvPs9R'


    data = {
        'grant_type': 'password',
        'username': 'charlessmith',
        'password': 'gsmcharles',
    }


    response = requests.post('http://localhost:8000/o/token/', data=data, auth=(local_client_id, local_client_secret))

    return response.text


def post_recall():
    test = ['GSMTEAM', 'SOME Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'some Recalls Reported', '12-01-2018']


    # example of test parameter
    # ['No Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'No Recalls Reported']


    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer hVe2xZpR0PxBoqS12k6RiNX9Dw661Q',
    }

    data = {
        "vin": test[0],
        "make": "FORD",
        "recalls": "No recalls",
        "run_date": "11-28-2018"
    }

    data = json.dumps(data)

    try:
        # response = requests.post('http://localhost:8000/api/v1/recalls/', data=data, headers=headers)
        heroku_response = requests.post('https://gsm-django.herokuapp.com/api/v1/recalls/', data=data, headers=headers)
        # print(json.dumps(response.json))
        return heroku_response.text

    except Exception as e:
        print(e)

def get_one_recall():

    headers = {
        'Authorization': 'Bearer hVe2xZpR0PxBoqS12k6RiNX9Dw661Q',
    }

    params = {
        'vin': "VHSRLAFKSF"
    }

    # response = requests.post('http://gsm-django.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
    try:
        response = requests.get('http://localhost:8000/api/v1/recalls/GSMTEAM/', headers=headers)
        # print(json.dumps(response.json))

    except Exception as e:
        print(e)

    return response.text

def get_all_recalls():

    headers = {
        'Authorization': 'Bearer hVe2xZpR0PxBoqS12k6RiNX9Dw661Q',
    }

    # response = requests.post('http://gsm-django.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
    try:
        # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
        response = requests.get('http://127.0.0.1:8000/api/v1/recalls/', headers=headers)
        # print(json.dumps(response.json))

    except Exception as e:
        print(e)

    return response.text

def get_by_rundate():

    headers = {
        'Authorization': 'Bearer hVe2xZpR0PxBoqS12k6RiNX9Dw661Q',
    }

    # response = requests.post('http://gsm-django.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
    try:
        # response = requests.post('http://gsm-django.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)
        response = requests.get('http://127.0.0.1:8000/api/v1/recalls/retrieve_by_rundate/11-28-2018/', headers=headers)
        # print(json.dumps(response.json))

    except Exception as e:
        print(e)

    return response.text

def bulk_post():
    # create multiple resources
    # [{"field":"value","field2":"value2"}]

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ctivvp7NUHGav6QGYxW7kNGfHSNbaf',
    }

    data = [{
        "vin": 'TEST1',
        "make": "FORD",
        "recalls": "No recalls",
        "run_date": "11-28-2018"
        },
        {
        "vin": 'TEST1',
        "make": "FORD",
        "recalls": "No recalls",
        "run_date": "11-28-2018"
        }]

    data = json.dumps(data)
    # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)

    try:
        #heroku_response = requests.post('https://gsm-django.herokuapp.com/api/v1/adesa_run_list/', data=data, headers=headers)
        response = requests.post('http://127.0.0.1:8000/api/v1/recalls_bulk_upload/', data=data, headers=headers)
        # print(json.dumps(response.json))
        #print(heroku_response.status_code)
        return response.text
    except Exception as e:

        print(e)

if __name__ == "__main__":
    #print(post_recall())
    #print(authorize())
    #print(get_one_recall())
    #print(get_all_recalls())
    #print(get_by_rundate())
    print(bulk_post())