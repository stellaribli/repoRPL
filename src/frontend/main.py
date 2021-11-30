import uploadcv
import login
import paket

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QMessageBox, QPushButton, QLabel
from PyQt5.uic import loadUi
import sys
sys.path.insert(0, './src')

paket.BOOKING_ID = 3


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window1 = login.Login()
    window2 = uploadcv.UploadCV()
    window1.show()
    app.exec_()