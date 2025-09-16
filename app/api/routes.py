from fastapi import FastAPI, HTTPException, status
from faker import Faker
from app.config.config import settings
import random
import pandas as pd

app = FastAPI()
fake = Faker()
file = settings.products_list
df = pd.read_csv(file)
df["index"] = range(1, len(df) + 1)
df.set_index("index", inplace=True)


@app.get("/shopping_generate")
async def shopping_generate():
    index = random.randint(1, len(df))
    product = df.iloc[index]
    return {
        "client": fake.name(),
        "creditCar": fake.credit_card_provider(),
        "ean": int(product["EAN"]),
        "product_name": product["Produto"],
        "price": round(float(product["Preço"]) * 1.2, 2),
        "store": 11,
        "dateTime": fake.iso8601(),
        "clientLocation": fake.location_on_land()
    }

@app.get("/shoppings_generate/{number_of_register}")
async def shoppings_generate(number_of_register: int):
    try:
        number_of_register = int(number_of_register)
    
        if(number_of_register < 1):
            raise ValueError

        shopping_list = []
        
        for _ in range(number_of_register):
            shopping = await shopping_generate()
            shopping_list.append(shopping)

        return shopping_list
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The number of registers must be greater than 0",
        )