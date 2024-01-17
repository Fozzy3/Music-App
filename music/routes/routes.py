from fastapi import APIRouter, status
from config.db import conn
from models.user import users
from schemas.user import User
from fastapi.responses import JSONResponse
from cryptography.fernet import Fernet
from services.spotify_funtions import get_spotify_data
from schemas.spotify_data import SpotifyDataResponse

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

@user.get("/users", tags=["User"])
def get_users():
    # Obtener usuarios desde la base de datos
    result = conn.execute(users.select()).fetchall()
    
    # Convertir el resultado a una lista de diccionarios usando row._asdict()
    users_list = [row._asdict() for row in result]
    
    # Retornar la lista de usuarios
    return {"users": users_list}

@user.post("/users", response_model=list[User], tags=["User"])
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}  
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))  
    conn.commit()
    
    # Obtener el ID de la última fila insertada
    last_inserted_id = result.lastrowid
    
    # Consultar la fila recién insertada y convertir a un diccionario
    new_user_db = conn.execute(users.select().where(users.c.id == last_inserted_id)).first()
    new_user_dict = dict(new_user_db._asdict()) if new_user_db else {"status":False, "message": "User not found"}
    
    # Convertir a formato JSON y retornar
    return JSONResponse(content={"data":new_user_dict} , status_code=200)

@user.get("/users/{id}", response_model=list[User], tags=["User"])
def get_unique_user(id: str):
    new_user_db = conn.execute(users.select().where(users.c.id == id)).first()
    new_user_dict = dict(new_user_db._asdict()) if new_user_db else {"status":False, "message": "User not found"}
    return JSONResponse(content=new_user_dict, status_code=200)

@user.delete("/users/{id}", status_code=status.HTTP_200_OK, tags=["User"])
def delete_unique_user(id: str):
    result = conn.execute(users.delete().where(users.c.id == id))
    if result.rowcount > 0:
        message = {"detail": "User deleted successfully"}
        status_code = 200
    else:
        message = {"detail": "User not found"}
        status_code = 404
    return JSONResponse(content=message, status_code=status_code)

@user.put("/users/{user_id}", response_model=User, tags=["User"])
def update_user(user_id: int, updated_user: User):
    # Verificar si el usuario existe
    existing_user = conn.execute(users.select().where(users.c.id == user_id)).first()
    if not existing_user:
        return JSONResponse(content={"success": "false", "message": "User not found"}, status_code=200)

    # Actualizar la información del usuario
    update_values = {"name": updated_user.name, "email": updated_user.email}
    if updated_user.password:
        update_values["password"] = f.encrypt(updated_user.password.encode("utf-8"))

    conn.execute(users.update().where(users.c.id == user_id).values(update_values))

    # Obtener el usuario actualizado
    updated_user_db = conn.execute(users.select().where(users.c.id == user_id)).first()
    updated_user_dict = dict(updated_user_db._asdict())

    return {"success": "true", "message": "User updated successfully", "data": updated_user_dict}
    
@user.get("/spotify_albums/{artist_name}", response_model=SpotifyDataResponse, tags=["Spotify"])
def get_spotify_data_route(artist_name: str):
    try:
        spotify_data = get_spotify_data(artist_name)
        return spotify_data
    except Exception as e:
        return {"error": str(e)}

