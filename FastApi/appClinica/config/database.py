import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Este es el nombre del archivo.sqlite. el ../ indica que debe subir un nivel del que estamos justo ahora, es decir de  config
sqliteFileName = "../BDclinica.sqlite"
#btiene la ruta absoluta del directorio actual del script en ejecución y la almacena en la variable baseDir.
baseDir = os.path.dirname(os.path.realpath(__file__))
#Crea la url de conexión a la base de datos SQLite utilizando la ruta absoluta del archivo SQLite
databaseUrl = f"sqlite:///{os.path.join(baseDir,sqliteFileName)}"

#Creará un objeto de tipo engine que gestionará la conexión a la base de datos
engine = create_engine(databaseUrl, echo=True)
#Crea una clase Session con sessionmarker, este se vinculará a la base de datos
Session = sessionmaker(bind=engine)
#Se crea un objeto de tipo Session
session = Session()
#Crea la clase base declarativa Base que se utilizará para definir modelos, recordar la variable Base, ya que se usará para el modelado
Base = declarative_base()