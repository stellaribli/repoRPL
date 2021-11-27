from enum import Enum
from datetime import date, datetime, timedelta
import enum
import json
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.sql.sqltypes import Date
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from re import search
from fastapi import Depends, FastAPI, HTTPException
import psycopg2
import sys
sys.path.insert(0, './src')
import models
import schemas
from database import db
from fastapi.responses import FileResponse
import shutil
import os
import os.path

cur = db.connect()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(description ="Login Account Tuteers")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    tanggal_lahir:Optional[str] = None
    jenis_kelamin: Optional[str] = None
    nomor_hp: Optional[int] = None

class UserInDB(User):
    hashed_password: str

class GenderEnum(enum.Enum):
    Male = "Male"
    Female = "Female"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

with open("user.json", "r") as read_file:
    fake_users_db = json.load(read_file)
read_file.close()

def hitungJumlahAkun():
    hitungJumlahAkun = cur.execute('SELECT COUNT(*) FROM tuteers;')
    jumlah = hitungJumlahAkun.fetchone()
    return(jumlah[0])

def makeDateFormat(year: int, month: int, date: int):
    return(str(year)+'-'+str(month)+'-'+str(date))
    
def enumToStr(gender:GenderEnum):
    if gender ==GenderEnum.Female:
        return("Female")
    elif gender ==GenderEnum.Male:
        return("Male")
    
def updateDate(tanggal: date):
    update_formula = 'UPDATE tuteers SET "tanggalLahir" = %s WHERE "ID_Tuteers" = 1'
    cur.execute(update_formula, tanggal)
    return('Gender Successfully Changed to Female!')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

#blm bener
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict) #supposed to be hash keknya

print(get_user(fake_users_db,'asdf'))
# print(get_user(cur,'asdf'))

def authenticate_user(fake_db, username: str, password: str): #Login keknya
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def curr_username(current_user: User = Depends(get_current_active_user)):
    return current_user.username

async def isCurrUsername(username: str, current_user: User = Depends(get_current_active_user)):
    if username==current_user.username:
        return(True)
    else:
        return(False)

@app.get('/test', tags = ['User Side'])
async def test(current_user: User = Depends(get_current_active_user)):
    return ("x")

@app.post('/registerSQL', tags = ['Manajemen Akun'])
async def register_sql(name: str, email: str, password: str, reenterpass: str, noHP: str, year: int, month: int, date: int, gender: GenderEnum):
    if password == reenterpass:
        tanggal =  makeDateFormat(year,month,date)
        genderStr = enumToStr(gender)
        passwordhashed = get_password_hash(password)
        query1 = 'INSERT INTO tuteers ("nama", "email", "noHP", "tanggalLahir", "gender","hashedPassword") VALUES'
        query2 = "(%s,%s,%s,%s,%s,%s);"
        query = query1+query2
        values = (name, email, noHP, tanggal, genderStr, passwordhashed)   
        item = cur.execute(query, values)
        return('Success')
    else:
        return('Password Tidak Sama!')

@app.post("/token", response_model=Token, tags=["Others"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    # yang diisi di form print(form_data.username) 
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get('/resetPasswordSQL/', tags=["Manajemen Akun"])
async def reset_password_sql(input: str):
    update_formula = 'UPDATE "tuteers" SET "hashedPassword" = %s WHERE "ID_Tuteers" = 1'
    values = (get_password_hash(input))
    item = cur.execute(update_formula, values)
    return ("Query Update Success")

@app.get("/tuteers")
async def gettuteers():
    item = cur.execute('SELECT email FROM tuteers')
    result = item.fetchall()
    return result

# @app.get('/apakahpasswordsama')
# async def samaga(a: str):
#     select_formula = 'SELECT "hashedPassword" FROM tuteers WHERE "ID_Tuteers" = 1;'
#     item = cur.execute(select_formula)   
#     result = item.fetchone()
#     if verify_password(a, result[0]):
#          return ("Biza")
#     else:
#         return ("h")
# @app.post('/reviewer', tags=["Admin View"])
# async def post_data(name:str, current_user: User = Depends(get_current_active_user)):
#     id=1
#     if(len(data['menu'])>0):
#         id=data['menu'][len(data['menu'])-1]['id']+1
#     new_data={'id':id,'name':name}
#     data['menu'].append(dict(new_data))
#     return ("Data berhasil diinput")
