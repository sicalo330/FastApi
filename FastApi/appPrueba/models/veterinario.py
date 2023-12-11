from config.database import Base
from sqlalchemy import Column,Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Veterinario(Base):
    __tablename__ = "Veterinario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)

    #Con el cascade hará que los pacientes relacionados también se borren, recordar preguntarle al profesor si es válido
    pacientes = relationship("Paciente", back_populates="veterinario",cascade="all, delete-orphan")