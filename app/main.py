from datasource.api import APICollector
from contracts.schema import ShoppingSchema
from config.config import settings

apiCollector = APICollector(ShoppingSchema, settings).start(10)
