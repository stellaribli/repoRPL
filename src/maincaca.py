import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox, QMainWindow
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
import urllib
import json
import os
import os.path
import requests

cur = db.connect()

class MainReviewer2(QDialog, QMainWindow):
    def __init__(self):
        super(MainReviewer2,self).__init__()
        loadUi('reviewercus.ui',self)  
        self.tabelsemuapesanan.setColumnWidth(0,180) 
        self.tabelsemuapesanan.setColumnWidth(1,280) 
        self.tabelsemuapesanan.setColumnWidth(2,280)  
        self.buttonpesanan.clicked.connect(self.gotomain1)
        self.buttonunduh.clicked.connect(self.download_cv)
        self.buttonunggah.clicked.connect(self.upload_cv)
        self.load_data()


    def load_data(self):
        cur_user_id = 1
        headers = {'Accept': 'application/json'}
        req = requests.get(f'http://tuciwir.azurewebsites.net/reviewerbookingdia?id_reviewer={cur_user_id}', headers=headers)
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

    def download_cv(self):
        booking_id = int(self.inputpilih.text())
        header={'Content-Type': 'application/json'}
        try:
            request = requests.get(f'http://tuciwir.azurewebsites.net/reviewerdownloadcv/download-cv?booking_id={booking_id}', headers=header)
            filename_raw = request.headers['Content-Disposition'].split('filename="')[1]
            filename = filename_raw.split('"')[0]
            options = QFileDialog.Options()
            file = QFileDialog.getSaveFileName(self, "Save File", filename, "PDF Files (*.pdf)", options=options)
            if file[0]:
                with open(file[0], 'wb') as f:
                    f.write(request.content)
                QMessageBox.information(self, 'Success', 'CV has been downloaded')
        except requests.exceptions.ConnectionError as r:
            r.status_code = "Connection refused"
            print(r.status_code)
    
    def upload_cv(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Upload CV File", "", "PDF Files (*.pdf)")
        if fileName:
            self.uploadedFile = fileName
            self.fileName.setText(os.path.basename(fileName))
            self.delete_button.show()
            QMessageBox.information(self, 'Success', 'CV has been uploaded')

    def gotomain1(self):
        mainreviewer1=MainReviewer1()
        widget.addWidget(mainreviewer1)
        widget.setCurrentIndex(widget.currentIndex()+1)

class MainReviewer1(QDialog, QMainWindow):
    def __init__(self):
        super(MainReviewer1,self).__init__()
        loadUi('reviewerall.ui',self)  
        self.tabelsemuapesanan.setColumnWidth(0,180) 
        self.tabelsemuapesanan.setColumnWidth(1,280) 
        self.tabelsemuapesanan.setColumnWidth(2,280)
        self.buttonpesanandia.clicked.connect(self.gotomain2)
        self.buttonpilih.clicked.connect(self.ambilpilihan)
        self.load_data1()

    def load_data1(self):
        headers = {'Accept': 'application/json'}
        req = requests.get('http://tuciwir.azurewebsites.net/reviewerbooking', headers=headers)
        booking_data = req.json()
        self.tabelsemuapesanan.setRowCount(len(booking_data))
        row = 0
        a="Belum Direview"
        for booking in (booking_data):
            self.tabelsemuapesanan.setItem(row, 0, QtWidgets.QTableWidgetItem(str(booking['ID_Booking'])))
            self.tabelsemuapesanan.setItem(row, 1, QtWidgets.QTableWidgetItem(str(booking['tgl'])))
            self.tabelsemuapesanan.setItem(row, 2, QtWidgets.QTableWidgetItem(a))
            row += 1

    def ambilpilihan(self):
        cur_user_id = 1
        # global cur_user_id
        id_booking=self.inputpilih.text()
        masukan = {'id_reviewer':cur_user_id, 'id_booking': id_booking}
        parsed = (urllib.parse.urlencode(masukan))
        url = 'http://tuciwir.azurewebsites.net/reviewerpilihbooking?' + parsed
        requests.post(url)
        QMessageBox.information(self, 'Success', 'Booking has been chosen')

    def gotomain2(self):
        mainreviewer2=MainReviewer2()
        widget.addWidget(mainreviewer2)
        widget.setCurrentIndex(widget.currentIndex()+1)

app=QApplication(sys.argv)
mainreviewer=MainReviewer2()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainreviewer)
widget.setFixedWidth(1280)
widget.setFixedHeight(720)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exit")