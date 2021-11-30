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
        statusEmail = ""
        f = {'email': self.email.text()}
        parsed = (urllib.parse.urlencode(f))
        url = 'https://tuciwir.azurewebsites.net/CheckTuteersAccount?' + parsed
        urlAdmin = 'https://tuciwir.azurewebsites.net/CheckReviewerAccount?' + parsed
        if str(requests.get(url).text) == "true":
            statusEmail = "Tuteers"
        elif str(requests.get(urlAdmin).text) == "true":
            statusEmail = "Admin"
        if not self.Female.isChecked() and not self.Male.isChecked(): 
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Pastikan semua field sudah terisi!')
            msg.exec_() 
        else:   
            if self.namalengkap.text() == "" or self.email.text() == "" or self.year.text() == "" or self.month.text()=="" or self.date.text() == "" or self.nomorhp.text() == "" or self.password.text() == "" or self.confirmpass.text() == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Pastikan semua field sudah terisi!')
                msg.exec_()  
            elif statusEmail == "Tuteers": 
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Akun anda sudah terdaftar!')
                msg.exec_()  
            elif statusEmail == "Admin": 
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Akun anda sudah terdaftar sebagai admin!')
                msg.exec_()                            
            elif self.password.text()!=self.confirmpass.text():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Input Password Salah!')
                msg.exec_()
            else: 
                if self.Female.isChecked():
                    jeniskelamin = "Female"
                elif self.Male.isChecked():
                    jeniskelamin = "Male"
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
                url = 'https://tuciwir.azurewebsites.net/registerSQL?' + parsed
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
