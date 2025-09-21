import requests
import pandas as pd
import json
from io import BytesIO
from typing import List
from contracts.schema import GenericSchema

class APICollector:
    def __init__(self, schema):
        self._schema = schema
        self._aws = None
        self._buffer = None
        return
    
    def start(self, param):
        response = self.getData(param)
        response = self.extractData(response)

        return self.transformDf(response)
        
    def getData(self, param):
        response = None

        if param > 1:
            response = requests.get(f'http://127.0.0.1:8000/shoppings_generate/{param}').json()
        else:
            response = [requests.get(f'http://127.0.0.1:8000/shopping_generate').json()]

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
    
    def transformDf(self, response):
        df = pd.DataFrame(response)
        return df
    
    def convertToParquet(self, df):
        '''
        BytesIO = >Evita a escrita e leitura de arquivos no disco (HD/SSD), 
        tratando todo o processo em memória.
        '''
        self._buffer = BytesIO()
        try:
            df.to_parquet(self._buffer, index=False)
            return self._buffer
        except:
            print("Erro ao transformar o DF em parquet")