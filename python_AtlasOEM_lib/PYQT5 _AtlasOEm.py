import sys
import fcntl
import io
import time
import threading 
from time import sleep
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLineEdit, QPushButton, QWidget, QDialog, QTextEdit, QLabel, QMenu, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTime, QTimer, QRect
from PyQt5 import QtCore


versionNumber = 'V0.1'

inTemp = 0.00
temp_average = 0.00
temp_counter = 0

pH = 0.00
pH_average = 0.00
pH_counter = 0

do = 0.00
do_average = 0.00
do_counter = 0

class mainMenu(QMainWindow):
	def __init__(self):
		super().__init__()
		self.topL = 20
		self.top = 40
		self.width = 800
		self.height = 400
		self.title = ('WIST Batch Reactor ' + versionNumber)
		self.initUI()
		
	def initUI(self):
		
		# initilize main window
		self.setWindowTitle(self.title)
		self.setGeometry(self.topL, self.top, self.width, self.height)
		
		#initlize menu and status bars
		menubar = self.menuBar()
		self.statusBar()
				
		#define file menu and and add options to it.
		exitAct = QAction('&Exit', self)
		exitAct.setShortcut('Ctrl-Q')
		exitAct.setStatusTip('Exit Application')
		exitAct.triggered.connect(qApp.quit)
		
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAct)		
		
		# Reactor conditions title
		self.reactor_title = QLabel('<b><u>Reactor Conditions</u></b>', self)		
		font = self.reactor_title.font()	
		font.setPointSize(20)
		self.reactor_title.setFont(font)	
		self.reactor_title.setGeometry(QRect(10,20,250,100))
		
		# Temperature title
		self.temperature_label = QLabel('<b>Temperature: </b>', self)
		font = self.temperature_label.font()
		font.setPointSize(18)
		self.temperature_label.setFont(font)
		self.temperature_label.setGeometry(QRect(10,50,200,100))
		
		# pH Title
		self.pH_label = QLabel('<b>pH: </b>', self)
		font = self.pH_label.font()
		font.setPointSize(18)
		self.pH_label.setFont(font)
		self.pH_label.setGeometry(QRect(10,75,200,100))
		
		# Dissolved oxygen title
		self.do_label = QLabel('<b>Dissolved Oxygen: </b>', self)
		font = self.do_label.font()
		font.setPointSize(18)
		self.do_label.setFont(font)
		self.do_label.setGeometry(QRect(10,100,210,100))				
		
		# Temperature label
		displayInTemp = '{0:0.2f}'.format(inTemp)
		self.currentTempIn = QLabel(str(displayInTemp) + '\u2103' , self)
		font = self.currentTempIn.font()
		font.setPointSize(18)
		self.currentTempIn.setFont(font)
		self.currentTempIn.setGeometry(QRect(175,50,200,100))
		
		# current pH value
		pH_display = '{0:0.2f}'.format(float(pH))
		self.pH_current = QLabel(str(pH_display), self)
		font = self.pH_current.font()
		font.setPointSize(18)
		self.pH_current.setFont(font)
		self.pH_current.setGeometry(QRect(175,75,200,100))
		
		# Current dissolved oxygen value
		do_display = '{0:0.2f}'.format(float(do))
		self.do_current = QLabel(str(do_display) + ' mg/L', self)
		font = self.do_current.font()
		font.setPointSize(18)
		self.do_current.setFont(font)
		self.do_current.setGeometry(QRect(225,100,200,100))				
		
	def update_temperature(self):						
		displayInTemp = '{0:0.2f}'.format(float(inTemp))		
		self.currentTempIn.setText(str(displayInTemp) + '\u2103')
		average_temperature()  
		return
		
	def update_pH(self):
		pH_display = '{0:0.2f}'.format(float(pH))
		self.pH_current.setText(str(pH_display))
		average_pH()
		return
		
	def update_do(self):
		do_display = '{0:0.2f}'.format(float(do))
		self.do_current.setText(str(do_display) + ' mg/L')
		average_do()
		return


class temperature_i2c(threading.Thread):
	long_timeout = 1.5
	def __init__(self, address , bus):
		threading.Thread.__init__(self)
		self.file_read = io.open("/dev/i2c-" + str(bus), "rb", buffering=0)
		self.file_write = io.open("/dev/i2c-" + str(bus), "wb", buffering=0)
		self.set_i2c_address(address)

	def set_i2c_address(self, addr):
		I2C_SLAVE = 0x703
		fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
		fcntl.ioctl(self.file_write, I2C_SLAVE, addr)

	def write(self, string):
        # appends the null character and sends the string over I2C
		string += "\00"
		self.file_write.write(bytes(string, 'UTF-8'))

	def read(self, num_of_bytes = 31):
        # reads a specified number of bytes from I2C,
        # then parses and displays the result
		res = self.file_read.read(num_of_bytes)  # read from the board
        # remove the null characters to get the response
		response = [x for x in res if x != '\x00']
		if response[0] == 1:  # if the response isn't an error
            # change MSB to 0 for all received characters except the first
            # and get a list of characters
			char_list = [chr(x & ~0x80) for x in list(response[1:])]
            # NOTE: having to change the MSB to 0 is a glitch in the
            # raspberry pi, and you shouldn't have to do this!
            # convert the char list to a string and returns it
			return ''.join(char_list[0:5])
		else:
			return "Error " + str(response[0])

	def query(self):		
        # write a command to the board, wait the correct timeout,
        # and read the response
		global inTemp
		global temp_counter
		string = "R"
		self.write(string)
        # the read and calibration commands require a longer timeout
		if((string.upper().startswith("R")) or
           (string.upper().startswith("CAL"))):
			time.sleep(self.long_timeout)
		elif((string.upper().startswith("SLEEP"))):
			return "sleep mode"
		else:
			time.sleep(self.short_timeout)        
		inTemp = self.read()
		print ('Temperature reading: ' + str(inTemp))
		temp_counter = temp_counter + 1                 
		return        

	def close(self):
		self.file_read.close()
		self.file_write.close()
        
def average_temperature():
	global temp_average
	temp_average = (temp_average + float(inTemp))
	current_average = temp_average / temp_counter
	print ('Average temperature: ' + str(current_average))
	return


def main():		
	app = QApplication(sys.argv)
	temp_probe = temperature_i2c(102,1)
	temp_probe.start()	
	temp_probe.join()
	ex = mainMenu()		
	timer = QTimer()
	timer.start(5000)	
	timer.timeout.connect(temp_probe.query)	
	timer.timeout.connect(ex.update_temperature)
	ex.show()	
	sys.exit(app.exec_())
			
if __name__ == '__main__':
	main()
