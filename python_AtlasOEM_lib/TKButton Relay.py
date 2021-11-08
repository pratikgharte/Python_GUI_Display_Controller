import tkinter as tk
from tkinter import font

import RPi.GPIO as GPIO

# Declare global variables
button_on = None
button_off = None

# Pin definitions
led_pin = 4,17,27,22

# This gets called whenever the ON button is pressed
def on():

    global button_on
    global button_off

    # Disable ON button, enable OFF button, and turn on LED
    button_on.config(state=tk.DISABLED, bg='gray64')
    button_off.config(state=tk.NORMAL, bg='gray99')
    GPIO.output(led_pin, GPIO.HIGH)

# This gets called whenever the OFF button is pressed
def off():

    global button_on
    global button_off

    # Disable OFF button, enable ON button, and turn off LED
    button_on.config(state=tk.NORMAL, bg='gray99')
    button_off.config(state=tk.DISABLED, bg='gray64')
    GPIO.output(led_pin, GPIO.LOW)

# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)

# Set LED pin as output and turn it off by default
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)

# Create the main window
root = tk.Tk()
root.title("LED Switch")

# Create the main container
frame = tk.Frame(root)

# Lay out the main container
frame.pack()

# Create widgets
button_font = font.Font(family='Helvetica', size=24, weight='bold')
button_on = tk.Button(frame, text="ON", width=4, command=on, 
                        state=tk.NORMAL, font=button_font, bg='gray99')
button_off = tk.Button(frame, text="OFF", width=4, command=off, 
                        state=tk.DISABLED, font=button_font, bg='gray64')

# Lay out widgets
button_on.grid(row=0, column=0)
button_off.grid(row=1, column=0)

# Run forever!
root.mainloop()

# Neatly release GPIO resources once window is closed
GPIO.cleanup()
