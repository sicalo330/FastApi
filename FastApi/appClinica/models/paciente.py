from config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

#Este es el modelado de datos de sqlalchemy
class Paciente(Base):#Se crear una clase llamada Paciente y este hereda las funcionalidades de Base
    #La variable que se creo en database.py en la carpeta config para definir los modelos

    #Esto declará el nombre de la tabla, puede tener cualquier nombre pero obviamente es mejor tener un nombre descriptivo
    __tablename__ = "Paciente"

    #Se crea una columna llamada ID, funcionará como llave primaria o como identificador único de un registro(Debe ser un entero)
    id = Column(Integer, primary_key=True, index=True)
    #nombre es una columna que solo admite Strings, y es obligatorio ponerlo ya que nullable es igual a False
    nombre = Column(String, nullable=False)
    #Apellido es un String y es obligatorio ponerlo
    apellido = Column(String, nullable=False)
    #Edad es un entero pero a diferencia de id, esta es una columna que admite números enteros pero no sirve de llave primario
    edad = Column(Integer, nullable=False)
    tipoSangre = Column(String, nullable=False)

    #-------------------Relaciones-----------------------------------
    #Nota:Primero se debe importar relationship de sqlalchemy(Mirar línea 3)

    """
    -Aquí se define una variable con nombre tratamiento

    -La variable tiene un constructor llamado relationship este definirá la relación en los modelos
    "Tratamiento" hace referencia al nombre de la tabla al que va digido,
    back_populates="paciente" hace referencia al nombre de la variable que tiene la relación similar al que estamos explicando ahora
    cascade="all, delete-orphan" elimina todas las relaciones que tenga una entidade con otras
    por ejemplo si un veterinario tiene dos pacientes, y se elimina el veterinario, también se eliminarán los pacientes
    """
    tratamiento = relationship("Tratamiento", back_populates="paciente", cascade="all, delete-orphan")

    """
    -VeterinarioId es el nombre de la variablre que contiene la llave foranea, ya que 1 veterinario puede atender a MUCHOS pacientes
    la llave foranea de veterinario debe estar en la entidad paciente, primero se identifica la id de la entidad a relacionar,
    en este caso se está accediendo a la id de la entidad veterinario(ver veterinario.py de esta carpeta) y cuando se borre un veterinario
    también se borrará el registro de paciente

    -Muy similar a la id, este debe ser un entero y debe ser obligatorio tener uno, Foreign key debe ser importado primero(Ver la línea 2)
    -la variable veterinario tiene la misma lógica de tratamiento(Ver línea 34), básicamente toma el nombre de la tabla a relacionar
    y se accede al nombre que llama de forma inversa a la variable a relacionar
    """
    veterinarioId = Column(Integer, ForeignKey("Veterinario.id", ondelete="CASCADE"), nullable=False)
    veterinario = relationship("Veterinario", back_populates="pacientes")