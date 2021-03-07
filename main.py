import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QInputDialog, QFileDialog
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
# import numpy as np
import time
import cv2
from tools.ui_main import *
import json
import os

class Main(QtWidgets.QMainWindow):
    # class constructor
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.video_path = ''

        self.timer = QTimer()
        self.timer.timeout.connect(self.get_frames)

        self.ui.pushButton.clicked.connect(self.pick_video)
        self.ui.pushButton_2.clicked.connect(self.pick_destination)
        self.ui.start_btn.clicked.connect(self.framify)
    
    def set_video(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.img_index = 1
        self.timer.start(1)

    def get_frames(self):
        ret, self.frame = self.cap.read()
        if ret == False:
            self.timer.stop()
            self.ui.warning_label.setText('Video Done')
            self.ui.warning_label.setStyleSheet('color:rgb(0,250,0')
            self.cap.release()
            self.ui.start_btn.setStyleSheet('background-color: rgb(0, 143, 0);')
            self.ui.start_btn('Start')
        else:
            height, width, channel = self.frame.shape
            step = channel * width
            # create QImage from image
            qImg = QImage(self.frame.data, width, height, step, QImage.Format_RGB888)
            # show image in img_label
            self.ui.label.setPixmap(QPixmap.fromImage(qImg))
            # Stores frames
            cv2.imwrite(self.ui.frame_line.text()+'/frameNo_'+str(self.img_index)+self.ui.format.currentText(), self.frame)
            self.img_index += 1


    def framify(self):
        if self.ui.start_btn.text() == 'Start':
            self.ui.start_btn.setText('Cancel')
            self.ui.start_btn.setStyleSheet('background-color: rgb(143, 0, 0);')
            self.set_video(self.ui.video_line.text())
        elif self.ui.start_btn.text() == 'Cancel':
            self.timer.stop()
            self.ui.warning_label.setText('Video Done')
            self.cap.release()
            self.ui.start_btn.setText('Start')
            self.ui.start_btn.setStyleSheet('background-color: rgb(0, 143, 0);')


    def pick_video(self):
        # self.ui.pushButton.setText(str(QFileDialog.getExistingDirectory(self, "Select Directory")))
        self.ui.video_line.setText(QFileDialog.getOpenFileName()[0])

    def pick_destination(self):
        self.ui.frame_line.setText(str(QFileDialog.getExistingDirectory(self, "Select Directory")))

def main_window():  # Run application
    app = QApplication(sys.argv)
    # create and show mainWindow
    mainWindow = Main()
    mainWindow.showMaximized()


    sys.exit(app.exec_())


if __name__ == '__main__':
    main_window()
