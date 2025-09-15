from fastapi import FastAPI

app = FastAPI()

@app.get("/gerar_compra")
async def gerar_compra():
    return {
        "client": "Nome",
        "creditCar": "Tipo do Cartão",
        "ean": "Código do Produto",
        "price": "Preço do Produto",
        "store": 11,
        "dateTime": "Data da Compra",
        "clientLocation": "Localização do Cliente"
    }