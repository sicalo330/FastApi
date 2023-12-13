from models.tratamiento import Tratamiento as TratamientoModel
from fastapi import APIRouter,Path
from typing import Optional, List
from pydantic import BaseModel, Field
from config.database import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload

tratamientoRouter = APIRouter()

class TratamientoBase(BaseModel):
    id: Optional[int] = None
    fechaInicio: str = Field(min_length = 2,max_length = 40)
    fechaFin: str = Field(min_length = 2, max_length = 40)
    tipoTratamiento: str = Field(min_length=5, max_length=200)
    descripcion: str = Field(min_length=0,max_length=200)
    pacienteId: Optional[int] = None

class TratamientoCreate(TratamientoBase):
    pass

class Tratamiento(TratamientoBase):
    id: Optional[int] = None
    paciente: Optional[int] = None

@tratamientoRouter.get("/tratamiento",tags=['VerTratamiento'],response_model=List[Tratamiento],status_code=200)
def getTratamientos() -> List[Tratamiento]:
    db = Session()
    result = db.query(TratamientoModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@tratamientoRouter.get("/tratamiento/{id}",tags=['VerTratamiento'], response_model=Tratamiento,status_code=200)
def getTratamiento(id:int = Path(ge=1,le=2000)):
    db = Session()
    result = db.query(TratamientoModel).filter(TratamientoModel.id == id).options(joinedload(TratamientoModel.paciente)).first()
    response = JSONResponse(content=jsonable_encoder(result),status_code=200)
    if(not result):
        response = JSONResponse(content={"message":"Tratamiento no encontrado"})
    return response

@tratamientoRouter.post("/tratamiento", tags=['CrearTratamiento'], response_model=Tratamiento,status_code=201)
def crearTratamiento(tratamiento:TratamientoCreate):
    db = Session()
    newTratamiento = TratamientoModel(**tratamiento.model_dump())
    db.add(newTratamiento)
    db.commit()
    return JSONResponse(content={"message":"Tratamiento creado"})

@tratamientoRouter.put("/tratamiento/{id}",tags=["ActualizarTratamiento"])
def actualizarTratamiento(id:int, tratamiento:TratamientoCreate):
    db = Session()
    result = db.query(TratamientoModel).filter(TratamientoModel.id == id).first()

    result.fechaInicio = tratamiento.fechaInicio
    result.fechaFin = tratamiento.fechaFin
    result.tipoTratamiento = tratamiento.tipoTratamiento
    result.descripcion = tratamiento.descripcion
    result.pacienteId = tratamiento.pacienteId
    db.commit()
    return JSONResponse(content={"message":"Tratamiento actualizado"},status_code=200)

@tratamientoRouter.delete("/tratamiento/{id}",tags=['Eliminar tratamiento'], response_model=dict)
def eliminarTratamiento(id:int):
    db = Session()
    result = db.query(TratamientoModel).filter(TratamientoModel.id == id).first()
    if(not result):
        return JSONResponse(status_code=404, content={"message":"Tratamiento no encontrado"})
    db.delete(result)
    db.commit()
    return JSONResponse(content={"mesage":"Tratamiento eliminado"}, status_code=200)