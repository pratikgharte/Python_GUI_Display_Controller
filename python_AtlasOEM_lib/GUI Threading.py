import RPi.GPIO as GPIO
import tkinter as tk
import time
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
#var10 = 0

def read_sensor():
    global var2
    global var1
    global PH
    global EC
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
    #read_DO = get_OEM_reading(DO, DO.read_DO_reading)
    
    time.sleep(.5)               # give circuits time to get the initial readings
    
    while True:
        
        ec_val = read_EC()      #take readings from the closures
        ph_val = read_pH()
        #do_val = read_DO()
        var2.set(f'PH : {ph_val : }')
        var1.set(f'EC : {ec_val : }')
        print("EC: " + str(ec_val)#", TDS: " + str(ec_val[1])  # print the readings
              + "\t PH: " + str(ph_val))
                         # wait 1 second to get more readings
        time.sleep(.5)
        
        #PH = ph_val
        #EC = ec_val
        
        
def Cal_4_Mode(var3):
    print("Entering CAL 4.0 Mode")
    var3.set("Please DIP the PH Probe in PH 4.0 Buffer Solution ")
    PH = AtlasOEM_PH() # create an OEM PH object

    PH.write_active_hibernate(1) # tell the circuit to start taking readings

            # high again when it acquires a new reading
            
    PH.read_calibration_data()
    pH_CalData = PH.read_calibration_data()
                #return self.read_32(0x08)/1000.0
    print("OEM pH CAL reading: " + str(pH_CalData))
    PH.write_calibration_data1(0X00)
    PH.write_calibration_data2(0X00)
    PH.write_calibration_data3(0X0F)
    PH.write_calibration_data4(0XA0)
    PH.write_calibration_request(1)
            #PH.write_calibration_request(3)
            #PH.write_calibration_request(2)
            #PH.write_calibration_request(0)
            #PH.read_calibration_confirm()
            #time.sleep(1)
    time.sleep(10)
            #PH.write_calibration_request(2)
    pH_ReadCal = PH.read_calibration_confirm()
    print("OEM pH CALCONF reading: " + str(pH_ReadCal))
    var3.set("Successfully Calibated LOW POINT PH 4.0")
    
def Cal_7_Mode(var4):
    print("Entering CAL 7.0 Mode")
    var4.set("Please DIP the PH Probe in PH 7.0 Buffer Solution")
    PH = AtlasOEM_PH() # create an OEM PH object

    PH.write_active_hibernate(1) # tell the circuit to start taking readings

    
    PH.read_calibration_data()
    pH_CalData = PH.read_calibration_data()
    #return self.read_32(0x08)/1000.0
    print("OEM pH CAL reading: " + str(pH_CalData))
    PH.write_calibration_data1(0X00)
    PH.write_calibration_data2(0X00)
    PH.write_calibration_data3(0X1B)
    PH.write_calibration_data4(0X5A)
    PH.write_calibration_request(2)
            #PH.write_calibration_request(2)
            #PH.write_calibration_request(0)
            #PH.read_calibration_confirm()
            #time.sleep(1)
    time.sleep(10)
            #PH.write_calibration_request(2)
    pH_ReadCal = PH.read_calibration_confirm()
    print("OEM pH CALCONF reading: " + str(pH_ReadCal))
    var3.set("Successfully Calibated MID POINT PH 7.0")
    
def Cal_10_Mode(var5):
    print("Entering CAL 10.0 Mode")
    #var5.set("Please DIP the PH Probe in PH 10.0 Buffer Solution")
    PH = AtlasOEM_PH() # create an OEM PH object

    PH.write_active_hibernate(1) # tell the circuit to start taking reading
            
    PH.read_calibration_data()
    pH_CalData = PH.read_calibration_data()
                #return self.read_32(0x08)/1000.0
    print("OEM pH CAL reading: " + str(pH_CalData))
    PH.write_calibration_data1(0X00)
    PH.write_calibration_data2(0X00)
    PH.write_calibration_data3(0X27)
    PH.write_calibration_data4(0X10)
    PH.write_calibration_request(3)
            #PH.write_calibration_request(2)
            #PH.write_calibration_request(0)
            #PH.read_calibration_confirm()
            #time.sleep(1)
    time.sleep(10)
            #PH.write_calibration_request(2)
    pH_ReadCal = PH.read_calibration_confirm()
    print("OEM pH CALCONF reading: " + str(pH_ReadCal))
    var5.set("Successfully Calibated MID POINT PH 10.0")
def Cal_EC_Mode(var6):
    EC = AtlasOEM_EC # create an OEM PH object

    EC.write_active_hibernate(1) # tell the circuit to start taking readings   
    EC.read_calibration_data()
    EC_CalData = EC.read_calibration_data()
                #return self.read_32(0x08)/1000.0
    print("OEM EC CAL reading: " + str(EC_CalData))
    EC.write_calibration_data1(0X00)
    EC.write_calibration_data2(0X00)
    EC.write_calibration_data3(0X1B)
    EC.write_calibration_data4(0X5A)
    EC.write_calibration_request(2)
            #PH.write_calibration_request(2)
            #PH.write_calibration_request(0)
            #PH.read_calibration_confirm()
            #time.sleep(1)
    time.sleep(20)
            #PH.write_calibration_request(2)
    EC_ReadCal = PH.read_calibration_confirm()
    print("OEM pH CALCONF reading: " + str(EC_ReadCal))
    var6.set("Successfully Calibated EC 1413")
def Cal_DeletePH_Mode(var7):
    PH = AtlasOEM_PH() # create an OEM PH object

    PH.write_active_hibernate(1) # tell the circuit to start taking readings

            # high again when it acquires a new reading
            
    PH.read_calibration_data()
    pH_CalData = PH.read_calibration_data()
                #return self.read_32(0x08)/1000.0
    print("OEM pH CAL reading: " + str(pH_CalData))
    PH.write_calibration_request(0)
            #PH.write_calibration_request(3)
            #PH.write_calibration_request(2)
            #PH.write_calibration_request(0)
            #PH.read_calibration_confirm()
            #time.sleep(1)
    time.sleep(5)
            #PH.write_calibration_request(2)
    pH_ReadCal = PH.read_calibration_confirm()
    print("OEM pH CALCONF reading: " + str(pH_ReadCal))
    
    


def PH_plus():
    global var8
    var8 = float(tekstvak_input_user.get())
    var8 += 1
    tekstvak_input_user.delete(0, tk.END)
    tekstvak_input_user.insert(0, var8)


def PH_minus():
    global var9
    var9 = float(tekstvak_input_user.get())
    var9 -= 1
    tekstvak_input_user.delete(0, tk.END)
    tekstvak_input_user.insert(0, var9)

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
#def Relay_PH():
    #ph_HIGH = 5
    #ph_LOW = 4
    #if PH > ph_HIGH:
            #GPIO.output(4, GPIO.HIGH)
    #elif EC < ph_LOW:
            #GPIO.output(17, GPIO.LOW)
    #Thread(target = loop2).terminate()    
# create the thread
task = threading.Thread(target=read_sensor, daemon=True)
#task1 = threading.Thread(target=Relay_PH, daemon=True)
#task1 = threading.Thread(target=read_sensor, daemon=True)
task.start()
#task1.start()
root = tk.Tk()
root.title("PH EC Controller")
var2 = tk.StringVar()
var1 = tk.StringVar()
var3 = tk.StringVar()
var4 = tk.StringVar()
var5 = tk.StringVar()
var6 = tk.StringVar()




lbl = tk.Label(root, textvariable=var2, width=40, height=5, font=('Consolas', 15, 'bold'))
lbl.grid(row=2,column=5)
lbl1 = tk.Label(root, textvariable=var1, width=40, height=5, font=('Consolas', 15, 'bold'))
lbl1.grid(row=4,column=5)
label = tk.Label(root, text="PH_HIGH Input")
label.grid(row=4,column=10)
b = tk.Button(root, text="Cal 4.0", height=2, width=10, font=("Arial",14), command=lambda: start_Cal4_Mode(var))
b.grid(row=4,column=0)
c = tk.Button(root, text="Cal 7.0", height=2, width=10, font=("Arial",14), command=lambda: start_Cal7_Mode(var4))
c.grid(row=3,column=0)
d = tk.Button(root, text="Cal 10.0", height=2, width=10, font=("Arial",14), command=lambda: start_Cal10_Mode(var5))
d.grid(row=5,column=0)
e = tk.Button(root, text="Cal EC", height=2, width=10, font=("Arial",14), command=lambda: start_CalEC_Mode(var6))
e.grid(row=2,column=10)
f = tk.Button(root, text="Delete PH Cal", height=2, width=10, font=("Arial",14), command=lambda: start_CalDeletePH_Mode(var7))
f.grid(row=2,column=0)
PH_plus = tk.Button(root, bd=10, width=10, height=1, text="+", command=PH_plus, font=("Helvetica", 12))
PH_plus.grid(row=5,column=10)
PH_minus = tk.Button(root, bd=10, width=10, height=1, text="-", font=("Helvetica", 12), command=PH_minus)
PH_minus.grid(row=6,column=10)

#tekstvak_input_user = tk.Entry(root, width=10)
#tekstvak_input_user.insert(0, 19.0)
#tekstvak_input_user.place(row=4,column=10)
#root.attributes('-fullscreen',True)
root.mainloop()

