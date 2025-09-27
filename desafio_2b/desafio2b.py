from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["cars_db"]
cars_collection = db["cars"]

@app.post("/cars")
def create_car(marca: str, modelo: str, ano: int, preco: float, ar_condicionado: bool):
    new_car = {
        "marca": marca,
        "modelo": modelo,
        "ano": ano,
        "preco": preco,
        "ar_condicionado": ar_condicionado
    }
    result = cars_collection.insert_one(new_car)
    return {"id": str(result.inserted_id), "message": "Carro criado com sucesso"}

@app.get("/cars")
def get_cars():
    cars = []
    for car in cars_collection.find():
        car["_id"] = str(car["_id"])
        cars.append(car)
    return {"cars": cars}

@app.put("/cars/{car_id}")
def update_car(car_id: str, marca: str, modelo: str, ano: int, preco: float, ar_condicionado: bool):
    update_data = {
        "marca": marca,
        "modelo": modelo,
        "ano": ano,
        "preco": preco,
        "ar_condicionado": ar_condicionado
    }
    result = cars_collection.update_one({"_id": ObjectId(car_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    return {"message": f"Carro {car_id} atualizado com sucesso"}

@app.delete("/cars/{car_id}")
def delete_car(car_id: str):
    result = cars_collection.delete_one({"_id": ObjectId(car_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    return {"message": f"Carro {car_id} excluído com sucesso"}
