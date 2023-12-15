from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routers.paciente import pacienteRouter
from routers.veteriario import veterinarioRouter
from routers.tratamiento import tratamientoRouter
from config.database import engine, Base

app = FastAPI()

app.title = "Mi aplicacion de peliculas"
app.version = "1.0.0"

#Se incluyenl las rutas de paciente al main
app.include_router(pacienteRouter)
#Se incluyen las rutas de veterinario al main
app.include_router(veterinarioRouter)
#Se inclye las rutas de tratamiento al main
app.include_router(tratamientoRouter)

#Crea las tablas de los modelos
Base.metadata.create_all(bind = engine)

#Simplemente se crea un h1 que dice lo siguiente
@app.get("/",tags=['Home'])
def inicio():
    return HTMLResponse(content='<h1>hola mamá aprendí a programar</h1>')