from models.paciente import Paciente as PacienteModel
from fastapi import APIRouter, Depends
from typing import Optional, List
from pydantic import BaseModel, Field
from config.database import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

pacienteRouter = APIRouter()

class Paciente(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=2, max_length=40)
    apellido: str = Field(min_length=1, max_length=20)
    edad: int = Field(ge=1, le=116)
    tipoSangre: str = Field(min_length=1, max_length=2)

@pacienteRouter.get("/pacientes", tags=['Ver'], response_model=List[Paciente], status_code=200)
def getPaciente() -> List[Paciente]:
    db = Session()
    result = db.query(PacienteModel).all()
    return jsonable_encoder(result)

@pacienteRouter.post("/pacientes", tags=['Crear'], response_model=dict, status_code=201)
def crearPaciente(paciente: Paciente):
    db = Session()
    newPaciente = PacienteModel(**paciente.model_dump())
    db.add(newPaciente)
    db.commit()
    return JSONResponse(content={"message": "Paciente creado"})