from config.database import Base
from sqlalchemy import Column,Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Tratamiento(Base):
    __tablename__ = "Tratamiento"
    #Se crea una columna llamada ID, funcionará como llave primaria o como identificador único de un registro(Debe ser un entero)
    id = Column(Integer, primary_key=True, index=True)
    # Una columna que solo admite Strings, y es obligatorio ponerlo ya que nullable es igual a False
    fechaInicio = Column(String, nullable=False)
    #Una columna que solo admite Strings, y es obligatorio ponerlo ya que nullable es igual a False
    fechaFin = Column(String, nullable=False)
    #Una columna que solo admite Strings, y es obligatorio ponerlo ya que nullable es igual a False
    tipoTratamiento = Column(String, nullable=False)
    #Una columna que solo admite Strings, y es obligatorio ponerlo ya que nullable es igual a False
    descripcion = Column(String, nullable=False)

    """
    -Teniendo en cuenta la cardinalidad de las entidades paciente y tratamiento, UN paciente necesita MUCHOS tratamientos, por lo tanto la llave foranea de paciente debe estar
    en el modelo tratamiento, se accede a la id de la tabla Paciente y que al borrarse la entidad paciente, se borran los tratamientos
    -relationship accede a la tabla Paciente y se hace una llamada a la variable tratamiento, este hará llamada inversa
    """
    pacienteId = Column(Integer, ForeignKey("Paciente.id", ondelete="CASCADE"),nullable=False)
    paciente = relationship("Paciente", back_populates="tratamiento")