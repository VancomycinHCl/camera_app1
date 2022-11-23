import logging
import time

import PyQt5.QtCore,PyQt5.QtWidgets
from record import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from initSetting import *
from PyQt5.QtCore import QThread, pyqtSignal,QTimer,QMutex
import driver.camera_test as A
import log_generate as log
import ctypes

class TimerThread(QThread):
    timerSignal = pyqtSignal(int)
    def __init__(self,timeInterval,commandInstance,functionPtr = None):
        super(TimerThread, self).__init__()
        #self.trigger = QtCore.pyqtSignal(bool)
        self.timerInterval = timeInterval
        self.functionPtr = functionPtr
        executable = self.CheckPtrCallable()
        self.cmd = commandInstance
        print(self.cmd.payload)
        if executable:
            # pass
            self.a = self.ThreadTimer()
        else:
            # self.ThreadTimer()
            pass
    def function(self):
        print(self.cmd.payload)
        #A.CaptureVideo(a1.payload)
    def ThreadTimer(self):
        self.threadTimer = QTimer()
        self.threadTimer.setInterval(self.timerInterval)
        self.threadTimer.timeout.connect(self.function)
        #self.threadTimer.setSingleShot(True)
        self.threadTimer.setTimerType(QtCore.Qt.PreciseTimer)
        a = self.threadTimer.start(1000)
        print(id(a))
    def CheckPtrCallable(self) -> bool:
        if callable(self.function):
            logging.debug("The function given can be triggered")
            return True
        else:
            logging.warning("The function Ptr is not a iterable instance.")
            return False

    def run(self):

        # self.threadTimer = QTimer()
        # self.threadTimer.setInterval(self.timerInterval)
        # self.threadTimer.timeout.connect(self.function)
        # self.threadTimer.setSingleShot(True)

        # currentTime = QtCore.QTime.currentTime()
        logging.info("A new thread will be created for timing and automatic recording")
        logging.info(self.timerInterval)
        self.threadTimer.start(self.timerInterval)
        try:
            logging.info("A timer will be triggered in the next clock cycle.")
        except Exception as e:
            logging.warning("The function Ptr is not a iterable instance.")
            logging.warning(e)
        self.timerSignal.emit(str(self.timerInterval))
        #print(currentTime.hour())
    def __del__(self):
        self.threadTimer.killTimer(id(self.a))
class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        #self.internel_timer = TimerThread()
        #self.internel_timer.start()
        #self.internel_timer.trigger(self.recordEachHour_disableImmeButton)
        self.setupUi(self)
        #self.filepath = ''
        self.recordImme_flag = False
        log.Log_Init()
        self.settings = {
                         "H264_Folder": None,
                         "MP4_Folder": None,
                         "width": None,
                         "height": None,
                         "duration": "0",
                         "iniFile": None,
                         "framerate": None
                         }
        # QtWidgets.QFileDialog.open(self.actionSave_Settings)
        self.actionOpen_Setting_File.triggered.connect(lambda: self.Open_Setting_File())
        self.actionSave_Settings.triggered.connect(lambda: self.Save_Setting_File())
        # self.fileOpen.triggered.connect(self.openMsg)  # the event of element menu is triggered
        self.Open_Setting_File_init("../config.ini")
        self.mutexLock = True
    @property
    def Setting(self)  -> dict:
        return self.settings
    @Setting.setter
    def Setting(self,dictIn)  -> None:
        self.settings = dictIn
        #logging.INFO("New set take into effect!")
    def applySettings(self):
        print(self.WeightBox.text())
        time_min = int(self.timeEdit_duration.time().toPyTime().minute)
        time_sec = int(self.timeEdit_duration.time().toPyTime().second)
        self.settings["duration"] = str(  (time_sec+time_min*60)*1000 )
        # self.settings["duration"] = str(self.settings["duration"])

        print(self.settings["duration"])
    def functionTest(self):
        print("JKLKHJ")
    def openOutputH264File(self):
        self.settings['H264_Folder'] = PyQt5.QtWidgets.QFileDialog.getExistingDirectory()
        self.filePath_H264.setText(self.settings['H264_Folder'])
        print(self.settings['H264_Folder'])

    def openOutputMP4File(self):
        self.settings['MP4_Folder'] = PyQt5.QtWidgets.QFileDialog.getExistingDirectory()
        self.filePath_MP4.setText(self.settings['MP4_Folder'])
        print(self.settings['MP4_Folder'])

    def Open_Setting_File(self):
        self.settings["iniFile"] = QtWidgets.QFileDialog.getOpenFileName()[0]
        camera_config,path_config,other_config = A.readConfig(self.settings["iniFile"])
        self.settings = self.settings | camera_config
        self.HeightBox.setValue(int(self.settings["height"]))
        self.WeightBox.setValue(int(self.settings["width"]))
        self.FPS.setValue(int(self.settings["framerate"]))

        self.filePath_H264.setText(path_config["root_path"]+path_config["raw_path"])
        self.filePath_MP4.setText(path_config["root_path"] + path_config["mp4_path"])
        self.filePath_H264.home(False)
        self.filePath_MP4.home(False)
        print(camera_config,path_config,other_config)
        print(self.settings["iniFile"],self.settings)

    def Open_Setting_File_init(self,filePath):
        camera_config,path_config,other_config = A.readConfig(filePath)
        self.settings = self.settings | camera_config
        self.settings = self.settings | other_config
        self.settings = self.settings | path_config
        self.HeightBox.setValue(int(self.settings["height"]))
        self.WeightBox.setValue(int(self.settings["width"]))
        self.FPS.setValue(int(self.settings["framerate"]))
        self.filePath_H264.setText(path_config["root_path"]+"/"+path_config["raw_path"])
        self.filePath_MP4.setText(path_config["root_path"] +"/"+ path_config["mp4_path"])
        self.filePath_H264.home(False)
        self.filePath_MP4.home(False)
        #print(camera_config,path_config,other_config)
        #print(self.settings["iniFile"],self.settings)

    def Save_Setting_File(self):
        self.settings["iniFile"] = QtWidgets.QFileDialog.getOpenFileName()
        logging.debug('Init file saved as %s' %(self.settings["iniFile"][0]))
    def recordEachHour_disableImmeButton(self):
        self.recordImme_flag = not self.recordImme_flag
        self.pushButton_recordImme.setDisabled(self.recordImme_flag)
        a1 = self.genCmdInstance()
        print(a1.payload)
        self.timerThread = TimerThread(timeInterval=1,functionPtr=self.functionTest,commandInstance=a1)
        if self.recordImme_flag == False:
            # self.timerThread.timerSignal.connect()
            #self.timerThread.setProperty("timeInterval",5)
            # self.timerThread.setProperty("function" ,self.openOutputFolder)
            # self.timerThread.function = self.openOutputFolder
            self.timerThread.threadTimer.moveToThread(self.timerThread)
            #self.timerThread.start()
        else:
            self.timerThread.quit()
            pass
    def openOutputFolder(self):
        pass
    def recordAsPlan(self,msg):
        print(msg)
        pass
    def recordImme(self):
        a1 = self.genCmdInstance()
        A.CaptureVideo(a1)
    def genCmdInstance(self):
        a = self.settings
        a1 = A.generateCommand_str_classInline(a)
        logging.info(a1.payload)
        return a1
    def previewImme(self):
        pass

    def __del__(self):
        self.internel_timer.finished()
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())
