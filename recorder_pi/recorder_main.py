import logging
import os

import PyQt5.QtCore,PyQt5.QtWidgets
from record import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
import driver.camera_test as A
import log_generate as log
from datetime import datetime
# import FTP_service.server as FTPserver

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.recordImme_flag = False
        self.showPreview_flag = False
        self.autoConversion_flag = False
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
        self.actionOpen_Setting_File.triggered.connect(lambda: self.Open_Setting_File())
        self.actionSave_Settings.triggered.connect(lambda: self.Save_Setting_File())
        self.Open_Setting_File_init("../config.ini")
    @property
    def Setting(self)  -> dict:
        return self.settings
    @Setting.setter
    def Setting(self,dictIn)  -> None:
        self.settings = dictIn
    def applySettings(self) -> bool:
        print(self.WeightBox.text())
        time_min = int(self.timeEdit_duration.time().toPyTime().minute)
        time_sec = int(self.timeEdit_duration.time().toPyTime().second)
        if (time_min*60 + time_sec) >= 59*60:
            QMessageBox.warning(self,
                                "Time Out Warning!",
                                "Your time setting has Larger than potential recording period, which will cause access conflict on the device. Please set the video duration smaller than 1 hour")
            return False
        else:
            self.settings["duration"] = str(  (time_sec+time_min*60)*1000 )
        print(self.settings["duration"])
        return True

    def openOutputH264File(self):
        self.settings['H264_Folder'] = PyQt5.QtWidgets.QFileDialog.getExistingDirectory()
        if self.settings['H264_Folder'] != '':
            self.filePath_H264.setText(self.settings['H264_Folder'])
        print(self.settings['H264_Folder'])

    def openOutputMP4File(self):
        self.settings['MP4_Folder'] = PyQt5.QtWidgets.QFileDialog.getExistingDirectory()
        if self.settings['MP4_Folder'] != "":
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

    def Save_Setting_File(self):
        self.settings["iniFile"] = QtWidgets.QFileDialog.getOpenFileName()
        logging.debug('Init file saved as %s' %(self.settings["iniFile"][0]))
    def recordEachHour_disableImmeButton(self):
        self.recordImme_flag = not self.recordImme_flag
        self.pushButton_recordImme.setDisabled(self.recordImme_flag)
        self.genTimer()
        if self.recordImme_flag == True:
            self.applySettings()
            timePast_minute = datetime.now().minute
            timeRemain_msec = (59-timePast_minute)*60*1000
            self.threadTimer.start(timeRemain_msec)
        else:
            try:
                self.threadTimer.stop()
            except Exception as E:
                logging.info(E)
                logging.info("The timer is not started, so there is no necessary to stop.")
    def openOutputFolder(self):
        pass
    def recordImme(self):
        self.applySettings()
        if self.recordImme_flag == True:
            self.threadTimer.start(60*1000)
        a1 = self.genCmdInstance()
        rawFileName,rawFilePath = A.CaptureVideo(a1)
        if self.autoConversion_flag:
            destFileName = rawFileName+".mp4"
            print(destFileName)
            convertCmd = ["ffmpeg","-r",str(self.settings["framerate"]),"-i",rawFilePath,destFileName]
            convertCmd = " ".join(convertCmd)
            print(convertCmd)
            os.system(convertCmd)
    def genCmdInstance(self):
        a = self.settings
        a1 = A.generateCommand_str_classInline(a)
        logging.info(a1.payload)
        return a1
    def autoConversion(self):
        self.autoConversion_flag = not self.autoConversion_flag
        #os.system("ffmpeg -r 80 -i 05_43_11.h264 output.mp4")
        pass
    def genTimer(self):
        self.threadTimer = QTimer()
        self.threadTimer.timeout.connect(self.recordImme)
        self.threadTimer.setSingleShot(True)
        return

    def previewImme(self):
        pass

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())
