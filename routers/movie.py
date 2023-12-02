from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from pydantic import BaseModel, Field

from middlewares.jwt_bearer import JWTBearer
from models.movie import Movie as MovieModel
from config.database import Session
from models.movie import Movie

movie_router = APIRouter()

@movie_router.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200)
def get_all_movies() -> List[Movie]:
  db = Session()
  movies = db.query(MovieModel).all()
  return JSONResponse(content=jsonable_encoder(movies), status_code=200)

@movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie, status_code=200)
def get_movie_by_id(id: int = Path(ge=1, le=2000)):
  db = Session()
  movie = db.query(MovieModel).filter(MovieModel.id == id).first()
  response = JSONResponse(content=jsonable_encoder(movie), status_code=200)
  if not movie:
    response = JSONResponse(content={'message': 'Movie not found'}, status_code=404)
    
  return response

# Query parameters
@movie_router.get('/movies/', tags=['Movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=12)):
  db = Session()
  movies = db.query(MovieModel).filter(MovieModel.category == category).all()
  response = JSONResponse(content=movies, status_code=200)
  if not movies:
    response = JSONResponse(content={'message': 'Category not found'}, status_code=404)
    
  return response

@movie_router.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def add_movie(movie: Movie):
  db = Session()
  new_movie = MovieModel(**movie.model_dump())
  db.add(new_movie)
  db.commit()
  return JSONResponse(content={'message': 'Movie added successfully'}, status_code=201)

@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie):
  db = Session()
  movie = db.query(MovieModel).filter(MovieModel.id == id).first()
  
  if not movie:
    return JSONResponse(content={'message': 'Movie not found'}, status_code=404)
  
  print(help(movie))
  # db.commit()
    
  return JSONResponse(content={'message': 'Movie updated successfully'}, status_code=200)

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(id: int = Path(ge=1, le=2000)):
  db = Session()
  movie = db.query(MovieModel).filter(MovieModel.id == id).first()
  if not movie:
    return JSONResponse(content={'message': 'Movie not found'}, status_code=404)
  
  db.delete(movie)
  db.commit()
    
  return JSONResponse(content={'message': 'Movie deleted successfully'}, status_code=200)