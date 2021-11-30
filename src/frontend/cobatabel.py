from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QMessageBox, QPushButton, QLabel
from PyQt5.uic import loadUi
import sys
sys.path.insert(0, './src')
import os
import requests


class TesTabel(QDialog):
    def __init__(self):
        super(TesTabel, self).__init__()
        loadUi('coba tabel.ui', self)
        self.setWindowTitle('COBA TABEL')
        self.load_data()

    def load_data(self):
        headers = {'Accept': 'application/json'}
        req = requests.get('http://127.0.0.1:8000/booking', headers=headers)
        booking_data = req.json()
        self.tableWidget.setRowCount(len(booking_data))
        row = 0
        for booking in (booking_data):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(booking['ID_Booking'])))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(booking['tgl_pesan'])))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(booking['cv'])))
            row += 1


    
app = QApplication(sys.argv)
window = TesTabel()
window.show()
app.exec_()