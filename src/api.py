from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi import Depends, FastAPI, HTTPException
import sys
sys.path.insert(0, './src')
from database import db
from re import search
from typing import List
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import psycopg2
import sys
from starlette.responses import Response
sys.path.insert(0, './src')
import models
import schemas
from database import db
from fastapi.responses import FileResponse
import shutil
import json
import os
import os.path

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
cur_booking_id = 0
cur = db.connect()
models.Base.metadata.create_all(bind=db)
app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Agung
def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path

# API Endpoints
@app.put('/upload-cv', tags=['Uploader'])
async def upload_cv(booking_id: int, uploaded_file: UploadFile = File(...)):
    file_path = f"./cv_tuteers/{uploaded_file.filename}"
    file_location = uniquify(file_path)
    item_found = False

    search_formula = 'SELECT * FROM booking WHERE "ID_Booking" = %s'
    item = cur.execute(search_formula, booking_id)
    result = item.fetchone()
    if result != None:
        if result[0] == booking_id:
            if result[3] == None:
                # cv blm ada
                item_found = True
                alter_formula = 'UPDATE booking SET cv = %s WHERE "ID_Booking" = %s'
                values = (file_location, booking_id)
                try:
                    with open(file_location, "wb+") as file_object:
                        shutil.copyfileobj(uploaded_file.file, file_object)
                    cur.execute(alter_formula, values)
                except:
                     raise HTTPException(
                         status_code=404, detail=f'There was an error!')
            else:
                return {"message": "CV exists!"}
    if item_found:
        return {"message": f"file '{uploaded_file.filename}' uploaded for booking number: {booking_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Booking not found!')
    
   
@app.put("/upload-review", tags=['Uploader'])
async def upload_review(booking_id: int, reviewer_id: int, uploaded_file: UploadFile = File(...)):
    file_path = f"./hasil_review/{uploaded_file.filename}"
    file_location = uniquify(file_path)
    item_found = False

    search_formula = 'SELECT * FROM review WHERE "ID_Booking" = %s and "ID_Reviewer" = %s'
    search_value = (booking_id, reviewer_id)
    item = cur.execute(search_formula, search_value)
    result = item.fetchone()
    print(result)
    if result != None:
        if result[0] == reviewer_id and result[1] == booking_id:
            if result[2] == None:
                # cv blm ada
                item_found = True
                alter_formula = 'UPDATE review SET "Hasil_Review" = %s, "isDone" = true WHERE "ID_Booking" = %s and "ID_Reviewer" = %s'
                values = (file_location, booking_id, reviewer_id)
                try:
                    with open(file_location, "wb+") as file_object:
                        shutil.copyfileobj(uploaded_file.file, file_object)
                    cur.execute(alter_formula, values)
                except:
                     raise HTTPException(
                         status_code=404, detail=f'There was an error!')
            else:
                return {"message": "Review exists!"}
    if item_found:
        return {"message": f"Review file '{uploaded_file.filename}' uploaded for booking number: {booking_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Review not found!')

@app.get("/download-cv", tags=['Downloader'])
async def download_tuteers_cv(booking_id: int):
    item_found = False
    search_formula = 'SELECT * FROM booking WHERE "ID_Booking" = %s'
    item = cur.execute(search_formula, booking_id)
    result = item.fetchone()
    if result != None:
        if result[0] == booking_id:
            item_found = True
            if result[3] == None:
                #cv belum ada
                return {"message": "CV doesn't exist!"}
            else:
                path = result[3]
                filename = "CV_IDBooking_" + str(result[0]) + ".pdf"
    if item_found:
        return FileResponse(path=path, filename=filename, media_type='application/pdf')
    raise HTTPException(
        status_code=404, detail=f'Booking did not exist!')

@app.get("/download-cv-review", tags=['Downloader'])
async def download_review_cv(booking_id: int):
    item_found = False
    search_formula = 'SELECT * FROM review WHERE "ID_Booking" = %s'
    item = cur.execute(search_formula, booking_id)
    result = item.fetchone()
    print(result)
    if result != None:
         if result[0] == booking_id:
            item_found = True
            if result[2] == None:
                #review belum ada
                return {"message": "Review isn't available yet!"}
            else:
                path = result[2]
                filename = "ReviewCV_IDBooking_" + str(result[1]) + ".pdf"
    if item_found:
        return FileResponse(path=path, filename=filename, media_type='application/pdf')
    raise HTTPException(
        status_code=404, detail=f'CV Review doesnt exists!')

@app.put('/remove-cv-from-booking', tags=['Delete'])
async def remove_cv_from_booking(booking_id: int):
    item_found = False
    search_formula = 'SELECT * FROM booking WHERE "ID_Booking" = %s'
    item = cur.execute(search_formula, booking_id)
    result = item.fetchone()
    if result != None:
        item_found = True
        if result[3] == None:
            return {"message" : "There is no CV yet!"}
        else:
            file_location = result[3]
            try:
                nullify = 'UPDATE booking SET "cv" = NULL WHERE "ID_Booking" = %s'
                value = (booking_id)
                cur.execute(nullify, value)
                os.remove(file_location)
            except:
                return {"message": "There is an error!"}

    if item_found:
        return {"message": f"CV file has been deleted for booking number: {booking_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Booking not found!')

@app.put('/delete-review', tags=['Delete'])
async def remove_cv_from_review(booking_id: int, reviewer_id: int):
    item_found = False
    search_formula = 'SELECT * FROM review WHERE "ID_Booking" = %s and "ID_Reviewer" = %s'
    values = (booking_id, reviewer_id)
    item = cur.execute(search_formula, values)
    result = item.fetchone()
    if result != None:
        item_found = True
        if result[2] == None:
            return {"message" : "There is no Review yet!"}
        else:
            file_location = result[2]
            try:
                nullify = 'UPDATE review SET "Hasil_Review" = NULL, "isDone" = False WHERE "ID_Booking" = %s and "ID_Reviewer" = %s'
                value = (booking_id, reviewer_id)
                cur.execute(nullify, value)
                os.remove(file_location)
            except:
                return {"message": "There is an error!"}
    if item_found:
        return {"message": f"CV review file has been deleted for booking number: {booking_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Review not found!')

@app.get("/review", tags=["Get"])
async def get_all_review():
    item = cur.execute('SELECT * FROM review')
    result = item.fetchall()
    return result
@app.get("/paket", tags=["Get"])
async def get_all_paket():
    item = cur.execute('SELECT * FROM paket')
    result = item.fetchall()
    return result

@app.get("/paket-by-paket_id", tags=["Get"])
async def get_paket(paket_id: int):
    item_found = False
    search_formula = 'SELECT * FROM paket WHERE "ID_Paket" = %s'
    values = (paket_id)
    item = cur.execute(search_formula, values)
    result = item.fetchone()
    if result != None:
        item_found = True
        if result[0] == paket_id:
            return result
            
    if item_found:
        return {"message": f"Paket: {paket_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Paket not found!')


@app.get("/paket-of-booking", tags=["Get"])
async def get_paket_of_booking(booking_id: int):
    formula = 'select b."ID_Booking", p."ID_Paket", p.jumlah_cv, p.harga, p.durasi from booking b, paket p where b."ID_Paket" = p."ID_Paket" and b."ID_Booking" = %s'
    try:
        item = cur.execute(formula, booking_id)
        result = item.fetchone()
    except Exception as e:
        print(e)
        raise HTTPException(
		    status_code=404, detail=f'Query Error!')
    return result
    
@app.get("/booking", tags=["Get"])
async def get_all_booking():
    item = cur.execute('SELECT * FROM booking')
    result = item.fetchall()
    return result

@app.get("/booking-by-booking_id", tags=["Get"])
async def get_booking(booking_id: int):
    item_found = False
    search_formula = 'SELECT * FROM booking WHERE "ID_Booking" = %s'
    values = (booking_id)
    item = cur.execute(search_formula, values)
    result = item.fetchone()
    if result != None:
        item_found = True
        if result[0] == booking_id:
            return result
            
    if item_found:
        return {"message": f"Booking: {booking_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Booking not found!')
    
@app.get("/booking-by-tuteers_id", tags=["Get"])
async def get_booking_by_tuteers_id(tuteers_id: int):
    item_found = False
    booking_id = cur_booking_id
    search_formula = 'SELECT * FROM booking WHERE "ID_Tuteers" = %s ORDER BY "ID_Booking" DESC limit 1'
    values = (tuteers_id)
    item = cur.execute(search_formula, values)
    result = item.fetchone()
    if result != None:
        item_found = True
        if result[2] == tuteers_id:
            booking_id = result[0]
            return booking_id

    if item_found:
        return {"message": f"Booking_id: {booking_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Tuteers Booking not found!')

@app.get("/transaksi", tags=["Get"])
async def get_all_transaksi():
    item = cur.execute('SELECT * FROM transaksi')
    result = item.fetchall()
    return result

@app.get("/transaksi-by-transaksi_id", tags=["Get"])
async def get_transaksi(transaksi_id: int):
    item_found = False
    search_formula = 'SELECT * FROM transaksi WHERE "ID_Transaksi" = %s'
    values = (transaksi_id)
    item = cur.execute(search_formula, values)
    result = item.fetchone()
    if result != None:
        item_found = True
        if result[0] == transaksi_id:
            return result
            
    if item_found:
        return {"message": f"Transaksi: {transaksi_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Transaksi not found!')

#DELETE
@app.delete("/delete-booking-by-booking_id", tags=["Delete"])
async def delete_booking(booking_id : int):
    delete_formula = 'DELETE FROM booking where "ID_Booking" = %s'
    values = (booking_id)
    item = cur.execute(delete_formula, values)
    return {"message" : "Booking dengan id " +str(booking_id)+ " berhasil dihapus"}

@app.delete("/delete-transaksi-by-transaksi_id", tags=["Delete"])
async def delete_transaksi(transaksi_id : int):
    delete_formula = 'DELETE FROM transaksi where "ID_Transaksi" = %s'
    values = (transaksi_id)
    item = cur.execute(delete_formula, values)
    return {"message" : "Transaksi dengan id " +str(transaksi_id)+ " berhasil dihapus"}

#ADD
@app.post("/create-booking", tags=["Add"])
#async def add_booking(paket_id: int, current_user: User = Depends(get_current_active_user)):
async def add_booking(paket_id: int, tuteers_id: int):
    try:
        item = cur.execute('select "ID_Booking" from booking order by "ID_Booking" DESC LIMIT 1')
        current_booking_id = item.fetchone()[0]
    except:
        raise HTTPException(
		    status_code=404, detail=f'Tidak bisa membuat id booking')

    booking_id = int(current_booking_id)+1
    add_formula = 'INSERT INTO booking ("ID_Booking", "ID_Paket", "ID_Tuteers", "tgl_pesan") values (%s, %s, %s, current_timestamp)'
    values = (booking_id, paket_id, tuteers_id)
    try:
        item2 = cur.execute(add_formula, values)
    except Exception as E:
        raise HTTPException(
		    status_code=404, detail=f'Gagal membuat booking')
    return {"message" : "Berhasil menambahkan booking dengan id booking " +str(booking_id)}

@app.post("/create-transaksi", tags=["Add"])
#async def add_booking(paket_id: int, current_user: User = Depends(get_current_active_user)):
async def add_transaksi(booking_id: int):
    try:
        # item = cur.execute('select "ID_Transaksi" from transaksi order by "ID_Transaksi" DESC LIMIT 1')
        item = cur.execute('select count(*) from transaksi')
        current_transaksi_id = item.fetchone()[0]
    except:
        raise HTTPException(
		    status_code=404, detail=f'Tidak bisa membuat id transaksi')
    transaksi_id = int(current_transaksi_id)+1
    add_formula = 'INSERT INTO transaksi ("ID_Transaksi", "ID_Booking", "Metode_Pembayaran", "Bukti_Pembayaran") values (%s, %s, %s, true)'
    values = (transaksi_id, booking_id, "BCA Virtual Account")
    try:
        item2 = cur.execute(add_formula, values)
    except Exception as E:
        raise HTTPException(
	        status_code=404, detail=f'Gagal melakukan transaksi')
    return {"message" : "Berhasil melakukan pembayaran untuk id booking " +str(booking_id)}

#Stella
def verify_password(plain_password, hashedPassword):
    return pwd_context.verify(plain_password, hashedPassword)

def get_password_hash(password):
    return pwd_context.hash(password)

def makeDateFormat(year: int, month: int, date: int):
    return(str(year)+'-'+str(month)+'-'+str(date))

@app.get('/ambilDataTuteers', tags = ['Manajemen Akun'])
async def ambilSemua(em: str):
    query = "SELECT * FROM tuteers WHERE email = '" + em + "';"
    current_user_query = cur.execute(query)
    return(current_user_query.fetchone())

@app.get('/ambilDataReviewer', tags = ['Manajemen Akun'])
async def ambilSemuaAdmin(em: str):
    query = "SELECT * FROM reviewer WHERE email = '" + em + "';"
    current_user_query = cur.execute(query)
    return(current_user_query.fetchone())

def apakahEmailExistTuteers(email:str):
    query = "SELECT EXISTS(SELECT * from tuteers WHERE email = %s);"
    values = email
    Execute=cur.execute(query,values).fetchone()
    return(Execute[0])

def apakahEmailExistReviewer(email:str):
    query = "SELECT EXISTS(SELECT * from reviewer WHERE email = %s);"
    values = email
    Execute=cur.execute(query,values).fetchone()
    return(Execute[0])

def ambilPassinDB(em:str):
    query = 'SELECT "hashedPassword" FROM tuteers WHERE email = %s;'
    current_user_query = cur.execute(query,em)
    return(current_user_query.fetchone()[0])

def ambilPassinDBRev(em:str):
    query = 'SELECT "hashedPassword" FROM reviewer WHERE email = %s;'
    current_user_query = cur.execute(query,em)
    return(current_user_query.fetchone()[0])

def authenticate_user(email: str, password: str):
    a = False
    if apakahEmailExistTuteers(email):
        passdiDB = ambilPassinDB(email)
        if verify_password(password, passdiDB):
            a = True
    return a

def authenticate_user_reviewer(email: str, password: str):
    a = False
    if apakahEmailExistReviewer(email):
        passdiDB = ambilPassinDBRev(email)
        if verify_password(password, passdiDB):
            a = True
    return a

@app.get('/login', tags = ['Manajemen Akun'])
async def login (email: str, password: str):
    if authenticate_user(email,password)==True:
        return True
    else:
        return False

@app.get('/loginadmin', tags = ['Manajemen Akun'])
async def loginadm (email: str, password: str):
    if authenticate_user_reviewer(email,password)==True:
        return True
    else:
        return False

@app.get('/resetPasswordSQL/', tags=["Manajemen Akun"])
async def reset_password_sql(passbaru: str, email: str):
    update_formula = 'UPDATE "tuteers" SET "hashedPassword" = %s WHERE "email" = %s'
    values = (get_password_hash(passbaru),email)
    item = cur.execute(update_formula, values)
    return ("Query Update Success")

@app.post('/registerSQL', tags = ['Manajemen Akun'])
async def register_sql(name: str, email: str, password: str, reenterpass: str, noHP: str, year: str, month: str, date: str, gender: str):
    if password == reenterpass:
        tanggal =  makeDateFormat(year,month,date)
        genderStr = gender
        passwordhashed = get_password_hash(password)
        query1 = 'INSERT INTO tuteers ("nama", "email", "noHP", "tanggalLahir", "gender","hashedPassword") VALUES'
        query2 = "(%s,%s,%s,%s,%s,%s);"
        query = query1+query2
        values = (name, email, noHP, tanggal, genderStr, passwordhashed)   
        cur.execute(query, values)
        return('Success')
    else:
        return('Password Tidak Sama!')

#Caca
@app.get('/reviewerbookingdia', tags=["ReviewCV"])
# async def read_all_booking(current_user: User = Depends(get_current_active_user)):
async def review_booking():
    item = cur.execute('SELECT b."ID_Booking", DATE(b."tgl_pesan") as tgl, r."isDone" FROM booking b, review r WHERE r."ID_Booking"=b."ID_Booking" AND r."ID_Reviewer"=1')
    result = item.fetchall()
    return result

#halaman awal booking yg blm direview siapapun
@app.get('/reviewerbooking', tags=["ReviewCV"])
# async def read_all_booking(current_user: User = Depends(get_current_active_user)):
async def read_all_booking():
    item = cur.execute('SELECT "ID_Booking", DATE("tgl_pesan") as tgl FROM booking WHERE "ID_Booking" NOT IN (SELECT b."ID_Booking" FROM booking b, review r WHERE r."ID_Booking"=b."ID_Booking")')
    result = item.fetchall()
    return result

# #pilih booking - masih salah
@app.post('/reviewerpilihbooking/{id_booking}', tags=["ReviewCV"])
async def choose_booking(id_booking:int, id_reviewer:int):
    values = (id_reviewer,id_booking)
    query = 'INSERT INTO review ("ID_Reviewer", "ID_Booking", "isDone") VALUES (%s,%s,false)'
    item = cur.execute(query, values)
    return('Success')
