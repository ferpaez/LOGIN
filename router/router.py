from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from schema.user_schema import UserSchema, DataUser
from config.db import engine
from model.user import users
from werkzeug.security import generate_password_hash, check_password_hash


user = APIRouter()

@user.get("/")
def root():
    return {"message": "aguante boca"}

@user.get('/api/user')
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()        #llama a todos los usuarios de la db
        return result

@user.get('/api/user/{user_id}')
def get_user(user_id: str):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).fetchone()     #llama a un usuario de la db
        return result



@user.post('/api/user', status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:       # abre y cierra la conexion a la db   
        new_user = {
            "id": data_user.id,
            "name": data_user.name,
            "username": data_user.username,
            "user_password": generate_password_hash(data_user.user_password, "pbkdf2:sha256:30", 30),
        }

        conn.execute(users.insert().values(new_user))
        conn.commit()

        return Response(status_code=HTTP_201_CREATED)

@user.post('/api/user/login')
def login_user(data_user: DataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.username == data_user.username)).fetchone()
        if result:
            if check_password_hash(result.user_password, data_user.user_password):
                return {"message": "Login exitoso"}
            else:
                return {"message": "Contraseña incorrecta"}
        else:
            return {"message": "Usuario no encontrado"}



@user.put('/api/user/{user_id}')    #actualiza un usuario
def update_user(user_id: str, data_update: UserSchema):
    with engine.connect() as conn:
        encrypted_password = generate_password_hash(data_update.user_password, "pbkdf2:sha256:30", 30)
        
        conn.execute(users.update().where(users.c.id == user_id).values(
            name = data_update.name,
            username = data_update.username,
            user_password = encrypted_password
        ).where(users.c.id == user_id))

        result = conn.execute(users.select().where(users.c.id == user_id)).fetchone()
        
        return result
    
@user.delete('/api/user/{user_id}', status_code=HTTP_204_NO_CONTENT)     #borra un usuario
def delete_user(user_id: str):
    with engine.connect() as conn:
        conn.execute(users.delete().where(users.c.id == user_id))
        return Response(status_code=HTTP_204_NO_CONTENT)