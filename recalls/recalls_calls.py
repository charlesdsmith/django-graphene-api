import requests
import json

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

