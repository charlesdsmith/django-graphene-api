# make calls to /graphql here

import json
import requests

def get_graphql(query):

    response = requests.get('http://localhost:8000/graphql?query=%s' % query)
    return response.text


if __name__ == "__main__":
    print(get_graphql("""query getOneCarFax {
  allCarfaxObjects{
    vin
    structuralDamage
    
  }
  findRecall: recalls(runDate:"11-28-2018"){
    vin
    make
  }
}"""))

