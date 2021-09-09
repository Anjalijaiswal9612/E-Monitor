import sys, time, backEnd, Threads
from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMessageBox  # Importing base widigts 
from PyQt5.QtWidgets import QLabel,QLineEdit, QPushButton, QFrame  # Importing aditional widgits
from PyQt5.QtCore import QObject, pyqtSignal



#''' UI '''
btnEnabledStyle ="""
    QPushButton{
    font: 75 10pt 'Microsoft YaHei UI';
    font-weight: bold;
    background-color : lightgreen;
    }
"""        
btnStyle = """
    font: 75 10pt 'Microsoft YaHei UI';
    font-weight: bold;
"""

bgStyle = """     
    background: qlineargradient( x1:10 y1:0, x2:10 y2:1, stop:0 #6262ff, stop:1 #000027);
"""

popupStyle = """     
    background: qlineargradient( x1:10 y1:0, x2:10 y2:1, stop:0 #6262ff, stop:0.4 #6262ff, stop:1 #000027);
    font: 30s 10pt 'Microsoft YaHei UI';
    font-weight: bold;
    color: #c4c4ff;
"""

titleStyle = """
    font-size: 30px;
    text-align: center;
    font-weight:600;
"""

ipStyle = """
    text-align:center;
    font-weight:300; 
    font-size:20px;
"""

class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Monitor")
        self.setGeometry(150, 200, 405, 227)
        self.setFixedSize(405, 227)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)      #Set Windowframe False
        
        bglabel = QLabel(self)      #----------------------------------- Application background QLabel
        bglabel.setGeometry(0,0, 405, 227)
        bglabel.setStyleSheet(bgStyle)
        

        # self.setLogo()  

        self.appTitle()

        self.setBtns()
        
        self.setCidField()
        
        self.setEidFeild()
        
        self.setCounter()
        
        self.connectFlag = False
        self.Connecting()

        self.setIndicator()

        self.line()

        
        # self.Lgif()
        # self.fade()
        
        '''START: code to make the window moveable'''
        self.mwidget = QWidget(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #get window size in variables
        self.center() 
        # print(self.pos())
        self.oldPos = self.pos()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    '''STOP: code to make the window moveable'''
    '''START: opening animation '''
    
    # def gif(self):      #----------------------------------- label contaning Starting GIF
    #     self.label = QLabel(self)
    #     self.label.setGeometry(0,0,405,228)
    #     self.Lgif = QtGui.QMovie("Resourses/load2.gif")
    #     self.label.setMovie(self.Lgif)
    #     self.Lgif.start()
    # def fade(self):     #----------------------------------- add faded start to the gif label
    #     self.setWindowOpacity(0.5)
    #     self.start.setStyleSheet(self.btnStyle)
    #     QtCore.QTimer.singleShot(4000, self.unfade)
    # def unfade(self):   #----------------------------------- end starting gif animation     
    #     self.setWindowOpacity(1)
    #     time.sleep(1)
    #     self.start.setStyleSheet(self.btnEnabledStyle)
    #     self.Lgif.stop()
    #     self.label.setVisible(False)
    #     self.label.setDisabled(True)
    '''STOP: opening animation '''


    """ Functions to add widgets"""
    def appTitle(self):
        label = QLabel(self)
        label.setText("E-Monitor")
        label.move(64,10)
        label.setFont(QtGui.QFont('Stalinist One')) 
        label.setStyleSheet(titleStyle)
    def setLogo(self):      #----------------------------------- set Logo of the application
        logo = QLabel(self)
        logo.setGeometry(QtCore.QRect(150, 5, 91, 91))
        logo.setText("")
        logo.setPixmap(QtGui.QPixmap("Resourses/logo.png"))
        logo.setObjectName("label")
    def setBtns(self):      #----------------------------------- Add buttons for "START" and "STOP"
        self.start = QPushButton(self)
        self.start.setGeometry(20, 160, 100, 28 )
        self.start.setText("START")
        self.start.setFocus(True)
        self.start.setStyleSheet(btnEnabledStyle)
        self.start.setObjectName("pushButton")
        self.stop = QPushButton(self)
        self.stop.setGeometry(293, 160, 100, 28 )
        self.stop.setText("STOP")
        self.stop.setDisabled(True)
        self.stop.setStyleSheet(btnStyle)
        self.stop.setObjectName("pushButton_2")
    def setCidField(self):        #----------------------------------- Text field for CorporateID
        self.CId = QLineEdit(self)
        self.CId.setGeometry(QtCore.QRect(80, 65, 241, 31))
        self.CId.setStyleSheet(ipStyle)
        self.CId.setAlignment(QtCore.Qt.AlignCenter)
        self.CId.setPlaceholderText("Enter Corporate ID")
        self.CId.setObjectName("lineEdit")
        self.CId.setFocus(False)
        self.CId.setText("cbascorpe100")
    def setEidFeild(self):        #----------------------------------- Text field for employeeID
        self.Id = QLineEdit(self)
        self.Id.setGeometry(QtCore.QRect(80, 100, 241, 31))
        self.Id.setStyleSheet(ipStyle)
        self.Id.setAlignment(QtCore.Qt.AlignCenter)
        self.Id.setPlaceholderText("Enter EMployee ID")
        self.Id.setObjectName("lineEdit")
        self.Id.setFocus(False)
        self.Id.setText("c5747")

    def setCounter(self):       #----------------------------------- Minute and Hour Counter Display
        self.timer = QLabel(self)
        self.timer.setGeometry(QtCore.QRect(140, 136, 200, 41))
        self.timer.setStyleSheet("font-weight:900; font-size:42px; color:#878787")
        self.timer.setText("00:00")
        self.timer.setObjectName("timer")
        # print(self.timer.text())
    def setIndicator(self):      #----------------------------------- Gif to indicate start recording
        Label = QLabel(self)
        Label.setGeometry(195, 190, 7, 7)
        self.rec = QtGui.QMovie("Resourses/rec.gif")
        Label.setMovie(self.rec)
        # self.rec.start()
    def Connecting(self):       #----------------------------------- Gif to indicate connection process
        label = QLabel(self)
        label.setGeometry(192, 190, 20, 20)
        self.gifConn = QtGui.QMovie("Resourses/conn.gif")
        label.setMovie(self.gifConn)
        # self.gifConn.start()
    def line(self):     #----------------------------------- Bottom Vertical line
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setGeometry(0, 220, 405,2)
   
            
        
""" Defining GUI logic Proceses """
    
class Model():  
    def __init__(self, view, signal):
        self.ui = view
        signal.isIdeal.connect(self.Ideal)
        signal.closeApp.connect(self.closeWindow)
        view.start.clicked.connect(self.Start)
        view.stop.clicked.connect(self.Stop)
        self.bgProcess = Threads.Threads(view, signal)
        self.HC = view.pos().x()+90     # Horizontal Center of main Window for msgbox 
        self.VC = view.pos().y()+50    # Vertical Center of main Window for msgbox
    def SSAnimation(self, T_F, startBtnStyle, stopBtnStyle):                               # START          ⬇    
        self.ui.start.setDisabled(T_F)     #----------------------------------------------START DISABLE     ⬇    
        self.ui.start.setStyleSheet(startBtnStyle) #------------------------------------START SYTLE CHANGE  ⬇   
        self.ui.Id.setDisabled(T_F)        #---------------------------------------------ID I/P DISABLE     ⬇
        self.ui.CId.setDisabled(T_F)       #---------------------------------------------CID I/P DISABLE    ⬇
        self.ui.stop.setEnabled(T_F)       #-----------------------------------------------ENABLE STOP      ⬇
        self.ui.stop.setStyleSheet(stopBtnStyle)
        
    def Start(self):        #------------------------------------------------------------------- START button functionality  
        print(self.ui.Id.text())        
        if self.ui.Id.text() == "" or self.ui.CId.text() == "":     #--------- Check if Name has been entered
            msg = QMessageBox()     
            msg.move(self.HC, self.VC)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("ID Fild Empty")
            msg.setInformativeText("Please,\nEnter yor Employee ID")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setStyleSheet(popupStyle)  
            msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            msg.exec()      #----------------------------------- No ID found display error 
        else:                                                  
            self.SSAnimation(True, btnStyle, btnEnabledStyle)
            self.ui.gifConn.start()
            ##############
            res = backEnd.Authenticate(self.ui.Id.text(), self.ui.CId.text())
            if res[0]:     #--- Check for valid EID and CID
                print("authenticated")
                self.ui.rec.start()   
                self.ui.gifConn.stop()
                self.bgProcess.runTimer()       #----------------------------------- Run Timer thread
                self.bgProcess.stratMonitoring(res[1])        #------------------------- Run Monitor Thread 
                self.bgProcess.checkIdealness()
            else:
                print("Not Valid")
                self.ui.Id.setText = ""
                self.ui.CId.setText = ""
    # STOP button functionality           
    def Stop (self):
        self.closemsgs("Confirm", "Are you sure you want to end this session?",QMessageBox.Yes|QMessageBox.No)
        #Connect msg bttons
    
    def Ideal(self):
        self.closemsgs("Ideal for too Long !!", "Your session will expire in 10 sec.\nIf u continur to remain ideal", QMessageBox.Ok)
    
    def closeDecission(self, i):      # Call back function on Yes btn clicked for self.msg
        print(i.text())
        if(i.text() == "&Yes"):
            self.closeWindow()      # Call back function to close WIndow
        else:
            self.ui.setWindowOpacity(1)     # set back the window opacity
            
    def closemsgs(self, Title, Body, btns):     #-------------------------------------Closing Confirmation message
        self.ui.setWindowOpacity(0.8)
        self.msg = QMessageBox()         # Confirmation msg box
        self.msg.move(self.HC, self.VC)
        self.msg.setIcon(QMessageBox.Question)
        self.msg.setText(Title)
        self.msg.setInformativeText(Body)
        self.msg.setStandardButtons(btns)
        self.msg.setDefaultButton(QMessageBox.Cancel)
        self.msg.setObjectName("body")
        self.msg.setStyleSheet(popupStyle)
        self.msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.msg.buttonClicked.connect(self.closeDecission)
        self.msg.exec()
    
    def closeWindow(self):      #-------------------------------------------------------Closing the windiw Application
        self.msg.close()
        self.ui.stop.setDisabled(True)
        self.ui.stop.setStyleSheet(btnStyle)
        self.ui.Id.setEnabled(True)
        self.ui.start.setEnabled(True)
        self.ui.start.setStyleSheet(btnEnabledStyle)
        self.ui.timer.setStyleSheet("font-weight:900; font-size:42px; color:#878787")
        self.ui.setWindowOpacity(0.5)
        time.sleep(1)
        self.ui.close()
        
        
class Logic(QObject):
    
   # =============================================================================
    isIdeal = pyqtSignal()
    closeApp = pyqtSignal()
   # =============================================================================
    
    def __init__(self):
        QObject.__init__(self)      #----------------------------------------------- Initialize the isIdeal as a QObject
     
    def Ideal(self):
        ''' The user is idele '''
        self.isIdeal.emit()
    def close(self):
        ''' Close the application '''
        self.closeApp.emit()
    



if __name__ == '__main__':
    app = QApplication([])
    
    QtGui.QFontDatabase.addApplicationFont("Resourses/StalinistOne-Regular.ttf")
    home = UI()
    home.show()
    Signals = Logic() # functionality(home)
    model = Model(home, Signals)
    sys.exit(app.exec_())
        