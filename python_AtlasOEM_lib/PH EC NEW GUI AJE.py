import RPi.GPIO as GPIO
import tkinter as tk
import time
import threading
from AtlasOEM_PH import AtlasOEM_PH
from AtlasOEM_EC import AtlasOEM_EC
import time
from ATLAS_OEM_Calibration4 import main

from tkinter import messagebox
global fullscreen
from PIL import ImageTk,Image
from tkinter import *

#c = Canvas(top, bg="blue", height=250, width=300)



# Return to windowed mode


# Automatically resize font size based on window siz
def read_sensor():
    
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
        var.set(f'PH : {ph_val : }')
        var1.set(f'EC : {ec_val : }')
        print("EC: " + str(ec_val)#", TDS: " + str(ec_val[1])  # print the readings
              + "\t PH: " + str(ph_val))
                         # wait 1 second to get more readings
        time.sleep(.5) 

# create the thread
task = threading.Thread(target=read_sensor, daemon=True)
task1 = threading.Thread(target=main, daemon=True)
#task1 = threading.Thread(target=read_sensor, daemon=True)

root = tk.Tk()
root.title("PH EC Controller")
var = tk.StringVar()
var1 = tk.StringVar()
lbl = tk.Label(root, textvariable=var, width=40, height=5, font=('Consolas', 24, 'bold'))
lbl.pack()
lbl1 = tk.Label(root, textvariable=var1, width=40, height=5, font=('Consolas', 24, 'bold'))
lbl1.pack()

task.start()


#root.attributes('-fullscreen',True)
root.mainloop()
