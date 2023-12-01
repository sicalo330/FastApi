from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
from  pydantic import BaseModel, Field
from typing import Optional, List
import time

#modelado de plantalla de peliculas
class pelicula(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=2, max_length=40)
    overview: str = Field(min_length=15, max_length=200)
    year: int = Field(le=time.localtime().tm_year)
    ranting: float = Field(ge=0.0, le = 10.0)
    category: str = Field(min_length=3, max_length=20)


# Crear una instancia de fastapi
app = FastAPI()

#cambio en la documentacion
app.title = "Mi aplicacion de peliculas"
app.version = "0.0.1"
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Mi Pelicula", min_length=5, max_length=30)
    overview: str = Field(default="Descripcion de la película", min_length=10, max_length=300)
    year: int = Field(default=2022, le=2022)
    rating: float = Field(default=10, ge=0, le=10)
    category: str = Field(default="Comedia", min_length=3, max_length=15)

# Crear una ruta
movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'adventure'    
    },
    {
        'id': 3,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Comedy'    
    }, 
    {
        'id': 4,
        'title': 'Drama Queen',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Drama'    
    }  
]

# get a la raiz del directorio
@app.get("/",tags=['root'])

#mensaje de bienvenida
def message():
    return HTMLResponse(content="<hi>Hola mamá aprendí a programar</h1>")

#get al primer end point para crear un filtro en movies(dict) por el id
@app.get("/movies/{id}", tags=["movies"], response_model=pelicula, status_code=200)
def get_movie(id:int = Path(ge=1,le=2000)):
    movie = list(filter(lambda movie: movie['id'] == id, movies))#uso de funcion lambda para el filtro
    if len(movies)>= 0:
        response = JSONResponse(status_code=200, content=movie)
    else:
        response = JSONResponse(status_code=404, content={"message": "Movie not found"})
    return movie

#creacion del segundo endpoint para el filtro en movies(dict) por la categoria
@app.get("/movies/")
def get_movie_category(category:str):
    movie = [movie for movie in movies if movie['category'] == category]#se uso una comprension de listas para el filtro(no recom.)
    return movie

#creacion del tercer endpoint para el post(publicacion) de peliculas y su adicion a la lista movies
@app.post("/movies/", tags=['movies'])
def create_movie(id: int = Body(), title: str= Body(), overview:str= Body(),
                 year:str= Body(), rating:float= Body(), category:str= Body()):
     
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
    })
    return movies

#creacion de endpoint para actualizar informacion de peliculas
@app.put("/movies/{id}", tags=['movies'])
def uptdate_movie(movie: Movie):
    
    for movie in  movies:
        if movie['id'] == id:
            movie['title'] = movie.title
            movie['overview'] = movie.overview
            movie['year'] = movie.year
            movie['rating'] = movie.rating
            movie['category'] = movie.category

    return JSONResponse(content={"message":"Movie update succesfully"},status_code=200)

#creacion de endpoint para eliminar peliculas
@app.delete("/movies/{id}", tags=['movies'], response_model=dict)
def delete_movie(id:int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            break
    return JSONResponse(content={"message":"Movie deleted suceesfully"}, status_code=200)