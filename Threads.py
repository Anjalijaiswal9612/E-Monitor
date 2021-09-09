from PyQt5 import QtCore
import time, backEnd
from ctypes import Structure, windll, c_uint, sizeof, byref

class Threads():
    def __init__(self, ui, logic):
        self.signals = logic
        self.ui= ui
        self.threadpool = QtCore.QThreadPool() 

    def runTimer (self):
        self.Timer = timeThread(self.ui)
        self.threadpool.start(self.Timer)

    def stratMonitoring  (self, timelaps):
        self.Data = dataThread(self.ui, timelaps)
        self.threadpool.start(self.Data)
    
    def checkIdealness (self):
        self.checkIfIdeal = checkForIdeal(self.ui, self.signals)
        self.threadpool.start(self.checkIfIdeal)

##############################################################################
#""" To Strat Application Timer """#
class timeThread(QtCore.QRunnable):
    def __init__(self, view):        # Initialise variables
        super(timeThread, self).__init__()
        self.ui = view
        self.time = time
        self.sec = 0
        self.min = 0
        self.hr = 0
    def run(self):      # timeThread run Blue-pritn
        print("ok yoh")
        while(not self.ui.start.isEnabled()):
            self.update_HM()
            time.sleep(1)
    def update_HM(self):        # Upadate  Timer
        self.sec += 1
        if self.sec >= 60:      #check if second needs to be reset
            self.sec = 0
            self.min += 1 # 60sec = 1min
            self.update(self.min, "M")
            if self.min >= 60:       #check if second needs to be reset
                self.min = 0
                self.hr += 1 
                self.update(self.min, "M")
                self.update(self.hr, "H")
        # else:
            # self.update(self.sec, "S")       # Call back function to Update seconds
    
    def update(self, value, target):        # Update the timer label
        # if target == "S":
        #     if value%2 == 0:
        #         self.ui.Isec.setText("")
        #     else:
        #         self.ui.Isec.setText("🟤")
        #     # self.ui.sec.setText("{:0>2d}".format(value))
        if target == "M":
            hr, min = (self.ui.timer.text()).split(":")
            time = hr +":"+ "{:0>2d}".format(value)
            self.ui.timer.setText(time)
        else:
            hr, min = (self.ui.timer.text()).split(":")
            time = "{:0>2d}".format(value) +":"+ min
            self.ui.timer.setText(time)
##############################################################################

#'''Threading for Monitoring Employees '''#
class dataThread(QtCore.QRunnable):
    def __init__(self, view, timelaps):       #Pass the userID for support initialisation
        super(dataThread, self).__init__()
        self.ui = view
        self.lapse = int(timelaps)
        self.support = backEnd.support(view.Id.text())
        
    def run(self):       # dataThread run Blue-pritn
        # self.support.connectGD()        # Authinthicate connection for google
        while not self.ui.start.isEnabled():    
            self.support.takeScreenshot()       # Call function form support
            time.sleep(self.lapse*60)   # laps should be *60 as the info provided is in min
##############################################################################
            
# =============================================================================
# #''' THREAD TO AUTHENTICATE USER LOGIN '''#
# class Authenticate(QtCore.QRunnable):
#     def __init__(self, cID, eID):
#        

#         self.data = {
#             "copid":cID,
#             "eid":eID
#         }
#         
#     def run(self):
#         API_ENDPOINT = " https://www.emonitor.cbascorp.com/api/comp/empcheck"
#       
#         # sending post request and saving response as response object
#         print("sending") 
#         r = requests.post(url = API_ENDPOINT, data = self.data) 
#         print(r)
#         # extracting response text  
#         try:
#             res = json.loads(r.text) 
#             pprint.pprint(res)
#             global captime, capurl, cappath
#             captime = res[0]['captime']
#             capurl = res[0]['capurl']
#             cappath = res[0]['cappath']
#             return True
#         except Exception:
#             pprint.pprint(res)
#             return False
# =============================================================================
            
#"""  Thread to check if user is ideal or not """#
class checkForIdeal(QtCore.QRunnable):
    def __init__(self, view, signal):
        super(checkForIdeal, self).__init__()
        self.ui = view
        self.signal = signal
    
    def run(self):
        while(True):
            x = get_idle_duration()
            if x > 10 :
                print("ideal")
                self.signal.Ideal()
                time.sleep(10*60)       # laps should be *60 as the info provided is in min
                if (self.ui.windowOpacity()) == 0.8 :
                    print("closing warning")
                    self.signal.close()
                    break
            time.sleep(2*60)    # laps should be *60 as the info provided is in min     
                                
            
            
        
        
class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0
