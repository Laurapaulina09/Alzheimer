from sqlalchemy import Table, Column, Integer, String
from config.db import meta

Tipos = Table("tipos", meta, 
    Column("id", Integer, primary_key=True), 
    Column("nombre", String(50))
)
