from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI(title=
"Demo API CRUD")
# Modelo simple
class Item(BaseModel):
    name: str
    price: float
    quantity: int
# Base de datos en memoria
items = []

# POST: agregar ítem
@app.post("/items/"
, response_model=Item)
def create_item(item: Item):
    items.append(item)
    return item

# GET: listar ítems
@app.get("/items/"
, response_model=list[Item])
def get_items():
    return items

# PUT: actualizar ítem por índice
@app.put("/items/{item_index}"
, response_model=Item)
def update_item(item_index: int, item: Item):
    if item_index < 0 or item_index >= len(items):
        raise HTTPException(status_code=404, detail="Ítem no encontrado")
    items[item_index] = item
    return item

# DELETE: eliminar ítem por índice
@app.delete("/items/{item_index}")
def delete_item(item_index: int):
    if item_index < 0 or item_index >= len(items):
        raise HTTPException(status_code=404, detail="Ítem no encontrado")
    deleted_item = items.pop(item_index)
    return {"msg": "Ítem eliminado","item": deleted_item}

CREATE DATABASE un2;
CREATE TABLE usuarios (id int auto_increment primary key,
nombre varchar(80),
fecha_inicio date,
rut varchar(18)
);

try 
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="un2"
    )
    cur = conexion.cursor()
    for (id,nombre) in cur
        print(f"id {id}, nombre: {nombre}")
    if conexion.is_conected():
        print("Conexion exitosa a la base de datos")
except mysql.connector.Error as e:
    print(f"Error al conectar: {e}")