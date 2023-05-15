from fastapi import FastAPI
from routes.estado import estado
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uuid
from typing import Union
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from os import getcwd
from ia.svm import Modelo
app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(estado)
@app.post("/upload")
async def upload_file(file:UploadFile = File(...)):
    nuevoNombre = str(uuid.uuid4())+".jpg"
    with open(getcwd() +"/Dataset_val/"+ nuevoNombre, "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()
        imagen= getcwd() +"/Dataset_val/"+ nuevoNombre
        respuestaImagen = Modelo(imagen)
        if(respuestaImagen == "Mild_Demented"):
            return "Demencia leve"
        elif(respuestaImagen == "Moderate_Demented"):
            return "Demencia moderada"
        elif(respuestaImagen == "Very_Mild_Demented"):
            return "Demencia muy leve"
        else:
            return "No demente"
app.mount("/", StaticFiles(directory="public"))