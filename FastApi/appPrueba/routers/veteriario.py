from models.veterinario import Veterinario as VeterinarioModel
from fastapi import APIRouter,Path
from typing import Optional, List
from pydantic import BaseModel, Field
from config.database import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

veterinarioRouter = APIRouter()

class Veterinario(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=1, max_length=40)
    apellido: str = Field(min_length=1,max_length=40)
    edad: int = Field(ge=1,le=116)

@veterinarioRouter.get("/veterinario",tags=['Ver'],response_model=List[Veterinario],status_code=200)
def getVeterinario() -> List[Veterinario]:
    db = Session()
    result = db.query(VeterinarioModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@veterinarioRouter.get("/veterinario/{id}",tags=['Ver'],response_model=Veterinario, status_code=200)
def getVeterinarioId(id:int = Path(ge = 1,le = 2000)):
    db = Session()
    result = db.query(VeterinarioModel).filter(VeterinarioModel.id == id).first()
    response = JSONResponse(content=jsonable_encoder(result),status_code=200)
    if(not result):
        response = JSONResponse(content={"message":"Veterinario no encontrado"}, status_code=404)
    return response

@veterinarioRouter.post("/veterinario",tags=['Crear'],response_model=dict,status_code=202)
def crearVeterinario(veterinario: Veterinario):
    db = Session()
    newVeterinario = VeterinarioModel(**veterinario.model_dump())
    db.add(newVeterinario)
    db.commit()
    return JSONResponse(content={"message":"VeterinarioCreado"})

@veterinarioRouter.put("/veterinario/{id}",tags=["Actualizar"])
def actualizarVeterinario(id:int, veterinario:Veterinario):
    db = Session()
    result = db.query(VeterinarioModel).filter(VeterinarioModel.id == id).first()
    if(not result):
        return JSONResponse(content={"message":"veterinario no encontrado"})

    result.nombre = veterinario.nombre
    result.apellido = veterinario.apellido
    result.edad = veterinario.edad
    db.commit()
    return JSONResponse(content={"message":"Veterinario actualizado"},status_code=200)

@veterinarioRouter.delete("/veterinario/{id}",tags=['Eliminar'],response_model=dict)
def eliminarVeterinario(id:int):
    db = Session()
    result = db.query(VeterinarioModel).filter(VeterinarioModel.id == id).first()
    if(not result):
        return JSONResponse(status_code=404, content={"message":"Veterinario no encontrado"})
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message":"Veterinario eliminado"}, status_code=200)