El objetivo del proyecto final es demostrar las funcionalidades que tiene el framework a la hora de relacionar distintas entidades de una clinica veterinaria.
Estas son las entidades con sus respectivas cardinalidades:
-Paciente
-Veterinario
-Tratamiento

1 veterinario puede atiende a MUCHOS pacientes
1 paciente necesita MUCHOS tratamientos

Cada entidad podrá ser visto como si fuera una lista y se podrá buscar por ID
Cada entidad podrá ser creada desde 0
Cada entidad podrá actualizar o sobreescribir sus datos
Cada entidad podrá ser eliminada de la base de datos

Para ejecutar el proyecto se necesitan las siguientes librerías:
pip install...
-fastapi
-sqlalchemy
-pydantic
-uvicorn (para correr el servidor)
-pydantic

Nota: Recordar poner "pip install" seguido del nombre de la librería dejando un espacio
Ejemplo: pip install fastapi

Después de eso es necesario crear el ambiente virtual usando el siguiente comando: python -m venv venv
Después hay que activarlo con el siguiente comando: .\venv\Scripts\activate

Con esto ya estamos en el ambiente virtual.

Por último es necesario ejecutar el proyecto utilizando...
uvicorn main:app --reload --port 5000