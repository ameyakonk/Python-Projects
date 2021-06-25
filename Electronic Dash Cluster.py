#from qroundprogressbar import QRoundProgressBar
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from datetime import date
import time
import datetime
import sys

class MyThread(QThread):
    # Create a counter thread
        change_value = pyqtSignal(int)
        def run(self):
            cnt = 0
            while cnt < 100:
                cnt+=1
                time.sleep(0.025)
                self.change_value.emit(cnt)
            while cnt > 0 :
                cnt-=1
                time.sleep(0.025)
                self.change_value.emit(cnt)
                    
                            
class TimeDisplay(QWidget):
        progressPercent=0
        def __init__(self):
            super().__init__()
            self.initUI()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.showTime)
            self.timer.start(1)
            
        def showTime(self):
            self.a=datetime.datetime.now()
            self.update()
            self.label.setText('Date: %s/%s/%s' % (self.a.day,self.a.month,self.a.year) + "\nTime: (%s:%s:%s)" % (self.a.hour,self.a.minute,self.a.second) )
            self.update()
            
        def initUI(self):
            self.setGeometry(200, 200, 500, 400)
            self.setStyleSheet("background-color: #A9A9A9;") 
            self.setWindowTitle('Clock')
            self.setWindowFlags(Qt.FramelessWindowHint)

            self.paintlabel = QLabel(self)
            self.label = QLabel(self)
            self.progresslabel = QLabel(self)
            self.needlelabel = QLabel(self)
            self.speedlabel = QLabel(self)
            self.numberValue()
            
            self.paintlabel.resize(350, 320)
            self.paintlabel.move(100, 90)
            #self.paintlabel.setStyleSheet("background-color: blue")

            self.needlelabel.setAlignment(Qt.AlignCenter)
            self.label.setFont(QFont('Russo One',10))
            self.label.resize(200, 100)
            #self.label.setStyleSheet("background-color: green")

            self.speedlabel.setFont(QFont('Russo One',35))
            #self.speedlabel.move(400, 50)
            self.speedlabel.move(400, 210)
            self.speedlabel.resize(90, 70)
            #self.speedlabel.setStyleSheet("background-color: orange")
            
            self.progresslabel.setFont(QFont('Russo One',10))
            self.progresslabel.resize(50, 100)
            self.progresslabel.move(310, 10)
            #self.progresslabel.setStyleSheet("background-color: lightblue")
            
            self.BatteryPercent()
            self.show()

        def SpeedoMeter(self,val):
            self.speedlabel.setText('%s' % (val))

        def needleDisplay(self,val):
            pixmap = QPixmap('blue_needle.png')
            mappedValue = self.mapValue(val,0,100,-150,30) 
            pixmapScaled = pixmap.scaled(300,300, Qt.KeepAspectRatio)
            pixmap = pixmapScaled.transformed(QTransform().rotate(mappedValue), Qt.SmoothTransformation)
            #diag = (pixmapScaled.width()**2 + pixmapScaled.height()**2)**0.5
            #self.needlelabel.setMinimumSize(int(diag), int(diag))
            self.needlelabel.move(230,170)
            self.needlelabel.resize(200,200)
            self.needlelabel.setPixmap(pixmap)
            #self.needlelabel.setStyleSheet("background-color: lightgreen")
            
        
        def BatteryPercent(self):
            self.progressbar = QProgressBar(self)
            self.progressbar.setGeometry(200,50,100,20)
            #self.progressbar.move(100,100)
            self.progressbar.setMaximum(100)
            self.progressbar.setTextVisible(False)
            self.startThread()
            self.update()
            self.show()

        def startThread(self):
            self.thread = MyThread()
            self.thread.change_value.connect(self.setProgressVal)
            self.thread.change_value.connect(self.SpeedoMeter)
            self.thread.change_value.connect(self.needleDisplay)
            self.thread.change_value.connect(self.setLabels)
            self.thread.start()
 
        def setProgressVal(self, val):
            self.value = val
            self.progressbar.setValue(val)
            mappedValue = self.mapValue(val,0,50,0,255) if val < 50 else self.mapValue(val,50,100,255,0)
            hexValue = hex(int(mappedValue))
            hexValue = hexValue[2:]
            hexValue = hexValue.upper()
            if (len(hexValue) == 1) and val < 50:
                    hexValue = hexValue + '0'  
            if (len(hexValue) == 1) and val > 50:
                    hexValue = '0%s' % hexValue
            self.color='#FF%s' % hexValue +'00' if val < 50 else '#%s' % hexValue +'FF'+'00'
            self.progresslabel.setText('%s' % (val) + " %")
            self.progressbar.setStyleSheet("QProgressBar {border: 1px solid black;border-radius:2px;padding:1px}""QProgressBar::chunk {background: %s}" % self.color )
            #self.progresslabel.setStyleSheet("background-color: lightgreen")
            
        def mapValue(self,val,InMinValue,InMaxValue,OutMinValue,OutMaxValue):
            return (val - InMinValue) * (OutMaxValue - OutMinValue) / (InMaxValue - InMinValue) + OutMinValue

        def numberValue(self):
            self.Valuelabel1 = QLabel(self)
            self.Valuelabel2 = QLabel(self)
            self.Valuelabel3 = QLabel(self)
            self.Valuelabel4 = QLabel(self)
            self.Valuelabel5 = QLabel(self)
            self.Valuelabel6 = QLabel(self)
            self.Valuelabel7 = QLabel(self)
            self.Valuelabel8 = QLabel(self)

            self.fontValue = 20

            self.Valuelabel1.resize(20, 30)
            self.Valuelabel1.move(165, 355)
          #  self.Valuelabel1.setStyleSheet("background-color: blue")
            self.Valuelabel1.setFont(QFont('Russo One',self.fontValue))
            self.Valuelabel1.setText('1')

            self.Valuelabel2.resize(20, 30)
            self.Valuelabel2.move(135, 285)
          #  self.Valuelabel2.setStyleSheet("background-color: blue")
            self.Valuelabel2.setFont(QFont('Russo One',self.fontValue))
            self.Valuelabel2.setText('2')
            
            self.Valuelabel3.resize(20, 30)
            self.Valuelabel3.move(135, 215)
          #  self.Valuelabel3.setStyleSheet("background-color: blue")
            self.Valuelabel3.setFont(QFont('Russo One',self.fontValue))
            self.Valuelabel3.setText('3')
            
            self.Valuelabel4.resize(20, 30)
            self.Valuelabel4.move(160, 155)
          #  self.Valuelabel4.setStyleSheet("background-color: blue")
            self.Valuelabel4.setFont(QFont('Russo One',self.fontValue))
            self.Valuelabel4.setText('4')
            
            self.Valuelabel5.resize(20, 30)
            self.Valuelabel5.move(210, 105)
          #  self.Valuelabel5.setStyleSheet("background-color: blue")
            self.Valuelabel5.setFont(QFont('Russo One',self.fontValue))
            self.Valuelabel5.setText('5')
            
            self.Valuelabel6.resize(20, 30)
            self.Valuelabel6.move(280, 85)
           # self.Valuelabel6.setStyleSheet("background-color: blue")
            self.Valuelabel6.setFont(QFont('Russo One',self.fontValue))
            self.Valuelabel6.setText('6')
            
            self.Valuelabel7.resize(20, 30)
            self.Valuelabel7.move(340, 90)
           # self.Valuelabel7.setStyleSheet("background-color: blue")
            self.Valuelabel7.setFont(QFont('Russo One',self.fontValue))
            self.Valuelabel7.setText('7')
            
            self.Valuelabel8.resize(20, 30)
            self.Valuelabel8.move(400, 110)
           # self.Valuelabel8.setStyleSheet("background-color: blue")
            self.Valuelabel8.setFont(QFont('Russo One',self.fontValue))
            self.Valuelabel8.setText('8')
            
            

        def setLabels(self,val):
                endAngle = int(self.mapValue(self.value,0,100,0,-190))
                self.red = int(self.mapValue(self.value,0,100,0,255))
                self.green = int(self.mapValue(self.value,0,100,255,0))
                paintpixmap = QPixmap(self.paintlabel.size())
                paintpixmap.fill(Qt.transparent)
                paint = QPainter(paintpixmap)
                paint.setPen(QtGui.QPen(QtGui.QColor(self.red,self.green,0,255)  ,15))
                paint.drawArc(70, 35, 280, 280, -120 * 16,endAngle * 16)
                paint.end()
                self.paintlabel.setPixmap(paintpixmap)
                
         
app = QApplication(sys.argv)
dir_ = QDir("Russo_One")
id = QFontDatabase.addApplicationFont('Russo_One/RussoOne-Regular.ttf')
#family = QFontDatabase.applicationFontFamilies(id)[0]
#print(QFontDatabase.applicationFontFamilies(id)[0])
w = TimeDisplay()
w.show()
sys.exit(app.exec_())
