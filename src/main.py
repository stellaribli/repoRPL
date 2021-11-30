import sys
from PyQt5.QtWidgets import QFileDialog, QPushButton, QDialog, QApplication, QWidget, QLabel, QMainWindow, QMessageBox, QCheckBox, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from typing import List
import requests
import urllib
import json
from PyQt5 import QtCore, QtGui, QtWidgets
import PyPDF2
import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QMessageBox, QPushButton, QLabel
sys.path.insert(0, './src')
import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QLabel, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from re import search
from typing import List
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import psycopg2
import sys
sys.path.insert(0, './src')
import models
import schemas
from database import db
from fastapi.responses import FileResponse
import shutil
import json
import os
import os.path
import requests


cur_booking_id = 1
cur_user_ID = 1
loggedin = False
currentUser = ''
currentName = ''
booking_id = 2

#Stella
class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi('login.ui',self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        self.loginaccbutton_3.clicked.connect(self.gotoreset)

    def loginfunction(self):
        email=self.email.text()
        password=self.password.text()
        f = {'email' : email, 'password' : password}
        parsed = (urllib.parse.urlencode(f))
        url = 'http://127.0.0.1:8000/login?' + parsed
        hasil =  requests.get(url)
        x = str(hasil.text)
        global loggedin
        global currentUser 
        global currentName
        global cur_user_ID
        if hasil.text == "true":
            loggedin = True
            f = {'em' : email}
            parsed = (urllib.parse.urlencode(f))
            url = 'http://127.0.0.1:8000/ambilDataTuteers?' + parsed
            hasil =  requests.get(url)
            currentUser = hasil.json()
            currentName = currentUser['nama']
            cur_user_ID = currentUser['ID_Tuteers']
            print(cur_user_ID)
            widget.setCurrentIndex(4) #Nanti diganti jadi ke tuteers
            
            self.email.setText("")
            self.password.setText("")
            # print(currentName)
        else:
            url = 'http://127.0.0.1:8000/loginadmin?' + parsed
            hasil =  requests.get(url)
            if hasil.text == "true":
                loggedin = True
                f = {'em' : email}
                parsed = (urllib.parse.urlencode(f))
                url = 'http://127.0.0.1:8000/ambilDataReviewer?' + parsed
                hasil =  requests.get(url)
                currentUser = hasil.json()
                # print(currentUser)
                widget.setCurrentIndex(3) #nanti diganti ke admin
                
                self.email.setText("")
                self.password.setText("")
            else:
                loggedin = False
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Login Tidak Berhasil!')
                msg.exec_()
        return

    def gotocreate(self):
        widget.setCurrentIndex(1)
        
        self.email.setText("")
        self.password.setText("")

    def gotoreset(self):
        widget.setCurrentIndex(2)
        
        self.email.setText("")
        self.password.setText("")

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginaccbutton.clicked.connect(self.gotologin)
    
    def createaccfunction(self):
        jeniskelamin = ""
        if self.Female.isChecked():
            jeniskelamin = "Female"
        elif self.Male.isChecked():
            jeniskelamin = "Male"

        if self.password.text()==self.confirmpass.text():
            jen = jeniskelamin
            namalengkap = self.namalengkap.text()
            email = self.email.text()
            year = self.year.text()
            month = self.month.text()
            date = self.date.text()
            nomorhp = self.nomorhp.text()
            password=self.password.text()
            confirmpass = self.confirmpass.text()
            f = {'name': namalengkap, 'email' : email, 'password' : password, 'reenterpass' : confirmpass, 'noHP':nomorhp, 'year':year, 'month':month, 'date' : date,'gender': jen}
            parsed = (urllib.parse.urlencode(f))
            url = 'http://127.0.0.1:8000/registerSQL?' + parsed
            requests.post(url)
            # QLineEdit.clear(self)
            widget.setCurrentIndex(0)
            self.namalengkap.setText("")
            self.email.setText("")
            self.year.setText("")
            self.month.setText("")
            self.date.setText("")
            self.nomorhp.setText("")
            self.password.setText("")
            self.confirmpass.setText("")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Input Password Salah!')
            msg.exec_()

    def gotologin(self):
        widget.setCurrentIndex(0)
        self.namalengkap.setText("")
        self.email.setText("")
        self.year.setText("")
        self.month.setText("")
        self.date.setText("")
        self.nomorhp.setText("")
        self.password.setText("")
        self.confirmpass.setText("")
        
class ResetPassword(QDialog):
    def __init__(self):
        super(ResetPassword,self).__init__()
        loadUi('resetpass.ui',self)  
        self.kembali.clicked.connect(self.back)
        self.simpanbutton.clicked.connect(self.resetpass)
    def resetpass(self):
        if self.passbaru.text()==self.passbaru_2.text():
            f = {'email': self.passlama.text(), 'passbaru' : self.passbaru.text()}
            parsed = (urllib.parse.urlencode(f))
            url = 'http://127.0.0.1:8000/resetPasswordSQL/?' + parsed
            requests.get(url)
            widget.setCurrentIndex(0)
            self.passbaru.setText("")
            self.passbaru_2.setText("")
            self.passlama.setText("")
    def back(self):
        widget.setCurrentIndex(0) 
        self.passbaru.setText("")
        self.passbaru_2.setText("")
        self.passlama.setText("")

class AboutUs(QDialog):
    def __init__(self):
        super(AboutUs,self).__init__()
        loadUi('aboutus.ui',self) 
        # self.logoutbutton.setText(currentName) 
        # self.usr()
        # self.show()
        # self.logoutbutton.clicked.connect(currentName) 
        self.logoutbutton.clicked.connect(self.gotologin)     
        self.aboutmebutton.clicked.connect(self.gotoaboutus) 
        
    # def usr(self): 
    #     global currentName
    #     print(currentName)
    #     self.show()

    def gotologin(self):
        global loggedin
        loggedin = False
        widget.setCurrentIndex(0)

    # def gotolayanan(self):
    #     widget.setCurrentIndex(#lalaalala)

    def gotoaboutus(self):
        widget.setCurrentIndex(3)
         

#Tugus
class HomeScreen(QMainWindow):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi('homescreen.ui', self)
        self.setWindowTitle('Home Screen')
        self.bookingButton.clicked.connect(self.goToBooking)
        self.statusPesananButton.clicked.connect(self.goToStatus)
    

    def goToBooking(self):
        
        widget.setCurrentIndex(6)
        QMessageBox.about(self, "Info", "Go to booking")
    
    def goToStatus(self):
        QMessageBox.about(self, "Info", "Go to status")

class UploadCV(QDialog):
    def __init__(self):
        super(UploadCV, self).__init__()
        loadUi("uploadcv.ui", self)
        print("uploadcv " + str(cur_booking_id))
        print("uploadcv " + str(cur_user_ID))
        print("uploadcv " + str(self.getPaketBooking(cur_booking_id)))
        self.setWindowTitle('Upload CV')
        self.uploadButton.clicked.connect(self.uploadCV)
        self.uploadedFile = None
        self.dataPaket = self.getPaketBooking(cur_booking_id)
        self.submitBookingButton.clicked.connect(lambda: self.submitBooking(cur_booking_id))
        self.jmlCV.setText(str(self.dataPaket.json()['jumlah_cv']) + "CV")
        self.jmlHari.setText(str(self.dataPaket.json()['durasi']) + " Hari")
        self.rincian.setText("Paket " + str(self.dataPaket.json()['jumlah_cv']) + " CV " + str(self.dataPaket.json()['durasi']) + " Hari")
        self.harga.setText("Rp" + str(self.dataPaket.json()['harga']))
        self.bookingNumber.setText("#" + str(self.dataPaket.json()['ID_Booking']))
        self.delete_button.hide()
        self.homescreen.hide()
        self.prosesReview.hide()
        self.delete_button.clicked.connect(self.deleteCV)
        self.homescreen.clicked.connect(self.goToHomeScreen)
        self.reloadUi()

    def reloadUi(self):
        self.dataPaket = self.getPaketBooking(cur_booking_id)
        self.submitBookingButton.clicked.connect(lambda: self.submitBooking(cur_booking_id))
        self.jmlCV.setText(str(self.dataPaket.json()['jumlah_cv']) + "CV")
        self.jmlHari.setText(str(self.dataPaket.json()['durasi']) + " Hari")
        self.rincian.setText("Paket " + str(self.dataPaket.json()['jumlah_cv']) + " CV " + str(self.dataPaket.json()['durasi']) + " Hari")
        self.harga.setText("Rp" + str(self.dataPaket.json()['harga']))
        self.bookingNumber.setText("#" + str(self.dataPaket.json()['ID_Booking']))
    
    def uploadCV(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Upload CV File", "", "PDF Files (*.pdf)")
        if fileName:
            self.uploadedFile = fileName
            # print(self.uploadedFile)
            self.fileName.setText(os.path.basename(fileName))
            self.delete_button.show()

        else:
            print("No file selected")
        
    def submitBooking(self, booking_id):
        if self.uploadedFile:
            with open(self.uploadedFile, 'rb') as f:
                files = {'uploaded_file': f}
                headers = {'Accept': 'application/json'}
                request = requests.put(f'http://127.0.0.1:8000/upload-cv?booking_id={booking_id}', files=files, headers=headers)
                # print(request.status_code)
                # print(request.text)
                if (request.text[0] == "CV exists!"):
                    self.remove_CV_from_Booking(booking_id)
                    request = requests.put(f'http://127.0.0.1:8000/upload-cv?booking_id={booking_id}', files=files, headers=headers)
                    # print(request.status_code)
                    # print(request.text['message'])
                    QMessageBox.about(self, "Success", f"CV untuk booking {booking_id} berhasil di upload!")
                else:
                    QMessageBox.about(self, "Success", f"CV untuk booking {booking_id} berhasil di upload!")
                self.delete_button.hide()
                self.homescreen.show()
                self.uploadButton.hide()
                self.submitBookingButton.hide()
                self.prosesReview.show()

        else:
            QMessageBox.warning(self, "Warning", "Please upload your CV file")
    
    def getPaketBooking(self, booking_id):
        data = requests.get(f'http://127.0.0.1:8000/paket-of-booking?booking_id={booking_id}')
        return data
    
    def deleteCV(self):
        self.uploadedFile = None
        self.fileName.setText("No File Uploaded!")
        self.delete_button.hide()

    def remove_CV_from_Booking(self, booking_id):
        req = requests.put(f'http://127.0.0.1:8000/remove-cv-from-booking?booking_id={booking_id}')
        # print(req.text)

    def goToHomeScreen(self):
        self.close()



#Agunk
class PilihPaket(QDialog):
    def __init__(self):
        super(PilihPaket, self).__init__()
        loadUi('paket.ui', self)
        #Paket 1
        self.PesanPaket1.clicked.connect(lambda: self.pesanpaket(1,cur_user_ID))
        self.jmlCV.setText(str(self.getPaket(1)['jumlah_cv'])+" CV")
        self.jmlHari.setText(str(self.getPaket(1)['durasi'])+" Hari")
        self.harga.setText("Rp "+ str(self.getPaket(1)['harga']))
        #Paket 2
        self.PesanPaket2.clicked.connect(lambda: self.pesanpaket(2,cur_user_ID))
        self.jmlCV_2.setText(str(self.getPaket(2)['jumlah_cv'])+" CV")
        self.jmlHari_2.setText(str(self.getPaket(2)['durasi'])+" Hari")
        self.harga_2.setText("Rp "+ str(self.getPaket(2)['harga']))
        #Paket 3
        self.PesanPaket3.clicked.connect(lambda: self.pesanpaket(3,cur_user_ID))
        self.jmlCV_3.setText(str(self.getPaket(3)['jumlah_cv'])+" CV")
        self.jmlHari_3.setText(str(self.getPaket(3)['durasi'])+" Hari")
        self.harga_3.setText("Rp "+ str(self.getPaket(3)['harga']))
        
    def pesanpaket(self, paket_id, tuteers_id):
        global cur_booking_id
        req = requests.post(f'http://127.0.0.1:8000/create-booking?paket_id={paket_id}&tuteers_id={tuteers_id}')
        if paket_id:
            print("Berhasil membuat pesanan")

            #update current id booking
            dataBooking = requests.get(f'http://127.0.0.1:8000/booking-by-tuteers_id?tuteers_id={tuteers_id}')
            booking_id = int(dataBooking.json())
            cur_booking_id = booking_id
            print("id Booking saat ini " + str(cur_booking_id))

            #go to pembayaran
            # pembayaran=Pembayaran()
            # widget.addWidget(pembayaran)
            
            widget.setCurrentIndex(7)

            #self.close()

    def getPaket(self, paket_id):
        data = requests.get(f'http://127.0.0.1:8000/paket-by-paket_id?paket_id={paket_id}')
        return data.json()
    
    def getBookingTuteers(self, tuteers_id):
        data = requests.get(f'http://127.0.0.1:8000/booking-by-tuteers_id?tuteers_id={tuteers_id}')
        return data.json()

class Pembayaran(QDialog):
    def __init__(self):
        super(Pembayaran, self).__init__()
        loadUi('transaksi.ui', self)
        print(cur_booking_id)
        print(self.getPaketofBooking(cur_booking_id))
        self.bayar.clicked.connect(lambda: self.pembayaran(cur_booking_id))
        self.cancel.clicked.connect(lambda: self.BatalPesanan(cur_booking_id))
        self.rincian.setText("Paket " + str(self.getPaketofBooking(cur_booking_id)['jumlah_cv']) + " CV - " + str(self.getPaketofBooking(cur_booking_id)['durasi']) + " Hari")
        self.harga.setText("Rp "+ str(self.getPaketofBooking(cur_booking_id)['harga']))
        self.bookingNumber.setText("#" + str(self.getBooking(cur_booking_id)['ID_Booking']))
        self.reloadUi()

    def reloadUi(self):
        self.rincian.setText("Paket " + str(self.getPaketofBooking(cur_booking_id)['jumlah_cv']) + " CV - " + str(self.getPaketofBooking(cur_booking_id)['durasi']) + " Hari")
        self.harga.setText("Rp "+ str(self.getPaketofBooking(cur_booking_id)['harga']))
        self.bookingNumber.setText("#" + str(self.getBooking(cur_booking_id)['ID_Booking']))
    

    def pembayaran(self,booking_id):
        req = requests.post(f'http://127.0.0.1:8000/create-transaksi?booking_id={booking_id}')
        if booking_id:
            print("berhasil melakukan pembayaran untuk No.Booking "+str(booking_id))
            
            widget.setCurrentIndex(5)
            

    def BatalPesanan(self, booking_id):
        req = requests.delete(f'http://127.0.0.1:8000/delete-booking-by-booking_id?booking_id={booking_id}')
        if booking_id:
            print("berhasil membatalkan pesanan dengan No. Booking "+str(booking_id))
            pilihpaket = PilihPaket()
            widget.addWidget(pilihpaket)
            widget.setCurrentIndex(6)
            
            #self.close()

    def getPaketofBooking(self, booking_id):
        data = requests.get(f'http://127.0.0.1:8000/paket-of-booking?booking_id={booking_id}')
        return data.json()
    
    def getBooking(self, booking_id):
        data = requests.get(f'http://127.0.0.1:8000/booking-by-booking_id?booking_id={booking_id}')
        return data.json()

#CacCAA
class MainReviewer2(QDialog, QMainWindow):
    def __init__(self):
        super(MainReviewer2,self).__init__()
        loadUi('reviewercus.ui',self)  
        # ui = MainReviewer()
        # ui.setupUi(self)
        self.tabelsemuapesanan.setColumnWidth(0,200) 
        self.tabelsemuapesanan.setColumnWidth(1,400) 
        self.tabelsemuapesanan.setColumnWidth(2,300) 
        self.buttonpesanan.clicked.connect(self.gotomain1)
        self.load_data()

    def load_data(self):
        headers = {'Accept': 'application/json'}
        req = requests.get('http://127.0.0.1:8000/reviewerbookingdia?reviewer_id=1', headers=headers)
        booking_data = req.json()
        self.tabelsemuapesanan.setRowCount(len(booking_data))
        row = 0
        for booking in (booking_data):
            a=str(booking['isDone'])
            if a=="True":
                a="Review Selesai"
            else:
                a="Dalam Review"
            self.tabelsemuapesanan.setItem(row, 0, QtWidgets.QTableWidgetItem(str(booking['ID_Booking'])))
            self.tabelsemuapesanan.setItem(row, 1, QtWidgets.QTableWidgetItem(str(booking['tgl'])))
            self.tabelsemuapesanan.setItem(row, 2, QtWidgets.QTableWidgetItem(a))
            row += 1
    
    def gotomain1(self):
        mainreviewer1=MainReviewer1()
        widget.addWidget(mainreviewer1)
        widget.setCurrentIndex(widget.currentIndex()+1)

class MainReviewer1(QDialog, QMainWindow):
    def __init__(self):
        super(MainReviewer1,self).__init__()
        loadUi('reviewerall.ui',self)  
        # ui = MainReviewer()
        # ui.setupUi(self)
        self.tabelsemuapesanan.setColumnWidth(0,200) 
        self.tabelsemuapesanan.setColumnWidth(1,400) 
        self.tabelsemuapesanan.setColumnWidth(2,300) 
        self.buttonpesanandia.clicked.connect(self.gotomain2)
        self.load_data1()

    def load_data1(self):
        headers = {'Accept': 'application/json'}
        req = requests.get('http://127.0.0.1:8000/reviewerbooking', headers=headers)
        booking_data = req.json()
        self.tabelsemuapesanan.setRowCount(len(booking_data))
        row = 0
        a="Belum Direview"
        for booking in (booking_data):
            self.tabelsemuapesanan.setItem(row, 0, QtWidgets.QTableWidgetItem(str(booking['ID_Booking'])))
            self.tabelsemuapesanan.setItem(row, 1, QtWidgets.QTableWidgetItem(str(booking['tgl'])))
            self.tabelsemuapesanan.setItem(row, 2, QtWidgets.QTableWidgetItem(a))
            row += 1
            # btn = QPushButton(self.tabelsemuapesanan)
            # btn.setText('add')
            # self.tabelsemuapesanan.setCellWidget(booking, 4, btn)

    def gotomain2(self):
        mainreviewer2=MainReviewer2()
        widget.addWidget(mainreviewer2)
        widget.setCurrentIndex(widget.currentIndex()+1)
    

app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
widget.addWidget(Login()) #Index jadi 0
widget.addWidget(CreateAcc()) #Index jadi 1
widget.addWidget(ResetPassword()) #Index jadi 2
widget.addWidget(AboutUs())  #Index jadi 3
widget.addWidget(HomeScreen())  #Index jadi 4
widget.addWidget(UploadCV()) #Index jadi 5
widget.addWidget(PilihPaket()) #Index jadi 6
widget.addWidget(Pembayaran()) #Index jadi 7
widget.addWidget(MainReviewer1()) #Index jadi 8
widget.addWidget(MainReviewer2()) #Index jadi 9
widget.setCurrentIndex(0) 
widget.setFixedWidth(1280)
widget.setFixedHeight(720)
widget.show()
app.exec_()
