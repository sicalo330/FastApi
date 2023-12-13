from models.paciente import Paciente as PacienteModel
from fastapi import APIRouter,Path
from typing import Optional, List
from pydantic import BaseModel, Field
from config.database import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload
pacienteRouter = APIRouter()

class PacienteBase(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=2, max_length=40)
    apellido: str = Field(min_length=1, max_length=20)
    edad: int = Field(ge=1, le=116)
    tipoSangre: str = Field(min_length=1, max_length=3)
    veterinarioId: Optional[int] = None

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase):
    id: Optional[int] = None
    veterinario: Optional[int] = None

#Obtendrá todos los pacientes que están en la base de datos
@pacienteRouter.get("/pacientes", tags=['VerPaciente'], response_model=List[Paciente], status_code=200)
def getPaciente() -> List[Paciente]:
    db = Session()
    result = db.query(PacienteModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Obtendrá un paciente tomando una id como parámetro
@pacienteRouter.get("/pacientes/{id}",tags=["VerPaciente"],response_model=Paciente, status_code=200)
def getPacienteId(id:int = Path(ge=1,le=2000)):
    db = Session()
    result = db.query(PacienteModel).filter(PacienteModel.id == id).options(joinedload(PacienteModel.veterinario)).first()
    response = JSONResponse(content=jsonable_encoder(result),status_code=200)
    if (not result):
        response = JSONResponse(content={"message":"Paciente no fue encontrado"},status_code=404)
    return response


@pacienteRouter.post("/pacientes", tags=['CrearPaciente'], response_model=Paciente, status_code=201)
def crearPaciente(paciente: PacienteCreate):
    db = Session()
    newPaciente = PacienteModel(**paciente.model_dump())
    db.add(newPaciente)
    db.commit()
    return JSONResponse(content={"message": "Paciente creado"})

@pacienteRouter.put("/paciente/{id}", tags=["ActualizarPaciente"])
def actualizarVeterinario(id: int, paciente: PacienteCreate):
    db = Session()
    result = db.query(PacienteModel).filter(PacienteModel.id == id).first()

    result.nombre = paciente.nombre
    result.apellido = paciente.apellido
    result.edad = paciente.edad
    result.tipoSangre = paciente.tipoSangre
    result.veterinarioId = paciente.veterinarioId
    db.commit()
    return JSONResponse(content={"message": "Paciente actualizado"}, status_code=200)

@pacienteRouter.delete("/paciente/{id}",tags=['EliminarPaciente'],response_model=dict)
def eliminarVeterinario(id:int):
    db = Session()
    result = db.query(PacienteModel).filter(PacienteModel.id == id).first()
    if(not result):
        return JSONResponse(status_code=404, content={"message":"Paciente no encontrado"})
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message":"Paciente eliminado"}, status_code=200)