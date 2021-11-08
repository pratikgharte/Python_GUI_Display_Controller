import RPi.GPIO as GPIO
import tkinter as tk
import time
import threading

def read_sensor():
    GPIO.setmode(GPIO.BOARD)
    flowin =7
    GPIO.setup(7,GPIO.IN)
    rate=0
    seconds=0
    pulse=550
    time_new = 0.0
    #numlist=list()

    while True:
        y=2
        time_new = time.time() + 1
        rate_cnt = 0
        #y=numlist.append(x)
        while time.time() <= time_new:
            x=GPIO.input(flowin)
            if y!=x:
                if GPIO.input(flowin)!= 0:
                    rate+= 1
                y=x
        seconds+=1
        litre=rate/pulse
        minutes=seconds/60
        flowrate=litre/minutes
        #print("flowrate",flowrate)
        # update the tkinter label via StringVar
        var.set(f'flowrate: {flowrate:10.2f}')

# create the thread
task = threading.Thread(target=read_sensor, daemon=True)

root = tk.Tk()

var = tk.StringVar()
lbl = tk.Label(root, textvariable=var, width=40, height=5, font=('Consolas', 24, 'bold'))
lbl.pack()

task.start() # start the reading thread
root.mainloop()