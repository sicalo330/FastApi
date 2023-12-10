from models.paciente import Paciente as PacienteModel
from fastapi import APIRouter
from typing import Optional, List
from pydantic import BaseModel, Field
from config.database import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

pacienteRouter = APIRouter()

class PacienteBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=40)
    apellido: str = Field(min_length=1, max_length=20)
    edad: int = Field(ge=1, le=116)
    tipoSangre: str = Field(min_length=1, max_length=3)

class PacienteCreate(PacienteBase):
    veterinarioId: int

class Paciente(PacienteBase):
    id: Optional[int] = None
    veterinario: Optional[int] = None

@pacienteRouter.get("/pacientes", tags=['Ver'], response_model=List[Paciente], status_code=200)
def getPaciente() -> List[Paciente]:
    db = Session()
    result = db.query(PacienteModel).all()
    return jsonable_encoder(result)

@pacienteRouter.post("/pacientes", tags=['Crear'], response_model=dict, status_code=201)
def crearPaciente(paciente: PacienteCreate):
    db = Session()
    newPaciente = PacienteModel(**paciente.dict())
    db.add(newPaciente)
    db.commit()
    return JSONResponse(content={"message": "Paciente creado"})
