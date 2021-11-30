from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QMessageBox, QPushButton, QLabel
from PyQt5.uic import loadUi
import sys
sys.path.insert(0, './src')
import PyPDF2
import os
import requests
import shutil

class DownloadCV(QDialog):
    def __init__(self):
        super(DownloadCV, self).__init__()
        loadUi('tesdonlot.ui', self)
        self.setWindowTitle('Download CV')
        self.setWindowIcon(QtGui.QIcon('../img/logo aksel.png'))
        self.setFixedSize(self.size())
        self.downloadButton.clicked.connect(self.download_cv)
    
    
    def download_cv(self):
        booking_id = int(self.booking_id.text())
        header={'Content-Type': 'application/json'}
        try:
            request = requests.get(f'http://127.0.0.1:8000/download-cv?booking_id={booking_id}', headers=header)
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

        



app = QApplication(sys.argv)
window = DownloadCV()
window.show()
app.exec_()