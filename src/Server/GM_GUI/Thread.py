import time 
from PyQt5.QtCore import QThread, pyqtSignal

class Thread(QThread):
    data = pyqtSignal()

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True

    def run(self):
        while self.isRunning:
            self.data.emit()
            time.sleep(1)

    def stop(self):
        self.running = False