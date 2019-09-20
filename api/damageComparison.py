# graphql call to retrieve all records from damage comparisons table

# first get all he records from the table
import json
import requests

def getAllDamageComparisons():

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

    #response = requests.post("http://localhost:3000/graphql", headers=headers, data=data)
    response2 = requests.post("https://gsm-django.herokuapp.com/graphqlui", headers=headers, data=data)
    #print(response.text)

    #print(response.status_code)
    print(response2.content)
    return response2


def updateDamageComparisons(id, carfax):

    headers = {
        'Authorization': 'Bearer jAL8mDIwpm7Pqk7BUtelsgW3jIFUkO',
        "Content-Type": "application/json",

    }

    data = {
        "query": """mutation updateDamage($id:String!, $carfax:String!){
  updateDamageComparison(args:{id:$id, carfax:$carfax}){
      ok
      response
         }
    }""",
        "variables": {"id": "%d" % id, "carfax": "%s" % carfax},
    }

    data = json.dumps(data)
    #response = requests.post("http://localhost:3000/graphql", headers=headers, data=data)
    response2 = requests.post("https://gsm-django.herokuapp.com/graphqlui", headers=headers, data=data)

    print(response2.content)
    return response2


if __name__ == '__main__':
    #getAllDamageComparisons()
    updateDamageComparisons(2, "test_carfax")