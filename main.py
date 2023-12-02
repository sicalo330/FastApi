import time

from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder

from jwt_manager import create_token
from config.database import engine, Base
from middlewares.jwt_bearer import JWTBearer
from middlewares.errorHandler import ErrorHandler
from routers.movie import movie_router

app = FastAPI()

app.title = 'Peliculas API'
app.description = 'API de peliculas'
app.version = '1.0.0'

app.add_middleware(ErrorHandler)
app.add_route(movie_router)

Base.metadata.create_all(bind=engine)


class User(BaseModel):
  email: str
  password: str = Field(min_length=8)
  

@app.get('/', tags=['Home'], dependencies=[Depends(JWTBearer())])
def home():
  return HTMLResponse(content='<h1>Hola mamá aprendí a programar</h1>', status_code=200)


@app.post('/login', tags=['auth'], response_model=dict, status_code=200)
def login(user: User = Body()):
  if user.email == 'admin@mail.com' and user.password == '12345678':
    token = create_token(data=user.model_dump())
    response = JSONResponse(content={'message': 'Login success', 'token': token}, status_code=200)
  else:
    response = JSONResponse(content={'message': 'Login failed'}, status_code=401)
    
  return response