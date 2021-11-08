import RPi.GPIO as GPIO
import tkinter as tk
import time
import threading
from AtlasOEM_PH import AtlasOEM_PH
import time
def read_sensor():
    
    PH = AtlasOEM_PH() # create an OEM PH object

    PH.write_active_hibernate(1) # tell the circuit to start taking readings

    while True:
        if PH.read_new_reading_available():              # if we have a new reading
            pH_reading = PH.read_PH_reading()            # get it from the circuit
            print("OEM pH reading: " + str(pH_reading))  # print the reading
               # then clear the new reading register 
            #return pH_reading                                    # so the circuit can set the register
            var.set(f'PH : {pH_reading : }')
            PH.write_new_reading_available(0)
            
            
        else:
            #print("waiting")
            time.sleep(.5)

# create the thread
task = threading.Thread(target=read_sensor, daemon=True)

root = tk.Tk()

var = tk.StringVar()
lbl = tk.Label(root, textvariable=var, width=40, height=5, font=('Consolas', 24, 'bold'))
lbl.pack()

task.start() # start the reading thread
root.mainloop()