from config.database import Base
from sqlalchemy import Column,Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Veterinario(Base):
    #Ver el modelo paciente y tratamiento para enter las columnas y la id
    __tablename__ = "Veterinario"

    #Se crea una columna llamada ID, funcionará como llave primaria o como identificador único de un registro(Debe ser un entero)
    id = Column(Integer, primary_key=True, index=True)
    # Una columna que solo admite Strings, y es obligatorio ponerlo ya que nullable es igual a False
    nombre = Column(String, nullable=False)
    # Una columna que solo admite Strings, y es obligatorio ponerlo ya que nullable es igual a False
    apellido = Column(String, nullable=False)
    # Una columna que solo admite enteros, y es obligatorio ponerlo ya que nullable es igual a False
    edad = Column(Integer, nullable=False)

    #Con el cascade hará que los pacientes relacionados también se borren
    pacientes = relationship("Paciente", back_populates="veterinario",cascade="all, delete-orphan")