from models.veterinario import Veterinario as VeterinarioModel
from fastapi import APIRouter,Path
from typing import Optional, List
from pydantic import BaseModel, Field
from config.database import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

#Estructura la ruta de veterinarioRouter
veterinarioRouter = APIRouter()

#Se crea un clase VeterinarioBase que hereda de la clase BaseModel
#Está diseñado para estructurar y validar datos de entrada en operaciones de la
#API
#Su estructura es muy similar al de los modelos de sqlalchemy
class Veterinario(BaseModel):
    #La id es un entero y no es necesario ponerlo ya que sqlite ya lo hace
    id: Optional[int] = None
    #fechaInicio es un string(str) y debe tener minimo 2 letras y maximo 40
    #min_length define el numero de letras minimo a poner y max_length define
    #el número máximo de letras a poner
    nombre: str = Field(min_length=1, max_length=40)
    apellido: str = Field(min_length=1,max_length=40)
    edad: int = Field(ge=1,le=116)

#Obtendrá una lista de todos los veterinarios que están en la base de datos
@veterinarioRouter.get("/veterinario",tags=['VerVeterinario'],response_model=List[Veterinario],status_code=200)
#Devolverá una lista de veterinarios
def getVeterinario() -> List[Veterinario]:
    #Se crea una instancia de Session() que se importo de antemano(Ver línea 5)
    db = Session()
    #Se utiliza el objeto db para obtener todos los registros de veterinario
    result = db.query(VeterinarioModel).all()
    #Devolverá una respuesta de tipo json con los datos que fueron llamados en
    #result
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Se obtendrá un veterinario buscandolo meidante su id
@veterinarioRouter.get("/veterinario/{id}",tags=['VerVeterinario'],response_model=Veterinario, status_code=200)
def getVeterinarioId(id:int = Path(ge = 1,le = 2000)):#Establece que id debe ser mayor que 1 pero menor que 2000
    #Se crea una instancia de la clase Session()
    db = Session()
    #Se filtran los datos, se accede a la id del modelo Veterinario de sqlaclhemy(ver veterinario en la carpeta models) y se hace una consulta teniendo en cuenta la id
    #Se obtiene el primer registro que se adecúe a la condición dada por la id
    result = db.query(VeterinarioModel).filter(VeterinarioModel.id == id).first()
    #Se declará una variable llamada response tendrá los datos obtenidos de result
    response = JSONResponse(content=jsonable_encoder(result),status_code=200)
    #En el caso de que la variable result no tenga ningún registro que cumpla con la condición(Es decir que no haya encontrado un registro con la id a buscar)
    #Mostrará un mensaje que dice "Veterinario no encontrado"
    if(not result):
        response = JSONResponse(content={"message":"Veterinario no encontrado"}, status_code=404)
    #Se devolverán los datos obtenidos en response
    return response

#Esto sirve para crear veterinario
@veterinarioRouter.post("/veterinario",tags=['CrearVeterinario'],response_model=dict,status_code=202)
def crearVeterinario(veterinario: Veterinario):
    db = Session()
    #Crea una nueva instancia de VeterinarioModel utilizando los datos proporcionados en docs
    newVeterinario = VeterinarioModel(**veterinario.model_dump())
    #Agrega el nuevo veterinario a la sesión de la base de datos.
    db.add(newVeterinario)
    #Confirma los cambios y los envía definitivamete a la base de datos
    db.commit()
    #Retorna un mensaje diciendo que veterinario fue creado
    return JSONResponse(content={"message":"VeterinarioCreado"})

#Ruta para actualizar un veterinario buscando su ID
@veterinarioRouter.put("/veterinario/{id}",tags=["ActualizarVeterinario"])
#Recibe la una id y se crea un objeto de tipo VeterinarioCreate
def actualizarVeterinario(id:int, veterinario:Veterinario):
    db = Session()
    #Se busca un veterinario por su id
    result = db.query(VeterinarioModel).filter(VeterinarioModel.id == id).first()
    #Si veterinario existe aparecerá este mensaje
    if(not result):
        return JSONResponse(content={"message":"veterinario no encontrado"})

    #Se reemplazan los valores dados en docs
    result.nombre = veterinario.nombre
    result.apellido = veterinario.apellido
    result.edad = veterinario.edad
    #Se confirman los datos y se envían a la base de datos
    db.commit()
    #Se devuelve un mensaje
    return JSONResponse(content={"message":"Veterinario actualizado"},status_code=200)

#Ruta para eliminar veterinario
#Dará como respúesta un diccionario
@veterinarioRouter.delete("/veterinario/{id}",tags=['EliminarVeterinario'],response_model=dict)
def eliminarVeterinario(id:int):
    db = Session()
    result = db.query(VeterinarioModel).filter(VeterinarioModel.id == id).first()
    #Verifica si el veterinario existe
    if(not result):
        return JSONResponse(status_code=404, content={"message":"Veterinario no encontrado"})
    #Si el veterinario existe se usa el método delete teniendo de parámetro result
    db.delete(result)
    #Los cambios se confirman en la base de datos
    db.commit()
    #Se devuelve un mensaje llamado veterinario eliminado
    return JSONResponse(content={"message":"Veterinario eliminado"}, status_code=200)