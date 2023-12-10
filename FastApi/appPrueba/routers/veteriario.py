from models.veterinario import Veterinario as VeterinarioModel
from fastapi import APIRouter
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

@veterinarioRouter.get("/veterinario",tags=['ver'],response_model=List[Veterinario],status_code=200)
def getVeterinario() -> List[Veterinario]:
    db = Session()
    result = db.query(VeterinarioModel).all()
    return jsonable_encoder(result)

@veterinarioRouter.post("/veterinario",tags=['Crear'],response_model=dict,status_code=202)
def crearVeterinario(veterinario: Veterinario):
    db = Session()
    newVeterinario = VeterinarioModel(**veterinario.model_dump())
    db.add(newVeterinario)
    db.commit()
    return JSONResponse(content={"message":"VeterinarioCreado"})