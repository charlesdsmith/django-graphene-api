import requests
import json

test = ['VHSRLAFKStest', 'No Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'some Recalls Reported', '12-01-2018']
# MAKE SURE TO USE "application/json" IN "Content-Type"


def authorize():

    client_id = '4cTTNannIFUGWcFbrl0GyWhlSK4pVoBBDwbGiEmT'
    client_secret = 'ECkqotBupUmcrK3JgrOnw8f8bPFhbWd37Cpi4JWXs3vcJRpgwADaJmqFnk8jKkWggrTKIDY6DIYq9sWDgbKCX0i4BclwEH4cPvJpqdk85mK6Ld9EbVzjtyhBVt8hfSRY'


    data = {
        'grant_type': 'password',
        'username': 'charles',
        'password': 'charles',
    }


    response = requests.post('http://localhost:8080/o/token/', data=data, auth=(client_id, client_secret))
    #heroku_response = requests.post('https://gsm-django.herokuapp.com/o/token/', data=data, auth=(client_id, client_secret))

    return response.text

def post_run_list():

    # example of test parameter
    # ['No Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'No Recalls Reported']


    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer Vl1tcchRnhJcNeIz7ztJdQTrjGp0Qv',
    }

    data = {
        "vin": "123456",
        "img_url": "https://germanstarmotors.slack.com/messages/DE33RNUSHTEST2/",
        "year": "1991",
        "grade": "4",
        "run_date": "11-28-2018",
        "lane": "2"
    }

    data = json.dumps(data)
    # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)

    try:
        heroku_response = requests.post('https://gsm-django.herokuapp.com/api/v1/shopping_list/', data=data, headers=headers)
        #response = requests.post('http://127.0.0.1:8000/api/v1/adesa_run_list/', data=data, headers=headers)
        # print(json.dumps(response.json))
        print(heroku_response.status_code)
        return heroku_response.text
    except Exception as e:

        print(e)

def get_by_rundate():

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer I5RmXX9VBaLvAozrv7EkIQVL9GaEGY',
    }

    try:
        heroku_response = requests.get('https://gsm-django.herokuapp.com/api/v1/adesa_run_list/retrieve_by_rundate/11-28-2018/', headers=headers)
        #response = requests.post('http://127.0.0.1:8000/api/v1/adesa_run_list/', data=data, headers=headers)
        # print(json.dumps(response.json))
        print(heroku_response.status_code)
        return heroku_response.text
    except Exception as e:
        print(e)

def update_runlist():

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer nOyAc2RdHnVGp8dPgf0UBL0fK7dWpL',
    }

    data = {
        "colour": """{"user": "remone"}"""
    }

    data = json.dumps(data)
    try:
        print("here")
        response = requests.patch('http://127.0.0.1:8080/api/v1/adesa_run_list/5UXFG43549L225116/', data=data, headers=headers)
        print(response.text)
        return response.text

    except Exception as e:
        print(e)

if __name__ == "__main__":
    #print(authorize())
    #print(post_run_list())
    #print(get_by_rundate())
    print(update_runlist())


    '''def decorator(func):
        def wrapper(name):
            return "hello {0}".format(func(name))
        return wrapper

    @decorator
    def get_text(name):
        return "this is {0}".format(name)

    my_get_text = decorator(get_text)
    print(my_get_text)
    print(get_text('charles'))'''
