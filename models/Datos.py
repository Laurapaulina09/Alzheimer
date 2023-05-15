from sqlalchemy import Table, Column, Integer, String
from config.db import meta


Datos = Table("datos", meta, 
    Column("id", Integer, primary_key=True),
    Column("tipo", Integer),
    Column("ruta", String(255))
)