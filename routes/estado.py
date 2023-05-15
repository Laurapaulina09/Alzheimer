from fastapi import APIRouter
import random
from config.db import conn
from models.Tipos import Tipos
from models.Datos import Datos
estado = APIRouter()



@estado.get("/tipos")
def getTipos():
    dat = conn.execute(Tipos.select()).all()
    n = []
    for i in dat:
        n.append({
            "id":i._data[0],
            "nombre":i._data[1]
        })
    return n
    
@estado.get("/datos")
def getDatos():
    dat = conn.execute(Datos.select()).all()
    n = []
    for i in dat:
        n.append({
            "id":i._data[0],
            "tipo":i._data[1],
            "ruta":i._data[2]
        })
    return n

@estado.get("/aleatorio/")
def getDatoAleatorio():
    aleatorio = random.randint(1,6400)
    dat = conn.execute(Datos.select().where(Datos.c.id == aleatorio)).first()
    return {
        "id":dat._data[0],
        "tipo":dat._data[1],
        "ruta":dat._data[2]
    }