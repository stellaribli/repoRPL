import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from re import search
from typing import List
# from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
# from sqlalchemy.orm import Session
# import psycopg2
# import sys
# sys.path.insert(0, './src')
# import models
# import schemas
# from database import db
# from fastapi.responses import FileResponse
# import shutil
# import json
# import os
# import os.path
import requests

class Test(QDialog):
    def __init__(self):
        super(Test,self).__init__()
        loadUi('login.ui',self)    

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi('login.ui',self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        
    def loginfunction(self):
        email=self.email.text()
        password=self.password.text()
        print("Successfully logged in with email: ", email, "and password:", password)
        
        data = requests.get('http://127.0.0.1:8000/booking')
        print(data.json())

    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

data = requests.get('http://127.0.0.1:8000/testt')
print(data.json())

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginaccbutton.clicked.connect(self.gotologin)


    def createaccfunction(self):
        if self.password.text()==self.confirmpass.text():
            namalengkap = self.namalengkap.text()
            email = self.email.text()
            year = self.year.text()
            month = self.month.text()
            date = self.date.text()
            jeniskelamin = self.jeniskelamin.text()
            nomorhp = self.nomorhp.text()
            password=self.password.text()
            confirmpass = self.confirmpass.text()

            url = 'http://127.0.0.1:8000/registerSQL?name=' + namalengkap + '&email=' + email + '&password=' + password + '&reenterpass=' + confirmpass + '&noHP=' + nomorhp + '&year=' + year + '&month=' + month + '&date=' + date + '&gender=' + jeniskelamin
            requests.post(url)
            print("Successfully created acc with email: ", email)

            # text_file = open("login.txt", "w")
            # text_file.write(namalengkap + '\n')
            # text_file.write(email + '\n')
            # text_file.write(tanggallahir + '\n')
            # text_file.write(jeniskelamin + '\n')
            # text_file.write(nomorhp + '\n')
            # text_file.write(password)
            # text_file.close()
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            print("Password Berbeda!")

    def gotologin(self):
        loginacc=Login()
        widget.addWidget(loginacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

app=QApplication(sys.argv)
mainwindow=CreateAcc()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1435)
widget.setFixedHeight(800)
widget.show()
app.exec_()