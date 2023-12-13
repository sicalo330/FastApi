from config.database import Base
from sqlalchemy import Column,Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Tratamiento(Base):
    __tablename__ = "Tratamiento"

    id = Column(Integer, primary_key=True, index=True)
    fechaInicio = Column(String, nullable=False)
    fechaFin = Column(String, nullable=False)
    tipoTratamiento = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)

    pacienteId = Column(Integer, ForeignKey("Paciente.id", ondelete="CASCADE"),nullable=False)
    paciente = relationship("Paciente", back_populates="tratamiento")