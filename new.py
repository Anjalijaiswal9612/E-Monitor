from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
 
class PunchingBag(QObject):
    ''' Represents a punching bag; when you punch it, it
        emits a signal that indicates that it was punched. '''
    punched = pyqtSignal()
 
    def __init__(self):
        # Initialize the PunchingBag as a QObject
        QObject.__init__(self)
 
    def punch(self):
        ''' Punch the bag '''
        self.punched.emit()
        
def say_punched():
    ''' Give evidence that a bag was punched. '''
    print('Bag was punched.')
 
bag = PunchingBag()
# Connect the bag's punched signal to the say_punched slot
bag.punched.connect(say_punched)

for i in range(10):
    bag.punch()
    print(i)
    
    

from ctypes import Structure, windll, c_uint, sizeof, byref
import time



for i in range(30):
    print(get_idle_duration())
    time.sleep(1)






