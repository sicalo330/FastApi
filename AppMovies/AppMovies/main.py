import time
from fastapi import FastAPI, Path, Query, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.responses import HTMLResponse, JSONResponse
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

from config.database import engine, Base

from middlewares.jwt_bearer import JWTBearer
from middlewares.error_handler import ErrorHandler

from routers.movie import movie_router

# Crear una instancia de FastAPI (aplicacion)
app = FastAPI()

# Cambio en la documentacion
app.title = "Mi aplicacion de peliculas"
app.version = "1.0.0"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
Base.metadata.create_all(bind=engine)

class User(BaseModel):
    email:str
    password:str

@app.get("/", tags=['home'])
def message():
    return HTMLResponse(content="<h1>Hola mamá aprendí a programar</h1>")

@app.post("/login", 
          tags=['auth'], 
          response_model=dict, status_code=200)
def login(user: User):
    if user.email == "admin@mail.com" and user.password == "admin":
        token = create_token(data=user.model_dump())
        result = JSONResponse(content={"token":token},
                              status_code=200)
    else:
        result = JSONResponse(content={"message": "Invalid credentials"},
                              status_code=401)
    return result