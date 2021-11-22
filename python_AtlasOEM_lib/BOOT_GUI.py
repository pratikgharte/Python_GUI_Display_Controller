import RPi.GPIO as GPIO
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import ttk
import time
import tkinter.messagebox
import threading
from AtlasOEM_PH import AtlasOEM_PH
from AtlasOEM_EC import AtlasOEM_EC
import time
from tkinter import messagebox
global fullscreen
from PIL import ImageTk,Image
from tkinter import *
global ph_HIGH
global ph_LOW
import time
import board
import digitalio
import adafruit_max31865
import os
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import Tk, Canvas, Frame, BOTH
from tkinter.messagebox import showinfo
PHT = 0
ECT = 0
number = 0
number1 = 0
number2 = 0
number3 = 0
number4 = 0
ec_val = 0
ph_val = 0
#var10 = 0
GPIO.setwarnings(False)
PH_HIGH = 4
PH_LOW = 17
EC_HIGH = 27
EC_LOW = 22
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

def helloCallBack1():
    os.system('python PlotPH.py')
   
    
def helloCallBack2():
    os.system('python PlotEC.py')
    
def helloCallBack3():
    os.system('python PH_EC_HoldingTCP.py')
def read_sensor1():
    global var2
    global var1
    global var20
    global PH
    global EC
    global ec_val
    global ph_val
    PH = AtlasOEM_PH(name = "PH") # create an OEM PH object
    EC = AtlasOEM_EC(name = "EC") # create an OEM EC object
    #DO = AtlasOEM_DO(name = "DO") # create an OEM DO object
    
    PH.write_active_hibernate(1) # tell the circuits to start taking readings
    EC.write_active_hibernate(1)
    #DO.write_active_hibernate(1)
    
    def get_OEM_reading(OEM_circuit, readfunction):    # creates a closure to take readings for each circuit         
        reading = [1]                                  # we use a list to approximate a static variable to cache previous readings
        def OEM_reading_closure():                     # make a custom function to do the readings
            if OEM_circuit.read_new_reading_available():   # if we have a new reading
                reading[0] = readfunction()            # get it from the circuit
                #print("OEM " + OEM_circuit.get_name() + \
                #      " reading: " + str(reading))  # print the reading
                OEM_circuit.write_new_reading_available(0)  # then clear the new reading register 
                                                    # so the circuit can set the register
                                                    # high again when it acquires a new reading
            return reading[0]                       # return the value in the list
        return OEM_reading_closure                  # return the custom function without calling it, so we can call it when we want readings
    
    def get_all_EC_values():                        # we can gt all 3 EC values by returning them in a list
        EC_val = EC.read_EC_reading()
        #TDS_val = EC.read_TDS_reading()
        #sal_val = EC.read_salinitiy_reading()
        return EC_val #,TDS_val, sal_val]
    
    read_pH = get_OEM_reading(PH, PH.read_PH_reading) #assign the closures so we can call them to get readings
    read_EC = get_OEM_reading(EC, get_all_EC_values)
    #read_pH = float("{0:.1f}".format(read_pHraw))
    #read_EC = float("{0:.1f}".format(ead_ECraw))
    #read_DO = get_OEM_reading(DO, DO.read_DO_reading)
    
    #time.sleep(20)
    # give circuits time to get the initial readings
    
    def read_temp():
        spi = board.SPI()
        cs = digitalio.DigitalInOut(board.D5)  # Chip select of the MAX31865 board.
        sensor = adafruit_max31865.MAX31865(spi, cs)
        global temp
        # Read temperature.
        tempraw = sensor.temperature
        temp = float("{0:.1f}".format(tempraw))
        # Print the value.
        #print("Temperature: {0:0.1f}C".format(temp))
        # Delay for a second.
        
        return temp
    
        
    while True:
        
        ec_val = read_EC()      #take readings from the closures
        ph_val = read_pH()
        temp_val=read_temp()
#         time.sleep(10)
        #do_val = read_DO()
        #var2.set(f'PH:{ph_val:}')
        #var1.set(f'EC:{ec_val:}')
        #var20.set(f'Temperature:{temp_val:}')
        #print("EC:" + str(ec_val), "Temperature:" + str(temp)  # print the readings
              #+ "\t PH:" + str(ph_val))
        ECT = ec_val
        ECT2=int(ECT)
        #PHT =  ph_val
        #print(ECT2)
        #print(str(PHT))
        #print(str(ECT))
       
        
        #GPIO.output(EC_HIGH, GPIO.LOW)
        GPIO.output(EC_HIGH, GPIO.HIGH)
        if(number == 0):
            GPIO.output(PH_LOW, GPIO.LOW)
            GPIO.output(PH_HIGH, GPIO.LOW)
            #GPIO.output(EC_LOW, GPIO.LOW)
            #GPIO.output(EC_HIGH, GPIO.LOW)
        
        
        elif(number1==0):
            GPIO.output(PH_LOW, GPIO.LOW)
            GPIO.output(PH_HIGH, GPIO.LOW)
            #GPIO.output(EC_LOW, GPIO.LOW)
            #GPIO.output(EC_HIGH, GPIO.LOW)
        elif(number2==0):
            #GPIO.output(PH_LOW, GPIO.LOW)
            #GPIO.output(PH_HIGH, GPIO.LOW)
            GPIO.output(EC_LOW, GPIO.LOW)
            GPIO.output(EC_HIGH, GPIO.LOW)
            
        #elif(ECT > 0):
            #GPIO.output(EC_HIGH, GPIO.HIGH)
        
        elif(ECT < number2):
            GPIO.output(EC_HIGH, GPIO.LOW)
            
        #

def read_sensor():
    global var2
    global var1
    global var20
    global PH
    global EC
    global ec_val
    global ph_val
    PH = AtlasOEM_PH(name = "PH") # create an OEM PH object
    EC = AtlasOEM_EC(name = "EC") # create an OEM EC object
    #DO = AtlasOEM_DO(name = "DO") # create an OEM DO object
    
    PH.write_active_hibernate(1) # tell the circuits to start taking readings
    EC.write_active_hibernate(1)
    #DO.write_active_hibernate(1)
    
    def get_OEM_reading(OEM_circuit, readfunction):    # creates a closure to take readings for each circuit         
        reading = [1]                                  # we use a list to approximate a static variable to cache previous readings
        def OEM_reading_closure():                     # make a custom function to do the readings
            if OEM_circuit.read_new_reading_available():   # if we have a new reading
                reading[0] = readfunction()            # get it from the circuit
                #print("OEM " + OEM_circuit.get_name() + \
                #      " reading: " + str(reading))  # print the reading
                OEM_circuit.write_new_reading_available(0)  # then clear the new reading register 
                                                    # so the circuit can set the register
                                                    # high again when it acquires a new reading
            return reading[0]                       # return the value in the list
        return OEM_reading_closure                  # return the custom function without calling it, so we can call it when we want readings
    
    def get_all_EC_values():                        # we can gt all 3 EC values by returning them in a list
        EC_val = EC.read_EC_reading()
        #TDS_val = EC.read_TDS_reading()
        #sal_val = EC.read_salinitiy_reading()
        return EC_val #,TDS_val, sal_val]
    
    read_pH = get_OEM_reading(PH, PH.read_PH_reading) #assign the closures so we can call them to get readings
    read_EC = get_OEM_reading(EC, get_all_EC_values)
    #read_pH = float("{0:.1f}".format(read_pHraw))
    #read_EC = float("{0:.1f}".format(ead_ECraw))
    #read_DO = get_OEM_reading(DO, DO.read_DO_reading)
    
    time.sleep(10)
    # give circuits time to get the initial readings
    
    def read_temp():
        spi = board.SPI()
        cs = digitalio.DigitalInOut(board.D5)  # Chip select of the MAX31865 board.
        sensor = adafruit_max31865.MAX31865(spi, cs)
        global temp
        # Read temperature.
        tempraw = sensor.temperature
        temp = float("{0:.1f}".format(tempraw))
        # Print the value.
        #print("Temperature: {0:0.1f}C".format(temp))
        # Delay for a second.
        #time.sleep(.5)
        return temp
        time.sleep(10)
        
    while True:
        
        ec_val = read_EC()      #take readings from the closures
        ph_val = read_pH()
        temp_val=read_temp()
        
        #do_val = read_DO()
        var2.set(f'PH:{ph_val:}')
        var1.set(f'EC:{ec_val:}')
        var20.set(f'Temperature:{temp_val:}')
        print("EC:" + str(ec_val), "Temperature:" + str(temp)  # print the readings
              + "\t PH:" + str(ph_val))
        ECT = ec_val
        ECT2=int(ECT)
        PHT =  ph_val
        print(ECT2)
        #print(str(PHT))
        #print(str(ECT))
        time.sleep(10)
        
        #GPIO.output(EC_HIGH, GPIO.LOW)
        #GPIO.output(EC_HIGH, GPIO.HIGH)
        if(number == 0):
            GPIO.output(PH_LOW, GPIO.LOW)
            GPIO.output(PH_HIGH, GPIO.LOW)
            #GPIO.output(EC_LOW, GPIO.LOW)
            #GPIO.output(EC_HIGH, GPIO.LOW)
        
        
        elif(number1==0):
            GPIO.output(PH_LOW, GPIO.LOW)
            GPIO.output(PH_HIGH, GPIO.LOW)
            #GPIO.output(EC_LOW, GPIO.LOW)
            #GPIO.output(EC_HIGH, GPIO.LOW)
        elif(number2==0):
            #GPIO.output(PH_LOW, GPIO.LOW)
            #GPIO.output(PH_HIGH, GPIO.LOW)
            GPIO.output(EC_LOW, GPIO.LOW)
            GPIO.output(EC_HIGH, GPIO.LOW)
          
        elif(PHT < number):
            GPIO.output(PH_HIGH, GPIO.HIGH)
            GPIO.output(PH_LOW, GPIO.LOW)
            
        elif(PHT > number1):
            GPIO.output(PH_LOW, GPIO.HIGH)
            GPIO.output(PH_HIGH, GPIO.LOW)
            
            #GPIO.output(EC_LOW, GPIO.HIGH)   
        #elif(ECT2 > number2):
           # GPIO.output(27, GPIO.HIGH)
            
        
def Cal_4_Mode(var3):
    print("Entering CAL 4.0 Mode")
   # var3.set("Please DIP the PH Probe in PH 4.0 Buffer Solution ")
    var3.set("Entering CAL 4.0 Mode")
    PH = AtlasOEM_PH() # create an OEM PH object

    PH.write_active_hibernate(1) # tell the circuit to start taking readings

            # high again when it acquires a new reading
            
    PH.read_calibration_data()
   
    PH.write_calibration_request(0)
    PH.write_calibration_data(4.00)
    #PH.write_calibration_request(0)
            #PH.write_calibration_request(3)
            #PH.write_calibration_request(2)
            #PH.write_calibration_request(0)
            #PH.read_calibration_confirm()
            #time.sleep(1)
    #tk.messagebox.showinfo(title="Calibration 4.0",message="Calibrationg Sensor Please Wait")
    time.sleep(10)
    
            #PH.write_calibration_request(2)
    pH_ReadCal = PH.read_calibration_confirm()
    pH_CalData = PH.read_calibration_data()
                #return self.read_32(0x08)/1000.0
    print("OEM pH CAL reading: " + str(pH_CalData))
    print("OEM pH CALCONF reading: " + str(pH_ReadCal))
    #tk.messagebox.showinfo(title="Calibration 4.0",message="Sensor Calibrated Sucessfully")
    #var3.set("Successfully Calibated LOW POINT PH 4.0")
    
def Cal_7_Mode(var4):
    print("Entering CAL 7.0 Mode")
    #var4.set("Please DIP the PH Probe in PH 7.0 Buffer Solution")
    PH = AtlasOEM_PH() # create an OEM PH object

    PH.write_active_hibernate(1) # tell the circuit to start taking readings

    
    PH.read_calibration_data()
    
    PH.write_calibration_request(1)
    PH.write_calibration_data(7.00)
    #PH.write_calibration_request(1)
            #PH.write_calibration_request(2)
            #PH.write_calibration_request(0)
            #PH.read_calibration_confirm()
            #time.sleep(1)
    tk.messagebox.showinfo(title="Calibration 7.0",message="Calibrationg Sensor Please Wait")
    time.sleep(10)
            #PH.write_calibration_request(2)
    pH_ReadCal = PH.read_calibration_confirm()
    pH_CalData = PH.read_calibration_data()
    #return self.read_32(0x08)/1000.0
    print("OEM pH CAL reading: " + str(pH_CalData))
    print("OEM pH CALCONF reading: " + str(pH_ReadCal))
    #tk.messagebox.showinfo(title="Calibration 7.0",message="Sensor Calibrated Sucessfully")
    #var3.set("Successfully Calibated MID POINT PH 7.0")
    
def Cal_10_Mode(var5):
    print("Entering CAL 10.0 Mode")
    #var5.set("Please DIP the PH Probe in PH 10.0 Buffer Solution")
    PH = AtlasOEM_PH() # create an OEM PH object

    PH.write_active_hibernate(1) # tell the circuit to start taking reading
            
    PH.read_calibration_data()
   
    PH.write_calibration_request(2)
    PH.write_calibration_data(10.00)
    #PH.write_calibration_request(2)
            #PH.write_calibration_request(2)
            #PH.write_calibration_request(0)
            #PH.read_calibration_confirm()
            #time.sleep(1)
    tk.messagebox.showinfo(title="Calibration 10.0",message="Calibrationg Sensor Please Wait")
    time.sleep(10)
            #PH.write_calibration_request(2)
    pH_ReadCal = PH.read_calibration_confirm()
    pH_CalData = PH.read_calibration_data()
                #return self.read_32(0x08)/1000.0
    print("OEM pH CAL reading: " + str(pH_CalData))
    print("OEM pH CALCONF reading: " + str(pH_ReadCal))
    #tk.messagebox.showinfo(title="Calibration 10.0",message="Sensor Calibrated Sucessfully")
    #var5.set("Successfully Calibated MID POINT PH 10.0")
def Cal_EC_Mode(var6):
    print("Entering CAL EC Mode")
    EC = AtlasOEM_EC(name = "EC") # create an OEM EC object
    EC.write_active_hibernate(1)

    

    if EC.read_new_reading_available():   # if we have a new reading
                EC.write_new_reading_available(0)  # then clear the new reading register    # then clear the new reading register 
                EC.read_calibration_data()
                EC_CalData = EC.read_calibration_data()
                print("OEM EC CAL reading: " + str(EC_CalData))
                EC.write_calibration_data(1413)
                EC.write_calibration_request(3)
                #PH.write_calibration_request(2)
                #PH.write_calibration_request(0)
                #PH.read_calibration_confirm()
                tk.messagebox.showinfo(title="Calibration EC 1413",message="Calibrationg Sensor Please Wait")
                #time.sleep(1)
                time.sleep(10)
                #PH.write_calibration_request(2)
                EC_ReadCal = EC.read_calibration_confirm()
                
                print("OEM pH CALCONF reading: " + str(EC_ReadCal))
                #tk.messagebox.showinfo(title="Calibration EC",message="Sensor Calibrated Sucessfully")
                #var6.set("Successfully Calibated EC 1413")
def Cal_DeletePH_Mode(var7):
    PH = AtlasOEM_PH() # create an OEM PH object

    PH.write_active_hibernate(1) # tell the circuit to start taking readings

            # high again when it acquires a new reading
            
    PH.read_calibration_data()
    
    PH.write_calibration_request(0)
    PH.write_calibration_data(0)
            #PH.write_calibration_request(3)
            #PH.write_calibration_request(2)
            #PH.write_calibration_request(0)
            #PH.read_calibration_confirm()
            #time.sleep(1)
    time.sleep(5)
            #PH.write_calibration_request(2)
    pH_ReadCal = PH.read_calibration_confirm()
    pH_CalData = PH.read_calibration_data()
                #return self.read_32(0x08)/1000.0
    print("OEM pH CAL reading: " + str(pH_CalData))
    print("OEM pH CALCONF reading: " + str(pH_ReadCal))
    


def PH_plus():
    global number
    maxN = 14
    number += 0.5
    number = min(maxN, number)
    label.config(text=number)
    print(number)

def PH_minus():
    global number
    minN = 0
    number -= 0.5
    number = max(minN, number)
    label.config(text=number)
    print(number)
    
def PH_plus1():
    global number1
    maxN = 14
    number1 += 0.5
    number1 = min(maxN, number1)
    label6.config(text=number1)
    print(number1)

def PH_minus1():
    global number1
    minN = 0
    number1 -= 0.5
    number1 = max(minN, number1)
    label6.config(text=number1)
    print(number1)
    
def EC_plus():
    global number2
    maxN = 5000
    number2 += 100
    number2 = min(maxN, number2)
    label7.config(text=number2)
    print(number2)

def EC_minus():
    global number2
    minN = 0
    number2 -= 100
    number2 = max(minN, number2)
    label7.config(text=number2)
    print(number2)
    
def EC_plus1():
    global number3
    maxN = 5000
    number3 += 0
    number3 = min(maxN, number3)
    label8.config(text=number3)
    print(number3)

def EC_minus1():
    global number3
    minN = 0
    number3 -= 0
    number3 = max(minN, number3)
    label8.config(text=number3)
    print(number3)

def start_Cal4_Mode(var3):
    t = threading.Thread(target=Cal_4_Mode, args=(var3,))
    t.start()
    
def start_Cal7_Mode(var4):
    t = threading.Thread(target=Cal_7_Mode, args=(var4,))
    t.start()
    
def start_Cal10_Mode(var5):
    t = threading.Thread(target=Cal_10_Mode, args=(var5,))
    t.start()
    
def start_CalEC_Mode(var6):
    t = threading.Thread(target=Cal_EC_Mode, args=(var6,))
    t.start()
def start_CalDeletePH_Mode(var7):
    t = threading.Thread(target=Cal_DeletePH_Mode, args=(var7,))
    t.start()    
#Thread(target = loop2).terminate()    
# create the thread
task = threading.Thread(target=read_sensor, daemon=True)
task1 = threading.Thread(target=helloCallBack3, daemon=True)
task2 = threading.Thread(target=read_sensor1, daemon=True)
task2.start()
task.start()
task1.start()
root = tk.Tk()
root.geometry('800x400')
bg = PhotoImage(file = "farmfluence-Logo.png")
#canvas1 = Canvas(root, width = 800,
                 #height = 450)
#canvas1.grid(row=0,column=1)
#canvas1.pack(fill=Tkinter.BOTH)
  
# Display image
#canvas1.create_image(0, 0, image = bg, anchor = "nw")
  
# Add Text
#canvas1.create_text( 200, 250, text = "Welcome")
#root.geometry("1024x800")
root.title("PH EC Controller")
#bg = PhotoImage(file ="farmfluence-Logo.png")
var2 = tk.StringVar()
var1 = tk.StringVar()
var20 = tk.StringVar()
var3 = tk.StringVar()
var4 = tk.StringVar()
var5 = tk.StringVar()
var6 = tk.StringVar()
var7 = tk.StringVar()


lbl = tk.Label(root, textvariable=var2, width=20, height=2, font=('calibri', 15, 'bold'))
lbl.grid(row=1,column=3)
lbl1 = tk.Label(root, textvariable=var1, width=20, height=2, font=('calibri', 15, 'bold'))
lbl1.grid(row=2,column=3)
lbl2 = tk.Label(root, textvariable=var20, width=20, height=2, font=('calibri', 15, 'bold'))
lbl2.grid(row=3,column=3)

#lbl3 = tk.Label(root, text=var3, width=20, height=2, font=('calibri', 15, 'bold'))
#lbl3.grid(row=8,column=3)
'''
lbl4 = tk.Label(root, textvariable=var4, width=20, height=2, font=('calibri', 15, 'bold'))
lbl4.grid(row=8,column=3)

lbl5 = tk.Label(root, textvariable=var5, width=20, height=2, font=('calibri', 15, 'bold'))
lbl5.grid(row=8,column=3)

lbl6 = tk.Label(root, textvariable=var6, width=20, height=2, font=('calibri', 15, 'bold'))
lbl6.grid(row=8,column=3)

lbl7 = tk.Label(root, textvariable=var20, width=20, height=2, font=('calibri', 15, 'bold'))
lbl7.grid(row=8,column=3)

lbl8 = tk.Label(root, textvariable=var7, width=20, height=2, font=('calibri', 15, 'bold'))
lbl8.grid(row=8,column=3)
'''
label = tk.Label(root, text=number, width=5, height=2, font=('calibri', 15, 'bold'))
label.grid(row=3,column=11)
label3 = tk.Label(root, text="PH HIGH", width=10, height=2, font=('calibri', 12, 'bold'))
label3.grid(row=2,column=11)
label4 = tk.Label(root, text="Thresholds", width=10, height=2, font=('calibri', 15, 'bold'))
label4.grid(row=1,column=12)
label5 = tk.Label(root, text="PH LOW", width=10, height=2, font=('calibri', 12, 'bold'))
label5.grid(row=5,column=11)
label6 = tk.Label(root, text=number1, width=5, height=2, font=('calibri', 15, 'bold'))
label6.grid(row=6,column=11)
label7 = tk.Label(root, text=number2, width=5, height=2, font=('calibri', 15, 'bold'))
label7.grid(row=3,column=12)
label8 = tk.Label(root, text=number3, width=5, height=2, font=('calibri', 15, 'bold'))
label8.grid(row=6,column=12)
label5 = tk.Label(root, text="EC HIGH", width=10, height=2, font=('calibri', 12, 'bold'))
label5.grid(row=2,column=12)
label5 = tk.Label(root, text="EC LOW", width=10, height=2, font=('calibri', 12, 'bold'))
label5.grid(row=5,column=12)
#label = tk.Label(root, text="PH_HIGH Input")
#label.grid(row=4,column=10)
b = tk.Button(root, text="Cal 4.0", width=8, height=1, bg="black", fg = "white",font=("calibri",14), command=lambda: start_Cal4_Mode(var3))
b.grid(row=2,column=0)
c = tk.Button(root, text="Cal 7.0", width=8, height=1, bg="black", fg = "white",font=("calibri",14), command=lambda: start_Cal7_Mode(var4))
c.grid(row=1,column=0)
d = tk.Button(root, text="Cal 10.0", width=8, height=1, bg="black", fg = "white",font=("calibri",14), command=lambda: start_Cal10_Mode(var5))
d.grid(row=3,column=0)
e = tk.Button(root, text="Cal  EC", width=8, height=1, bg="black", fg = "white",font=("calibri",14), command=lambda: start_CalEC_Mode(var6))
e.grid(row=4,column=0)
b1=tk.Button(root, text="Trend PH",bg="black", fg = "white",font=("calibri",14),command=helloCallBack1)
b1.grid(row=5, column=0)
b2=tk.Button(root, text="Trend EC",bg="black", fg = "white",font=("calibri",14),command=helloCallBack2)
b2.grid(row=6, column=0)
#b3=tk.Button(frame, text="Trend Temperature", font=dfont,bg="white",command=animate)
#b3.grid(row=28, column=2, padx=5, pady=5)
PH_plus = tk.Button(root, text="PH +", bg="black", fg = "white", command=PH_plus, font=("calibri", 12))
PH_plus.grid(row=4,column=10)
PH_minus = tk.Button(root, text="PH -", bg="black", fg = "white", command=PH_minus, font=("calibri", 12))
PH_minus.grid(row=4,column=11)

PH_plus1 = tk.Button(root, text="PH +", bg="black", fg = "white", command=PH_plus1, font=("calibri", 12))
PH_plus1.grid(row=7,column=10)
PH_minus1 = tk.Button(root, text="PH -", bg="black", fg = "white", command=PH_minus1, font=("calibri", 12))
PH_minus1.grid(row=7,column=11)

EC_plus = tk.Button(root, text="EC +", bg="black", fg = "white", command=EC_plus, font=("calibri", 12))
EC_plus.grid(row=4,column=12)
EC_minus = tk.Button(root, text="EC -", bg="black", fg = "white", command=EC_minus, font=("calibri", 12))
EC_minus.grid(row=4,column=13)

EC_plus1 = tk.Button(root, text="EC +", bg="black", fg = "white", command=EC_plus1, font=("calibri", 12))
EC_plus1.grid(row=7,column=12)
EC_minus1 = tk.Button(root, text="EC -", bg="black", fg = "white", command=EC_minus1, font=("calibri", 12))
EC_minus1.grid(row=7,column=13)
#image = bg,
#tekstvak_input_user = tk.Entry(root, width=10)
#tekstvak_input_user.insert(0, 19.0)
#tekstvak_input_user.place(row=4,column=10)
root.attributes('-fullscreen',True)
#root.configure(background="green2")

root.mainloop()


