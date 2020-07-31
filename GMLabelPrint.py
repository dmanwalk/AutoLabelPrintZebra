# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GmLabelPrinting.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
#Created by Damian Walker 6/16/20 
#For Hatch

from PyQt5 import QtCore, QtGui, QtWidgets
import socket
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
import time
#init class for the UI 
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(706, 384)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(130, 10, 391, 81))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.printExecute = QtWidgets.QPushButton(Form)
        self.printExecute.setGeometry(QtCore.QRect(200, 210, 271, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.printExecute.setFont(font)
        self.printExecute.setStyleSheet("background: green")
        self.printExecute.setObjectName("printExecute")
        self.qtyToPrint = QtWidgets.QLabel(Form)
        self.qtyToPrint.setGeometry(QtCore.QRect(220, 80, 171, 121))
        font = QtGui.QFont()
        font.setPointSize(45)
        font.setBold(False)
        font.setWeight(50)
        self.qtyToPrint.setFont(font)
        self.qtyToPrint.setFrameShape(QtWidgets.QFrame.Panel)
        self.qtyToPrint.setFrameShadow(QtWidgets.QFrame.Plain)
        self.qtyToPrint.setLineWidth(2)
        self.qtyToPrint.setAlignment(QtCore.Qt.AlignCenter)
        self.qtyToPrint.setObjectName("qtyToPrint")
        self.addQty = QtWidgets.QPushButton(Form)
        self.addQty.setGeometry(QtCore.QRect(400, 80, 71, 51))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.addQty.setFont(font)
        self.addQty.setObjectName("addQty")
        self.subQty = QtWidgets.QPushButton(Form)
        self.subQty.setGeometry(QtCore.QRect(400, 150, 71, 51))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.subQty.setFont(font)
        self.subQty.setObjectName("subQty")
        self.scannerInput = QtWidgets.QLineEdit(Form)
        self.scannerInput.setGeometry(QtCore.QRect(180, 330, 301, 31))
        self.scannerInput.setStyleSheet("background: rgb(250, 250, 250)")
        self.scannerInput.setObjectName("scannerInput")
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(16)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        #button functions
        self.addQty.clicked.connect(self.addPrint)
        #open popup for workcenter popup
        self.subQty.clicked.connect(self.subPrint)
        #get contents of line edit box when enter is pressed
        self.printExecute.clicked.connect(self.printLabels)
        #get contents of line edit box when enter is pressed
        self.scannerInput.returnPressed.connect(self.scanEntered)
        self.currentQty = 0 

    #I copied this from the serialized scan program dont judge this is basically to change the IP address of the printer on the fly 
    def scanEntered(self):
        scannedInput = self.scannerInput.text()
        self.scannerInput.clear()
        i = 0
        period = 0
        print(scannedInput)
        while i < len(scannedInput)-1:
            if scannedInput[i] == ".":
                period +=1
            i+=1

        if period == 3:
            self.host = scannedInput
            print("Print host changed")

#button logic for adding to the QTY to be printed
    def addPrint(self):
        if (self.currentQty <= 100):
            self.currentQty+=1
            self.qtyToPrint.setText(str(self.currentQty))
    
    def subPrint(self):
        if (self.currentQty>0):
            self.currentQty -=1
            self.qtyToPrint.setText(str(self.currentQty))
        else:
            pass
        #prints the actual labels in a while loop depending on the qty selected
    def printLabels(self):
        
        printedQty = 0
        while (printedQty < self.currentQty):
            self.qtyToPrint.setText(str(self.currentQty))
            mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         
            self.host = "10.2.1.136" 
            port = 9100  

            try:           
                mysocket.connect((self.host, port)) #connecting to host
                #ZPL for barcode look up online zpl viewer if you wanna see how it is supposed to look
                mysocket.send(b"""^XA
                                    ^MMT
                                    ^PW1146
                                    ^LL0354
                                    ^LS0
                                    ^BY240,240^FT809,291^BXN,20,200,0,0,1,~
                                    ^FH\^FD84824440^FS
                                    ^BY240,240^FT434,290^BXN,20,200,0,0,1,~
                                    ^FH\^FD84824440^FS
                                    ^BY240,240^FT56,291^BXN,20,200,0,0,1,~
                                    ^FH\^FD84824440^FS
                                    ^PQ1,0,1,Y^XZ

                """)#using bytes
                mysocket.close() #closing connection
                self.currentQty -=1
                self.qtyToPrint.setText(str(self.currentQty))
                time.sleep(2)

            except:
                self.errorMessageName = "Error Connecting to printer. Please verify both this computer, and the printer are plugged in and connnected to the internet. If problem persists, please contact the Hatch IT Department and put in a ticket."
                ErrorMessage(self)

                if (self.currentQty > 0):     
                    self.currentQty -=1 
                #end if 
            time.sleep(1)
                
                    #end while
            #end while
        self.currentQty = 0
        self.qtyToPrint.setText(str(self.currentQty))
        
    



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Bosch Label Printing Program"))
        self.printExecute.setText(_translate("Form", "Print"))
        self.qtyToPrint.setText(_translate("Form", "0"))
        self.addQty.setText(_translate("Form", "+"))
        self.subQty.setText(_translate("Form", "-"))
        
def ErrorMessage(self):
    print("Error Activiated")
    self.msg = QMessageBox()
    self.msg.setWindowTitle("ERROR")
    self.msg.setText(str(self.errorMessageName))
    self.msg.setIcon(QMessageBox.Warning)
    errorMsg = QtWidgets.QMessageBox()
    errorMsg.setObjectName("errorMsg")
    self.msg.setStandardButtons(QMessageBox.Cancel)
    self.x = self.msg.exec_()
    #end error message popup

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
