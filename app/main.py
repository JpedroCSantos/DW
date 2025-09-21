from datasource.api import APICollector
from contracts.schema import ShoppingSchema

apiCollector = APICollector(ShoppingSchema).start(10)
print(apiCollector)