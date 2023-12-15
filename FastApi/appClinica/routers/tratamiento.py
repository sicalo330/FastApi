from models.tratamiento import Tratamiento as TratamientoModel
from fastapi import APIRouter,Path
from typing import Optional, List
from pydantic import BaseModel, Field
from config.database import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload

#Estructura la ruta de tratamientoRouter
tratamientoRouter = APIRouter()

#Se crea un clase TratamientoBase que hereda de la clase BaseModel
#Está diseñado para estructurar y validar datos de entrada en operaciones de la
#API
#Su estructura es muy similar al de los modelos de sqlalchemy
class TratamientoBase(BaseModel):
    #La id es un entero y no es necesario ponerlo ya que sqlite ya lo hace
    id: Optional[int] = None
    #fechaInicio es un string(str) y debe tener minimo 2 letras y maximo 40
    #min_length define el numero de letras minimo a poner y max_length define
    #el número máximo de letras a poner
    fechaInicio: str = Field(min_length = 2,max_length = 40)
    fechaFin: str = Field(min_length = 2, max_length = 40)
    tipoTratamiento: str = Field(min_length=5, max_length=200)
    descripcion: str = Field(min_length=0,max_length=200)
    #El tratamientoId es un entero opcional (puede ser None), que indica la relación con un veterinario.
    pacienteId: Optional[int] = None

#Básicamente es lo mismo que TratamientoBase y no añade nada nuevo, simplemente se
#utiliza a la hora de crar instancias de Tratamiento con datos adicionales
class TratamientoCreate(TratamientoBase):
    pass

"""
Estas clases proporcionan una estructura para manejar diferentes
situaciones en la aplicación,
como la creación de nuevos tratamientos (TratamientoCreate) y la manipulación de
instancias existentes de tratamientos
"""

class Tratamiento(TratamientoBase):
    id: Optional[int] = None
    paciente: Optional[int] = None


#Obtendrá una lista de todos los tratamientos que están en la base de datos
@tratamientoRouter.get("/tratamiento",tags=['VerTratamiento'],response_model=List[Tratamiento],status_code=200)
#Devolverá una lista de tratamientos
def getTratamientos() -> List[Tratamiento]:
    #Se crea una instancia de Session() que se importo de antemano(Ver línea 5)
    db = Session()
    #Se utiliza el objeto db para obtener todos los registros de tratamiento
    result = db.query(TratamientoModel).all()
    #Devolverá una respuesta de tipo json con los datos que fueron llamados en
    #result
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Obtendrá un tratamiento tomando una id como parámetro
@tratamientoRouter.get("/tratamiento/{id}",tags=['VerTratamiento'], response_model=Tratamiento,status_code=200)
def getTratamiento(id:int = Path(ge=1,le=2000)):#Establece que id debe ser mayor que 1 pero menor que 2000
    #Se crea una instancia de la clase Session()
    db = Session()
    #Se filtran los datos, se accede a la id del modelo Tratamiento de sqlaclhemy(ver tratamiento en la carpeta models) y se hace una consulta teniendo en cuenta la id
    #Se obtiene el primer registro que se adecúe a la condición dada por la id
    result = db.query(TratamientoModel).filter(TratamientoModel.id == id).options(joinedload(TratamientoModel.paciente)).first()
    #Se declará una variable llamada response tendrá los datos obtenidos de result
    response = JSONResponse(content=jsonable_encoder(result),status_code=200)
    #En el caso de que la variable result no tenga ningún registro que cumpla con la condición(Es decir que no haya encontrado un registro con la id a buscar)
    #Mostrará un mensaje que dice "Tratamiento no encontrado"
    if(not result):
        response = JSONResponse(content={"message":"Tratamiento no encontrado"})
    #Se devolverán los datos obtenidos en response
    return response

#Esto sirve para crear tratamientos
@tratamientoRouter.post("/tratamiento", tags=['CrearTratamiento'], response_model=Tratamiento,status_code=201)
def crearTratamiento(tratamiento:TratamientoCreate):
    db = Session()
    #Crea una nueva instancia de TratamientoModel utilizando los datos proporcionados en docs
    newTratamiento = TratamientoModel(**tratamiento.model_dump())
    #Agrega el nuevo tratamiento a la sesión de la base de datos.
    db.add(newTratamiento)
    #Confirma los cambios y los envía definitivamete a la base de datos
    db.commit()
    #Retorna un mensaje diciendo que tratamiento fue creado
    return JSONResponse(content={"message":"Tratamiento creado"})

#Ruta para actualizar un tratamiento buscando su ID
@tratamientoRouter.put("/tratamiento/{id}",tags=["ActualizarTratamiento"])
#Recibe la una id y se crea un objeto de tipo TratamientoCreate
def actualizarTratamiento(id:int, tratamiento:TratamientoCreate):
    db = Session()
    #Se busca un tratamiento por su id
    result = db.query(TratamientoModel).filter(TratamientoModel.id == id).first()
    #Se reemplazan los valores dados en docs
    result.fechaInicio = tratamiento.fechaInicio
    result.fechaFin = tratamiento.fechaFin
    result.tipoTratamiento = tratamiento.tipoTratamiento
    result.descripcion = tratamiento.descripcion
    result.pacienteId = tratamiento.pacienteId
    #Se confirman los datos y se envían a la base de datos
    db.commit()
    #Se devuelve un mensaje
    return JSONResponse(content={"message":"Tratamiento actualizado"},status_code=200)

#Ruta para eliminar tratamiento
#Dará como respúesta un diccionario
@tratamientoRouter.delete("/tratamiento/{id}",tags=['Eliminar tratamiento'], response_model=dict)
def eliminarTratamiento(id:int):
    db = Session()
    result = db.query(TratamientoModel).filter(TratamientoModel.id == id).first()
    #Verifica si el tratamiento existe
    if(not result):
        return JSONResponse(status_code=404, content={"message":"Tratamiento no encontrado"})
    #Si el tratamiento existe se usa el método delete teniendo de parámetro result
    db.delete(result)
    #Los cambios se confirman en la base de datos
    db.commit()
    #Se devuelve un mensaje llamado tratamiento eliminado
    return JSONResponse(content={"mesage":"Tratamiento eliminado"}, status_code=200)