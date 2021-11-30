from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QMessageBox, QPushButton, QLabel
from PyQt5.uic import loadUi
import sys
sys.path.insert(0, './src')
import PyPDF2
import os
import requests

BOOKING_ID = 0
TUTEERS_ID = 0

class PilihPaket(QDialog):
    def __init__(self):
        super(PilihPaket, self).__init__()
        loadUi('paket.ui', self)
        self.pesanPaket1.clicked.connect(lambda: self.pilih1(1,1))
        self.jmlCV.setText(str(self.getPaket(1)['jumlah_cv']))
        self.durasi.setText(str(self.getPaket(1)['durasi']))
        self.harga.setText("Rp"+ str(self.getPaket(1)['harga']))
        

    def pilih1(self, tuteers_id, paket_id):
        # req = requests.get(f'http://127.0.0:8000/create-booking?paket_id={paket_id}&tuteers_id={tuteers_id}')
        if paket_id:
            print("berhasil")
            self.close()
    def getPaket(self, booking_id):
        data = requests.get(f'http://127.0.0.1:8000/paket-of-booking?booking_id={booking_id}')
        return data.json()

app = QApplication(sys.argv)
window = PilihPaket()
window.show()
app.exec_()