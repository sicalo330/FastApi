from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routers.paciente import pacienteRouter
from config.database import engine, Base

app = FastAPI()

app.title = "Mi aplicacion de peliculas"
app.version = "1.0.0"

app.include_router(pacienteRouter)

Base.metadata.create_all(bind = engine)


@app.get("/",tags=['Home'])
def inicio():
    return HTMLResponse(content='<h1>hola mamá aprendí a programar</h1>')