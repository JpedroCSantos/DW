import requests
from typing import List
from contracts.schema import GenericSchema

class APICollector:
    def __init__(self, schema):
        self._schema = schema
        self._aws = None
        self._buffer = None
        return
    
    def start(self, param):
        reponse = self.getData(param)
        
        return self.extractData(reponse)
    
    def getData(self, param):
        response = None

        if param > 1:
            response = requests.get(f'http://127.0.0.1:8000/shoppings_generate/{param}').json()
        else:
            response = requests.get(f'http://127.0.0.1:8000/shopping_generate').json()

        return response
    
    def extractData(self, response: List[dict]):
        shoppingItems: List[GenericSchema] = []

        for item in response:
            index = {}
            for key, value in self._schema.items():
                if type(item[key]) == value:
                    index[key] = item[key]
                else:
                    index[key] = None                    
            shoppingItems.append(index)

        return shoppingItems
    
    def transformDf():
        return