# make calls to /graphql here

import json
import requests

def get_graphql(query):

    response = requests.get('http://localhost:8000/graphql?query=%s' % query)
    return response.text


def post_graphql(query=None):

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "query": """{adesaRunlist(vin:"1GBE5C1295F519873") {
    vin
    MID
  }
}""",
        }

    data1 = {
        "query": """mutation{
            createCarfax(carfaxInfo:{vin:"graphqltest1"}){
                carfax{
                vin
                accident
                    }
                    }
                    }""",
    }

    data1 = json.dumps(data1)

    response = requests.post("http://localhost:8000/graphql", headers=headers, data=data1)
    print(response.text)

    return response.text

if __name__ == "__main__":
    post_graphql()

    '''print(get_graphql("""query getCarFaxByRundate {
  carfax(runDate:"11-18-2018"){
    vin
  }
}"""))'''


