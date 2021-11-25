from typing import List, Optional
import datetime
from pydantic import BaseModel
from enum import Enum
from sqlalchemy.sql.elements import Null



class Gender(int, Enum):
    male = 0
    female = 1


class Tuteers(BaseModel):
    nama: str
    email: str
    hashed_password: str
    noHP: str
    tanggalLahir: datetime.date
    gender: Gender

    class Config:
        orm_mode = True

class Reviewer(BaseModel):
    nama_reviewer: str
    email: str
    hashed_password: str
    noHP: str
    tanggalLahir: datetime.date
    gender: Gender
    
    class Config:
        orm_mode = True

class Review(BaseModel):
    ID_Reviewer: int
    ID_Booking: int
    hasil_review: str = ''
    isDone: str

    class Config:
        orm_mode = True


class Transaksi(BaseModel):
    Metode_Pembayaran: str
    Bukti_Pembayaran: bool
    ID_Booking: int
    
    class Config:
        orm_mode = True
    

class Booking(BaseModel):
    ID_Booking: int
    ID_Pemesan: int
    cv: str = ''
    tgl_pesan: datetime.datetime
    
    class Config:
        orm_mode = True


class Paket(BaseModel):
    ID_Paket: int    
    durasi: int
    jumlah_cv: int = 1
    harga: int = None

    class Config:
        orm_mode = True


class TuteersBooking(Tuteers):
    pesanan: List[Booking] = []
    class Config:
        orm_mode = True

class ReviewerCVReview(Reviewer):
    ongoing_reviews: List[Review] = []

    class Config:
        orm_mode = True

