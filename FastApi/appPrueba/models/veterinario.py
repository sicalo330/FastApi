from config.database import Base
from sqlalchemy import Column,Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Veterinario(Base):
    __tablename__ = "Veterinario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    pacientes = relationship("Paciente", back_populates="veterinario")