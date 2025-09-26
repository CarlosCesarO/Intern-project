from fastapi import FastAPI, HTTPException
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
    host="localhost",
    database="cars_db",
    user="postgres",
    password="admin"
)

cursor = conn.cursor()

@app.post("/cars")
def create_car(marca: str, modelo: str, ano: int, preco: float, ar_condicionado: bool):
    cursor.execute(
        "INSERT INTO cars (marca, modelo, ano, preco, ar_condicionado) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (marca, modelo, ano, preco, ar_condicionado)
    )
    new_id = cursor.fetchone()[0]
    conn.commit()
    return {"id": new_id, "message": "Carro criado com sucesso"}

@app.get("/cars")
def get_cars():
    cursor.execute("SELECT * FROM cars")
    rows = cursor.fetchall()
    return {"cars": rows}

@app.put("/cars/{car_id}")
def update_car(car_id: int, marca: str, modelo: str, ano: int, preco: float, ar_condicionado: bool):
    cursor.execute(
        "UPDATE cars SET marca = %s, modelo = %s, ano = %s, preco = %s, ar_condicionado = %s WHERE id = %s RETURNING id",
        (marca, modelo, ano, preco, ar_condicionado, car_id)
    )
    updated = cursor.fetchone()
    conn.commit()
    if not updated:
        raise HTTPException(status_code=404, detail="Erro ao atualizar o carro")
    return {"message": f"Carro {car_id} atualizado com sucesso"}

@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    cursor.execute("DELETE FROM cars WHERE id = %s RETURNING id", (car_id,))
    deleted = cursor.fetchone()
    conn.commit()
    if not deleted:
        raise HTTPException(status_code=404, detail="Erro ao excluir o carro")
    return {"message": f"Carro {car_id} excluído com sucesso"}


