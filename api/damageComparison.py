# graphql call to retrieve all records from damage comparisons table

# first get all he records from the table
import json
import requests

def post_graphql(query=None):

    headers = {
        'Authorization': 'Bearer jAL8mDIwpm7Pqk7BUtelsgW3jIFUkO',
        "Content-Type": "application/json",

    }

    data = {
        "query": """query getDamagedCars{
  allDamageComparisonObjects{
      vin
      carfax
         }
    }""",
    }

    data = json.dumps(data)

    response = requests.post("http://localhost:3000/graphql", headers=headers, data=data)
    #response2 = requests.post("https://gsmauctionapp.herokuapp.com/graphql/", headers=headers, data=data)
    #print(response.text)

    #print(response.status_code)
    print(response.content)
    return response
