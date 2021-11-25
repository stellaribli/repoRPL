from datetime import timezone
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import DATE, DATETIME, TIMESTAMP, Enum
import enum

from database import Base


class GenderEnum(enum.Enum):
    Male = 0
    Female = 1 


class Tuteers(Base):
    __tablename__ = "tuteers"

    ID_Tuteers = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashedPassword = Column(String, nullable=False)
    noHP = Column(String, nullable=False)
    tanggalLahir = Column(DATE, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)

    pesanan = relationship("Booking", back_populates="tuteers")


class Reviewer(Base):
    __tablename__ = "reviewer"

    ID_Reviewer = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashedPassword = Column(String, nullable=False)
    noHP = Column(String, nullable=False)
    tanggalLahir = Column(DATE, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)

    mereview = relationship("Review", back_populates="reviewer")


class Review(Base):
    __tablename__ = 'review'

    ID_Reviewer = Column(Integer, ForeignKey("reviewer.ID_Reviewer"), primary_key=True, index=True)
    ID_Booking = Column(Integer, ForeignKey("booking.ID_Booking"), primary_key=True, index=True)
    Hasil_Review = Column(String, nullable=True) #hasil reviewnya bentukannya link aja
    isDone = Column(Boolean, default=False)

    direview = relationship("Reviewer", back_populates="review")
    melakukan_booking = relationship("Booking", back_populates="review")


class Booking(Base):
    __tablename__ = "booking"

    ID_Booking = Column(Integer, primary_key=True, index=True)
    ID_Paket = Column(Integer, ForeignKey("paket.ID_Paket"))
    ID_Tuteers = Column(Integer, ForeignKey("tuteers.ID_Tuteers"))
    cv = Column(String) #jadinya link aja deh
    tgl_pesan = Column(TIMESTAMP(timezone=False),nullable=False)
    
    
    pemesan = relationship("Tuteers", back_populates="booking")
    booking_transaction = relationship("Transaksi", back_populates="booking", uselist=False)
    dilakukan_review = relationship("Review", back_populates="review", uselist=False)
    paket_booking = relationship("Paket", back_populates="booking")


class Transaksi(Base):
    __tablename__ = "transaksi"

    ID_Transaksi = Column(Integer, primary_key=True, index=True)
    ID_Booking = Column(Integer, ForeignKey("booking.ID_Booking"))
    Metode_Pembayaran = Column(String, nullable=False)
    Bukti_Pembayaran = Column(Boolean, default=False)

    transaction_of_booking = relationship("Booking", back_populates="transaksi")


class Paket(Base):
    __tablename__ = "paket"

    ID_Paket = Column(Integer, primary_key=True, index=True)
    durasi = Column(Integer, nullable=False)
    jumlah_cv = Column(Integer, nullable=False, default=1)
    harga = Column(Integer, default=0)

    booking_with_package = relationship("Booking", back_populates="paket")
