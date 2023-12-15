from models.paciente import Paciente as PacienteModel
from fastapi import APIRouter,Path
from typing import Optional, List
from pydantic import BaseModel, Field
from config.database import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload

#Estructura la ruta de pacienteRouter
pacienteRouter = APIRouter()

#Se crea un clase PacienteBase que hereda de la clase BaseModel
#Está diseñado para estructurar y validar datos de entrada en operaciones de la API
#Su estructura es muy similar al de los modelos de sqlalchemy
class PacienteBase(BaseModel):
    #La id es un entero y no es necesario ponerlo ya que sqlite ya lo hace
    id: Optional[int] = None
    #nombre es un string(str) y debe tener minimo 2 letras y maximo 40
    #min_length define el numero de letras minimo a poner y max_length define el número máximo de letras a poner
    nombre: str = Field(min_length=2, max_length=40)
    apellido: str = Field(min_length=1, max_length=20)
    edad: int = Field(ge=1, le=116)
    tipoSangre: str = Field(min_length=1, max_length=3)
    # El veterinarioId es un entero opcional (puede ser None), que indica la relación con un veterinario.
    veterinarioId: Optional[int] = None

#Básicamente es lo mismo que PacienteBase y no añade nada nuevo, simplemente se utiliza a la hora de crar instancias de Paciente con datos adicionales
class PacienteCreate(PacienteBase):
    pass

"""
Estas clases proporcionan una estructura para manejar diferentes situaciones en la aplicación,
como la creación de nuevos pacientes (PacienteCreate) y la manipulación de instancias existentes de pacientes
"""
class Paciente(PacienteBase):
    id: Optional[int] = None
    veterinario: Optional[int] = None

#Obtendrá una lista de todos los pacientes que están en la base de datos
@pacienteRouter.get("/pacientes", tags=['VerPaciente'], response_model=List[Paciente], status_code=200)
#Devolverá una lista de pacientes
def getPaciente() -> List[Paciente]:
    #Se crea una instancia de Session() que se importo de antemano(Ver línea 5)
    db = Session()
    #Se utiliza el objeto db para obtener todos los registros de paciente
    result = db.query(PacienteModel).all()
    #Devolverá una respuesta de tipo json con los datos que fueron llamados en result
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Obtendrá un paciente tomando una id como parámetro
@pacienteRouter.get("/pacientes/{id}",tags=["VerPaciente"],response_model=Paciente, status_code=200)
def getPacienteId(id:int = Path(ge=1,le=2000)):#Establece que id debe ser mayor que 1 pero menor que 2000
    #Se crea una instancia de la clase Session()
    db = Session()
    #Se filtran los datos, se accede a la id del modelo Paciente de sqlaclhemy(ver paciente en la carpeta models) y se hace una consulta teniendo en cuenta la id
    #Se obtiene el primer registro que se adecúe a la condición dada por la id
    result = db.query(PacienteModel).filter(PacienteModel.id == id).options(joinedload(PacienteModel.veterinario)).first()
    #Se declará una variable llamada response tendrá los datos obtenidos de result
    response = JSONResponse(content=jsonable_encoder(result),status_code=200)
    #En el caso de que la variable result no tenga ningún registro que cumpla con la condición(Es decir que no haya encontrado un registro con la id a buscar)
    #Mostrará un mensaje que dice "Paciente no encontrado"
    if (not result):
        response = JSONResponse(content={"message":"Paciente no fue encontrado"},status_code=404)
    #Se devolverán los datos obtenidos en response
    return response

#Esto sirve para crear pacientes
@pacienteRouter.post("/pacientes", tags=['CrearPaciente'], response_model=Paciente, status_code=201)
def crearPaciente(paciente: PacienteCreate):
    db = Session()
    #Crea una nueva instancia de PacienteModel utilizando los datos proporcionados en docs
    newPaciente = PacienteModel(**paciente.model_dump())
    #Agrega el nuevo paciente a la sesión de la base de datos
    db.add(newPaciente)
    #Confirma los cambios y los envía definitivamete a la base de datos
    db.commit()
    #Retorna un mensaje diciendo que paciente fue creado
    return JSONResponse(content={"message": "Paciente creado"})

#Esto sirve para actualizar los datos del paciente
@pacienteRouter.put("/paciente/{id}", tags=["ActualizarPaciente"])
#Para aclarar, se crea un objeto de tipo PacienteCreate para que se almacenen los nuevos datos
def actualizarVeterinario(id: int, paciente: PacienteCreate):
    db = Session()
    #Se obitienen los datos del paciente filtrados por id
    result = db.query(PacienteModel).filter(PacienteModel.id == id).first()

    #Digamos que result es un paciente con los datos ya escritos, mientras que el objeto paciente tiene las mismas columna que el paciente proveniente de result pero vacíos
    #Lo que estamos haciendo es actualizar los datos de paciente con el nuevo valor proporcionado en docs
    result.nombre = paciente.nombre
    result.apellido = paciente.apellido
    result.edad = paciente.edad
    result.tipoSangre = paciente.tipoSangre
    result.veterinarioId = paciente.veterinarioId
    #Se confirma los valores y se envían los nuevos datos a la base de datos
    db.commit()
    return JSONResponse(content={"message": "Paciente actualizado"}, status_code=200)

#Esta ruta sirve para eliminar un pacinete mediante su id
#Dará como respúesta un diccionario
@pacienteRouter.delete("/paciente/{id}",tags=['EliminarPaciente'],response_model=dict)
def eliminarVeterinario(id:int):
    db = Session()
    result = db.query(PacienteModel).filter(PacienteModel.id == id).first()
    #Verifica si el paciente existe
    if(not result):
        return JSONResponse(status_code=404, content={"message":"Paciente no encontrado"})
    #Si el paciente existe se usa el método delete teniendo de parámetro result
    db.delete(result)
    #Los cambios se confirman en la base de datos
    db.commit()
    #Se devuelve un mensaje llamado paciente eliminado
    return JSONResponse(content={"message":"Paciente eliminado"}, status_code=200)